import socket
import threading
import signal
import sys
import DBConnection
import datetime
import mysql.connector


class Server:
    def __init__(self, server_ip, port):
        self.server_ip = server_ip
        self.port = port
        self.server_socket = None
        self.is_running = True

    def handle_client(self, client_socket, client_address):
        try:
            db = DBConnection.connect_to_database()
            # Receive data from the client
            client_message = client_socket.recv(5000).decode()
            print("Received message from client:", client_message)
            msg = client_message.split()

            response = ""  # Initialize the response variable

            # handle login request
            if msg[0] == "1":
                try:
                    sql = "SELECT * FROM customer WHERE phone_no = " + msg[1]
                    rows = DBConnection.execute_select_query(db, sql)
                    trimmed_pass = rows[0][4].rstrip(b'\x00')
                    if rows is None:
                        response = "1000"
                    elif trimmed_pass.decode() != msg[2]:
                        response = "1001"
                    else:
                        response = "200 "
                        if rows[0][6]:
                            response += "1 "
                        else:
                            response += "0 "
                        response += rows[0][0] + " " + rows[0][1] + " " + rows[0][2] + " " + rows[0][3] + " " + (
                                rows[0][4].rstrip(b'\x00')).decode() + " " + rows[0][5].strftime("%Y-%m-%d")
                except Exception as e:
                    print("Error while accessing database:", str(e))
                    response = "1004"
                    
            # handle get acc_nos linked to a phone_no request
            elif msg[0] == "2":
                try:
                    sql = "SELECT acc_no FROM account a WHERE a.phone_no = '" + msg[1] + "'"
                    rows = DBConnection.execute_select_query(db, sql)
                    if len(rows) == 0:
                        response = "1002"
                    else:
                        response = "200 "
                        for row in rows:
                            response += row[0]
                            response += " "
                except Exception as e:
                    print("Error while accessing database:", str(e))
                    response = "1004"
                    

            # handle withdraw request
            elif msg[0] == "3":
                sql = "SELECT balance FROM account WHERE acc_no = '{}'".format(msg[1])
                print("query = "+sql)
                rows = DBConnection.execute_select_query(db, sql)
                if rows[0][0] < int(msg[2]):
                    response = "1003"
                else:
                    try:
                        sql = "UPDATE account SET balance = " + str(rows[0][0] - int(msg[2])) + " WHERE acc_no = '{}'".format(msg[1])
                        DBConnection.execute_query(db, sql)
                        sql="INSERT INTO transaction (tid, acc_no, type, amount, time) SELECT COALESCE(MAX(tid), 0) + 1, '{}', 'D', {}, CURRENT_TIMESTAMP FROM transaction".format(msg[1],msg[2])
                        DBConnection.execute_query(db, sql)
                        db.commit()
                        response = "200"
                    except Exception as e:
                        print("Error while accessing database:", str(e))
                        db.rollback()
                        response = "1004"
                        
            # handle deposit request
            elif msg[0] == "4":
                try:
                    sql = "SELECT balance FROM account WHERE acc_no = '{}'".format(msg[1])
                    rows = DBConnection.execute_select_query(db, sql)
                    sql = "UPDATE account SET balance = " + str(rows[0][0] + int(msg[2])) + " WHERE acc_no = '{}'".format(msg[1])
                    DBConnection.execute_query(db, sql)
                    sql="INSERT INTO transaction (tid, acc_no, type, amount, time) SELECT COALESCE(MAX(tid), 0) + 1, '{}', 'C', {}, CURRENT_TIMESTAMP FROM transaction".format(msg[1],msg[2])
                    DBConnection.execute_query(db, sql)
                    db.commit()
                    response = "200"
                except Exception as e:
                    print("Error while accessing database:", str(e))
                    db.rollback()
                    response = "1004"

            # handle branches request
            elif msg[0]=="5":
                try:
                    sql="SELECT bname from branch"
                    rows=DBConnection.execute_select_query(sql,db)
                    response+="200"
                    for row in rows:
                        response+=row[0]+" "
                except Exception as e:
                    print("Error while accessing database:", str(e))
                    response = "1004"
                    
            # handle create account request
            elif msg[0]=="6":
                try:
                    sql="SELECT COUNT(acc_no) FROM account"
                    rows=DBConnection.execute_select_query(sql,db)      
                    count=str(row[0][0])
                    accNo="AC"+count.zfill(14)
                    sql="SELECT bid WHERE bname = {}".format(msg[1])
                    rows=DBConnection.execute_select_query(sql,db)
                    bid=row[0][0]
                    accType=None
                    if msg[3]=="1":
                        accType="S"
                    elif msg[3]=="2":
                        accType="C"
                    sql="INSERT INTO account VALUES({}, {}, {}, {}, {}, {} )".format(accNo,bid,msg[2],str(0),str(1),accType)
                    DBConnection.execute_query(db,sql)
                    response="200 {}".format(accNo)
                except Exception as e:
                    print("Error while accessing database:", str(e))
                    db.rollback()
                    response = "1004"
                
                    
                    
        except mysql.connector.Error as e:
            print("MySQL Error occurred:", str(e))
            response = "5001"  # Handle MySQL database errors

        except Exception as e:
            print("Error occurred during client request:", str(e))
            # response = "500"  # Handle any other unexpected errors

        finally:
            # Close the client socket
            client_socket.sendall(response.encode())
            print("Sending response "+response)
            client_socket.close()
            db.close()

    def start_server(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Set the SO_REUSEADDR option so that port 8080 is immediately reusable
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # Bind the socket to a specific IP and port
            self.server_socket.bind((self.server_ip, self.port))

            # Listen for client connections
            self.server_socket.listen(5)
            print("Server listening on port", self.port)

            while self.is_running:
                # Accept incoming connection
                client_socket, client_address = self.server_socket.accept()
                print("Accepted connection from:", client_address)

                # Handle the client in a separate thread
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
                client_thread.start()

        except KeyboardInterrupt:
            print("Server is shutting down...")
            self.is_running = False

        finally:
            # Close the server socket
            if self.server_socket:
                self.server_socket.close()


def handle_shutdown(signal, frame):
    print("Received shutdown signal...")
    sys.exit(0)


def main():
    SERVER_IP = '127.0.0.1'
    PORT = 8080

    # Create a server instance
    server = Server(SERVER_IP, PORT)

    # Register the shutdown signal handler
    signal.signal(signal.SIGINT, handle_shutdown)

    # Start the server
    server.start_server()

if __name__ == "__main__":
    main()
