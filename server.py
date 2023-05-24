import socket
import threading
import signal
import sys

class Server:
    def __init__(self, server_ip, port):
        self.server_ip = server_ip
        self.port = port
        self.server_socket = None
        self.is_running = True

    def handle_client(self, client_socket, client_address):
        try:
            # Receive data from the client
            client_message = client_socket.recv(2000).decode()
            print("Received message from client:", client_message)

            # Process the client request
            response = "Server response"
            client_socket.send(response.encode())

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
