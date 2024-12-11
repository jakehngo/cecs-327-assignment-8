import socket

# const value for the size of the buffer for the program
BUFFERSIZE = 1024

def display_menu():
    print("\nSelect a query to send:")
    print("1. Average moisture in the fridge (in past 3 hours)")
    print("2. Average water consumption per washing cycle in smart dishwasher")
    print("3. Device with the highest electricity consumption (fridge 1, fridge 2, dishwasher)")
    print("Type 'exit' to quit.")

def get_query():
    display_menu()
    choice = input("Enter your choice: ")
    if choice == '1':
        return "average_moisture"
    elif choice == '2':
        return "average_water_consumption"
    elif choice == '3':
        return "highest_energy_device"
    elif choice.lower() == 'exit':
        return None
    else:
        print("Sorry, this query cannot be processed. Please try one of the following:")
        return get_query()

def main():
    try:
        # prompt the user to enter in the ip, port, and message to send
        server_ip = input("Enter the server IP address: ")
        if not server_ip:
            server_ip = "localhost"
        server_port = int(input("Enter the server port: "))
        
        # create a tcp socket
        # with allwos us to handle closing in case of exceptions for the socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            # connect to the server via the ip and port provided
            client_socket.connect((server_ip, server_port))
            
            while True:
                # if the message is "exit" terminate our program
                message = get_query()
                if message is None:
                    print("Exiting client...")
                    break
            
                print(f"Sending query to server: {message}")
                # send the message as an encoded buffer
                client_socket.sendall(message.encode())
                # get back the server's response and show it to the command line
                response = client_socket.recv(BUFFERSIZE)
                print("\nResponse from server:", response.decode())
    
    # error handling
    except ValueError:
        print("Invalid port number. Please enter a valid number.")
    except (ConnectionRefusedError, socket.gaierror):
        print("Could not connect to the server, maybe the ip or port is wrong!")
    except Exception as e:
        print(f"An error occurred: {e}")
            
if __name__ == "__main__":
 main()