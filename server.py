import socket
import threading
import signal
import sys
import DBConnection
import random

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
            elif msg[0] == "5":
                try:
                    sql = "SELECT bid,bname FROM branch"
                    rows = DBConnection.execute_select_query(db, sql)
                    response = "200,"

                    csv_data = []
                    for row in rows:
                        csv_data.append('{}. {}'.format(row[0],row[1]))

                    csv_string = ','.join(csv_data)
                    response += csv_string

                except Exception as e:
                    print("Error while accessing the database:", str(e))
                    response = "1004"

                    
            # handle create account request
            elif msg[0]=="6":
                try:
                    sql="SELECT COUNT(acc_no) FROM account"
                    rows=DBConnection.execute_select_query(db,sql)      
                    count=str(rows[0][0]+1)
                    accNo="AC"+count.zfill(14)
                    accType=None
                    if msg[3]=="1":
                        accType="S"
                    elif msg[3]=="2":
                        accType="C"
                    sql="INSERT INTO account VALUES('{}', {}, {}, {}, {}, '{}' )".format(accNo,str(msg[1]),msg[2],str(0),str(1),accType)
                    DBConnection.execute_query(db,sql)
                    db.commit()
                    response="200 {}".format(accNo)
                except Exception as e:
                    print("Error while accessing database:", str(e))
                    db.rollback()
                    response = "1004"
            
            # handle check balance request
            elif msg[0]=="7":
                try:
                    sql="SELECT balance FROM account WHERE acc_no ='{}'".format(msg[1])
                    rows=DBConnection.execute_select_query(db,sql)
                    response="200 {}".format(str(rows[0][0]))
                except Exception as e:
                    print("Error while accessing database:", str(e))
                    response = "1004"
                    
            # handle get loan request
            elif msg[0]=="8":
                    
                try: 
                    interest_rate = 5
                    sql="INSERT INTO loan (lid, acc_no, amount, interest_rate, start_date, end_date) SELECT COALESCE(MAX(lid), 0) + 1, '{}', {}, {}, NOW(), DATE(DATE_ADD(NOW(), INTERVAL 1 YEAR)) FROM loan".format(msg[1],msg[2],interest_rate)
                    DBConnection.execute_query(db,sql)
                    db.commit()
                    response="200 {}".format(interest_rate)
                except Exception as e:
                    db.rollback()
                    print("Error while accessing database:", str(e))
                    response = "1004"
            
            # handle get new card request
            elif msg[0]=="9":
                try:
                    sql="SELECT COUNT(card_no) FROM card"
                    rows=DBConnection.execute_select_query(db,sql)
                    card_no=str(rows[0][0]+1).zfill(16)
                    pin="0000" # default pin
                    cvv=random.randint(100, 999)
                    sql="INSERT INTO card VALUES ({},'{}','{}',DATE(DATE_ADD(NOW(), INTERVAL 1 YEAR)),{},{})".format(card_no,msg[1],msg[2],pin,cvv)
                    db.commit()
                    response="200 {} {} {}".format(card_no,pin,cvv)
                except Exception as e:
                    db.rollback()
                    print("Error while accessing database:", str(e))
                    response = "1004"
            
            # handle list all accounts request
            elif msg[0]=="10":
                try:
                    sql = "SELECT acc_no, CONCAT(fname, ' ', mname, ' ', ltname) AS full_name FROM customer c,account a WHERE c.phone_no=a.phone_no ORDER BY acc_no"
                    rows=DBConnection.execute_select_query(db,sql)
                    response+="200,"
                    csv_data = []
                    for row in rows:
                        csv_data.append('{}. {}'.format(row[0],row[1]))

                    csv_string = ','.join(csv_data)
                    response += csv_string
                except Exception as e:
                    print("Error while accessing database:", str(e))
                    response = "1004"
                    
            # handle send money from one account to other request
            elif msg[0]=="11":
                try:
                    
                    sql="SELECT balance FROM account WHERE acc_no = '{}'".format(msg[1])
                    rows=DBConnection.execute_select_query(db,sql)
                    if(rows[0][0]<int(msg[3])):
                        response="1003"
                    else:
                        sql="UPDATE account SET balance = balance - {} WHERE acc_no = '{}'".format(msg[3],msg[1])
                        DBConnection.execute_query(db,sql)
                        sql="INSERT INTO transaction (tid, acc_no, type, amount, time) SELECT COALESCE(MAX(tid), 0) + 1, '{}', 'D', {}, CURRENT_TIMESTAMP FROM transaction".format(msg[1],msg[3])
                        DBConnection.execute_query(db,sql)
                        sql="UPDATE account SET balance = balance + {} WHERE acc_no = '{}'".format(msg[3],msg[2])
                        DBConnection.execute_query(db,sql)
                        sql="INSERT INTO transaction (tid, acc_no, type, amount, time) SELECT COALESCE(MAX(tid), 0) + 1, '{}', 'C', {}, CURRENT_TIMESTAMP FROM transaction".format(msg[2],msg[3])
                        DBConnection.execute_query(db,sql)
                        db.commit()
                        response="200"

                except Exception as e:
                    print("Error while accessing database:", str(e))
                    response = "1004"
                    
            # handle get branch for given account no request
            elif msg[0]=="12":
                try:
                    sql="SELECT bname,city,state,pincode FROM branch b,account a WHERE a.acc_no = '{}' AND a.bid=b.bid".format(msg[1])
                    rows=DBConnection.execute_select_query(db,sql)
                    row=rows[0]
                    response="200,{},{},{},{}".format(row[0],row[1],row[2],row[3])
                except Exception as e:
                    print("Error while accessing database:", str(e))
                    response = "1004"
            
            # handle transaction history request
            elif msg[0]=="13":
                try:
                    dur=["WEEK","MONTH","YEAR"]
                    sql = "SELECT type,amount,time FROM transaction WHERE acc_no = '{}' AND time BETWEEN DATE_SUB(NOW(), INTERVAL 1 {}) AND NOW() ORDER BY time".format(msg[1],dur[int(msg[2])-1])
                    rows=DBConnection.execute_select_query(db,sql)
                    response+="200,"
                    csv_data = []
                    for row in rows:
                        csv_data.append('type: {} | amount: {} | time: {}'.format(row[0],row[1],row[2]))

                    csv_string = ','.join(csv_data)
                    response += csv_string
                except Exception as e:
                    print("Error while accessing database:", str(e))
                    response = "1004"
                    

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
