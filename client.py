import socket
from User import *

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


    def login(self):
        print("Enter phone_no")
        phn = input()
        print("Enter password")
        pwd = input()
        msg="1 " + phn + " " + pwd
        self.client_socket.send(msg.encode())
        server_response = self.client_socket.recv(5000).decode()
        splt=server_response.split()
        if(splt[0]=="200"):
            usr=User(0,0,0,0,0,0,0)
            isAdmin=False
            if(splt[1]=='1'):
                isAdmin=True
                print("Admin login successful")
                usr=Admin(0,0,0,0,0,0)
            else:
                print("Customer login successful")
                usr=Customer(0,0,0,0,0,0)
            if(isAdmin):
                usr.set_is_admin(True)
            else:
                usr.set_is_admin(False)
            
            usr.set_fname(splt[2])
            usr.set_mname(splt[3])
            usr.set_ltname(splt[4])
            usr.set_phone_no(splt[5])
            usr.set_encrypted_pass(splt[6])
            usr.set_dob(splt[7])
            
            return usr
            
        elif(splt[0]=="1000"):
            print("Phone number you provided is not registered to any account. Create new account instead")
            return None
        
        elif(splt[0]=="1001"):
            print("Password incorrect. Try again")
            
        


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

    try:
        # Send a request to the server
        # request = "Client request"
        # client.send_request(request)
        usr=client.login()
        
        usr.run()
    
    except KeyboardInterrupt:
        # Close the connection on Ctrl+C
        client.close_connection()
        print("Connection closed due to KeyboardInterrupt")

if __name__ == "__main__":
    main()
