import socket
from User import User


class Client:
    def __init__(self, server_ip, port):
        self.server_ip = server_ip
        self.port = port
        self.client_socket = None
        self.connect_to_server()

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
            self.connect_to_server()
            self.client_socket.sendall(request.encode())
            response=b""
            while True:
                # Receive a chunk of data
                chunk = self.client_socket.recv(4096)

                # Break the loop if no more data is received
                if not chunk:
                    break
                
                # Append the received chunk to the buffer
                response += chunk
            return response.decode()

        except Exception as e:
            print("An error occurred during request/response:", str(e))

    def login(self):
        rt = False
        try:
            print("Enter phone_no")
            phn = input()
            print("Enter password")
            pwd = input()
            request = "1 {} {}".format(phn,pwd)
            # self.connect_to_server()
            # self.client_socket.sendall(msg.encode())
            server_response = self.send_request(request)
            splt = server_response.split()
            
            if splt[0] == "200":
                usr = User(splt[2], splt[3], splt[4], splt[5], splt[6], splt[7], splt[1] == '1')
                rt = True
            elif splt[0] == "1000":
                print("Phone number you provided is not registered to any account. Create a new account instead")

            elif splt[0] == "1001":
                print("Password incorrect. Try again")

        except ConnectionError:
            print("Connection error. Make sure the server is running.")
        except TimeoutError:
            print("Connection timeout. Make sure the server is running.")
        except Exception as e:
            print("An error occurred during login:", str(e))
        finally:
            if not rt:
                return None
            else:
                return usr

    def withdraw(self, usr):
        try:
            acc = self.get_acc_nos_by_phone(usr.get_phone_no())
            print("Enter the amount you want to withdraw")
            amt = input()
            if acc is not None:
                withdraw_request = "3 {} {}".format(acc,amt)
                print("Withdraw request: " + withdraw_request)
                withdraw_response = self.send_request(withdraw_request)
                splt = withdraw_response.split()

                if splt[0] == "200":
                    print(amt + " withdrawn successfully")
                elif splt[0] == "1003":
                    print("Insufficient balance, failed to make withdrawal")
                elif splt[0] == "1002":
                    print("You don't have any account in our bank")

        except ConnectionError:
            print("Connection error. Make sure the server is running.")
        except TimeoutError:
            print("Connection timeout. Make sure the server is running.")
        except Exception as e:
            print("An unexpected error occurred:", str(e))

    def deposit(self, usr):
        try:
            acc = self.get_acc_nos_by_phone(usr.get_phone_no())
            print("Enter the amount you want to deposit")
            amt = input()
            if acc is not None:
                deposit_request = "4 {} {}".format(acc,amt)
                # print("deposit request: " + deposit_request)
                deposit_response = self.send_request(deposit_request)
                splt = deposit_response.split()

                if splt[0] == "200":
                    print(amt + " deposited successfully")
                elif splt[0]=="1004":
                    print("Internal database error, your money will be refunded")

        except ConnectionError:
            print("Connection error. Make sure the server is running.")
        except TimeoutError:
            print("Connection timeout. Make sure the server is running.")
        except Exception as e:
            print("An unexpected error occurred:", str(e))

    def create_account(self,usr):
        try:
            branch=self.get_branch()
            self.connect_to_server()
            print("Enter 1 for savings account or 2 for current account")
            accType=input()
            create_acc_request="6 {} {} {}".format(branch,usr.get_phone_no(),accType)
            create_response=self.send_request(create_acc_request)
            splt=create_response.split()
            if splt[0]=="200":
                print("Account created. Account number:")
                print(splt[1])
            elif splt[0]=="1004":
                print("Internal database error, failed to create acccount")
        except ConnectionError:
            print("Connection error. Make sure the server is running.")
        except TimeoutError:
            print("Connection timeout. Make sure the server is running.")
        except Exception as e:
            print("An unexpected error occurred:", str(e))
            
            
    def check_balance(self,usr):
        try:
            acc=self.get_acc_nos_by_phone(usr.get_phone_no())
            self.connect_to_server()
            bal_request="7 {}".format(acc)
            self.client_socket.sendall(bal_request.encode())
            bal_response=self.client_socket.recv(5000).decode()
            splt=bal_response.split()
            if splt[0]=="200":
                print("Available balance: "+splt[1])
            elif splt[0]=="1004":
                print("Internal database error, failed to fetch balance")
        
        
        except ConnectionError:
            print("Connection error. Make sure the server is running.")
        except TimeoutError:
            print("Connection timeout. Make sure the server is running.")
        except Exception as e:
            print("An unexpected error occurred:", str(e))
    
    def get_loan(self,usr):
        try:
            acc=self.get_acc_nos_by_phone(usr.get_phone_no())
            self.connect_to_server()
            print("Enter loan amount")
            amt=input()
            loan_request="8 {} {}".format(acc,amt)
            loan_response=self.send_request(loan_request)
            splt=loan_response.split()
            if splt[0]=="200":
                print("You have taken a loan for {} at {}% interest rate for 1 year".format(amt,splt[1]))
            elif splt[0]=="1004":
                print("Internal database error, failed to get loan")
            
        
        except ConnectionError:
            print("Connection error. Make sure the server is running.")
        except TimeoutError:
            print("Connection timeout. Make sure the server is running.")
        except Exception as e:
            print("An unexpected error ocurred:", str(e))    
            
            
            
    def get_new_card(self,usr):
        try:
            
            acc=self.get_acc_nos_by_phone(usr.get_phone_no())
            print("Enter 1 for credit card or 2 for debit card")
            cardType=input()
            if(cardType=="1"):
                cardType="C"
            else:
                cardType="D"
                
            card_request="9 {} {}".format(acc,cardType)
            card_response=self.send_request(card_request)
            splt=card_response.split()
            
            if(splt[0]=="200"):
                print("New card details:")
                print("card_no: {}".format(splt[1]))
                print("pin: {}".format(splt[2]))
                print("cvv: {}".format(splt[3]))
                print("Please change the default pin ASAP")
            elif splt[0]=="1004":
                print("Internal database error, failed to get new card")
            

            
        except ConnectionError:
            print("Connection error. Make sure the server is running.")
        except TimeoutError:
            print("Connection timeout. Make sure the server is running.")
        except Exception as e:
            print("An unexpected error ocurred:", str(e))    
            
            
    def send_money(self,usr):
        try:
            acc_send=self.get_acc_nos_by_phone(usr.get_phone_no())
            print("Select the account you want to send money to")
            acc_recv=self.get_all_accounts()
            if acc_recv==acc_send:
                print("Sender and receiver accounts must be different")
                return
            print("Enter the amount you want to send")
            amt=input()
            request="11 {} {} {}".format(acc_send,acc_recv,amt)
            response=self.send_request(request)
            splt=response.split()
            if splt[0]=="200":
                print("Money sent successfully")
            elif splt[0]=="1003":
                print("Insufficient balance in acc_no {}, failed to send money".format(acc_send))
            elif splt[0]=="1004":
                print("Internal database error, transaction failed")
        except ConnectionError:
            print("Connection error. Make sure the server is running.")
        except TimeoutError:
            print("Connection timeout. Make sure the server is running.")
        except Exception as e:
            print("An unexpected error ocurred:", str(e))
            
            
    def get_branch_address(self,usr):
        try:
            acc=self.get_acc_nos_by_phone(usr.get_phone_no())
            request="12 {}".format(acc)
            response=self.send_request(request)
            splt=response.split(",")
            if splt[0]=="200":
                print("Branch name: {}".format(splt[1]))
                print("Branch city: {}".format(splt[2]))
                print("Branch state: {}".format(splt[3]))
                print("Branch pincode: {}".format(splt[4]))
            elif splt[0]=="1004":
                print("Internal database error, failed to fetch branch details")
        except ConnectionError:
            print("Connection error. Make sure the server is running.")
        except TimeoutError:
            print("Connection timeout. Make sure the server is running.")
        except Exception as e:
            print("An unexpected error ocurred:", str(e))
            
    def get_history(self,usr):
        try:
            acc=self.get_acc_nos_by_phone(usr.get_phone_no())
            print("Enter last 1 weeks , 2 for last 1 month's and 3 for last 1 year's transactions")
            dur=input()
            request="13 {} {}".format(acc,dur)
            response = self.send_request(request)

            splt=response.split(",")
            if splt[0]=="200":
                for row in splt[1:]:
                    print(str(row))
                
            elif splt[0]=="1004":
                print("Internal database error, failed to fetch transaction history")

            
            
        except ConnectionError:
            print("Connection error. Make sure the server is running.")
        except TimeoutError:
            print("Connection timeout. Make sure the server is running.")
        except Exception as e:
            print("An unexpected error occurred:", str(e))
    # helper functions
    
    #funtion to display accounts linked to given phone no
    
    def get_acc_nos_by_phone(self,phone_no):
        try:
            request="2 "+phone_no
            print(request)
            response=self.send_request(request)
            splt=response.split()
            acc=None
            if splt[0]=="200":
                print("Select your account")
                for i in range(1,len(splt)):
                    print(str(i)+". "+splt[i])
                acc = splt[int(input())]
                
                
            elif splt[0]=="1002":
                print("No account linked to given number, try creating a new account")

            return acc
        except ConnectionError:
            print("Connection error. Make sure the server is running.")
        except TimeoutError:
            print("Connection timeout. Make sure the server is running.")
        except Exception as e:
            print("An unexpected error ocurred:", str(e))

    def get_branch(self):
        try:
            branch_request = "5"
            branch_response = self.send_request(branch_request)
            splt = branch_response.split(",")
            if splt[0] == "200":
                print("Select your branch")
                for branch_name in splt[1:]:
                    print(branch_name)
                branch = int(input())
                return branch
            else:
                return None
        except ConnectionError:
            print("Connection error. Make sure the server is running.")
        except TimeoutError:
            print("Connection timeout. Make sure the server is running.")
        except Exception as e:
            print("An unexpected error occurred:", str(e))


    def get_all_accounts(self):
        try:
            request="10"
  
            response=self.send_request(request)
            splt=response.split(",")
            i=1
            if splt[0]=="200":
                for row in splt[1:]:
                    print(str(i)+". "+row)
                    i+=1
                ind=int(input())
                lst = splt[ind].split(".")
                return lst[0]
            elif splt[0]=="1004":
                print("Internal server error,failed to fetch list of accounts")
            
        except ConnectionError:
            print("Connection error. Make sure the server is running.")
        except TimeoutError:
            print("Connection timeout. Make sure the server is running.")
        except Exception as e:
            print("An unexpected error ocurred:", str(e))
            
    # method to take pin input while updating card
    def get_pin(self):
        while True:
            password1 = input("Enter your password (4 digits): ")
            password2 = input("Re-enter your password: ")

            if password1 == password2 and len(password1) == 4 and password1.isdigit():
                print("Password set successfully!")
                return password1
            else:
                print("Passwords do not match or are not 4-digit numerical strings. Please try again.")
    
    def get_cards_by_acc(self,acc):
        try:
            request = ""
        except ConnectionError:
            print("Connection error. Make sure the server is running.")
        except TimeoutError:
            print("Connection timeout. Make sure the server is running.")
        except Exception as e:
            print("An unexpected error ocurred:", str(e))
    
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
    # client.connect_to_server()


    while(1):
        # client.connect_to_server()
        usr=client.login()
        if usr is None:
            print("Error logging in")
        else:
            if not usr.is_admin():
                while(1):
                    print("----------------------------------------")
                    print("Select your choice:")
                    print(" 0. Logout")
                    print(" 1. Create new account")
                    print(" 2. Withdraw")
                    print(" 3. Deposit")
                    print(" 4. Check account balance")
                    print(" 5. Get a loan")
                    print(" 6. Get a new card")
                    print(" 7. Send money to another account")
                    print(" 8. Get your branch address")
                    print(" 9. Get transaction history")
                    print("10. Update card pin")
                    print("11. Update profile")
                    choice = int(input())
                    if(choice==0):
                        break
                    
                    elif(choice==1):
                        client.create_account(usr)
                    elif(choice==2):
                        client.withdraw(usr)   
                    elif(choice==3):
                        client.deposit(usr)
                    elif(choice==4):
                        client.check_balance(usr)
                    elif(choice==5):
                        client.get_loan(usr)
                    elif(choice==6):
                        client.get_new_card(usr)
                    elif(choice==7):
                        client.send_money(usr)
                    elif(choice==8):
                        client.get_branch_address(usr)
                    elif(choice==9):
                        client.get_history(usr)
                    elif(choice==10):
                        pass
                    
                    elif(choice==11):
                        pass
            else:
                while(1):
                    print("----------------------------------------")
                    print("Select your choice:")
                    print("0. Logout")
                    print("1. Add new branch")
                    print("2. Update existing branch details")
                    print("3. View transactions")
                    print("4. Deactivate account")
                    print("5. Block card")
                    print("6. View loans")
                    print("7. View analytics")
                    choice = int(input())
                    if(choice==0):
                        break
                    
                    elif(choice==1):
                        pass
                    elif(choice==2):
                        pass
                    elif(choice==3):
                        pass
                    elif(choice==4):
                        pass
                    elif(choice==5):
                        pass
                    elif(choice==6):
                        pass
                    elif(choice==7):
                        pass

                
    
if __name__ == "__main__":
    main()