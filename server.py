import socket
import threading
import signal
import sys
import DBConnection
import datetime
class Server:
    def __init__(self, server_ip, port):
        self.server_ip = server_ip
        self.port = port
        self.server_socket = None
        self.is_running = True

    def handle_client(self, client_socket, client_address):
        try:
            db=DBConnection.connect_to_database()
            # Receive data from the client
            client_message = client_socket.recv(5000).decode()
            print("Received message from client:", client_message)
            msg=client_message.split()
            # print("size =")
            # print(len(msg))
            if msg[0] == "1":
                sql = "SELECT * FROM customer WHERE phone_no = " + msg[1]
                rows = DBConnection.execute_select_query(db,sql)
                trimmed_pass=rows[0][4].rstrip(b'\x00')
                if rows is None:
                    response = "1000"
                elif trimmed_pass.decode() != msg[2]:
                    response="1001"
                else:
                    response = "200 "
                    if rows[0][6]:
                        response += "1 "
                    else:
                        response += "0 "
                    response += rows[0][0] + " " + rows[0][1] + " " + rows[0][2] + " " + rows[0][3] + " " + (rows[0][4].rstrip(b'\x00')).decode() + " " + rows[0][5].strftime("%Y-%m-%d")

                    
                    


            client_socket.sendall(response.encode())

        except Exception as e:
            print("Error occurred during client request:", str(e))

        finally:
            # Close the client socket
            client_socket.close()

    def start_server(self):
        # Create a socket object
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to a specific IP and port
        self.server_socket.bind((self.server_ip, self.port))

        # Listen for client connections
        self.server_socket.listen(5)
        print("Server listening on port", self.port)

        while self.is_running:
            try:
                # Accept incoming connection
                client_socket, client_address = self.server_socket.accept()
                print("Accepted connection from:", client_address)

                # Handle the client in a separate thread
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
                client_thread.start()

            except KeyboardInterrupt:
                print("Server is shutting down...")
                self.is_running = False

        # Close the server socket
        self.server_socket.close()

    def handle_shutdown(self, signal, frame):
        print("Received shutdown signal...")
        self.is_running = False


def main():
    SERVER_IP = '127.0.0.1'
    PORT = 8080

    # Create a server instance
    server = Server(SERVER_IP, PORT)

    # Register the shutdown signal handler
    signal.signal(signal.SIGINT, server.handle_shutdown)

    # Start the server
    server.start_server()

if __name__ == "__main__":
    main()