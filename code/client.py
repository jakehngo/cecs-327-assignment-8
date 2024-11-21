import socket
# const value for the size of the buffer for the program
BUFFERSIZE = 1024
def main():
    while True:
        try:
 # prompt the user to enter in the ip, port, and message to send
            server_ip = input("Enter the server IP address: ")
            server_port = int(input("Enter the server port: "))
            message = input("Enter the message to send (type 'exit' to quit): ")
            # if the message is "exit" terminate our program
            if message.lower() == 'exit':
                print("Exiting client...")
                break
            # create a tcp socket
 # with allwos us to handle closing in case of exceptions for the socket
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
 # connect to the server via the ip and port provided
                client_socket.connect((server_ip, server_port))
 # send the message as an encoded buffer
                client_socket.sendall(message.encode())
 # get back the server's response and show it to the command line
                response = client_socket.recv(BUFFERSIZE)
                print("Response from server:", response.decode())
 # error handling
        except ValueError:
            print("Invalid port number. Please enter a valid number.")
        except (ConnectionRefusedError, socket.gaierror):
            print("Could not connect to the server, maybe the ip or port is wrong!")
        except Exception as e:
            print(f"An error occurred: {e}")
            
if __name__ == "__main__":
 main()