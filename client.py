import socket

class Client:
    def __init__(self, server_ip, port):
        self.server_ip = server_ip
        self.port = port
        self.client_socket = None

    def connect_to_server(self):
        try:
            # Create a socket object
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Connect to the server
            self.client_socket.connect((self.server_ip, self.port))
            print("Connected to the server")

        except ConnectionRefusedError:
            print("Connection refused. Make sure the server is running.")
            self.client_socket.close()

        except Exception as e:
            print("An error occurred during connection:", str(e))
            self.client_socket.close()

    def send_request(self, request):
        try:
            # Send request to the server
            self.client_socket.send(request.encode())

            # Receive and print the server response
            server_response = self.client_socket.recv(2000).decode()
            print("Server response:", server_response)

        except Exception as e:
            print("An error occurred during request/response:", str(e))

    def close_connection(self):
        if self.client_socket:
            # Close the client socket
            self.client_socket.close()
            print("Connection closed")

def main():
    SERVER_IP = '127.0.0.1'
    PORT = 8080

    # Create a client instance
    client = Client(SERVER_IP, PORT)

    # Connect to the server
    client.connect_to_server()

    # Send a request to the server
    request = "Client request"
    client.send_request(request)

    # Close the connection
    client.close_connection()

if __name__ == "__main__":
    main()
