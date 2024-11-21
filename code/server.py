import socket
# const value for the size of the buffer for the program
BUFFERSIZE = 1024
def main():
 # get the port number from the user
    port = int(input("Please enter a port number: "))
 # create a tcp socket
 # using the with makes it so that it takes care of closing and etc.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
 # listen in the port provided by the user
        server_socket.bind(("", port))
        server_socket.listen(5) # allows for 5 connections
 # confirm that the server is listening on that port
        print(f"Server is listening")
        while True:
 # accepts a connection with a client
            client_socket, client_address = server_socket.accept()
 # with handles closing and errors for client socket
            with client_socket:
                print(f"Connected to {client_address}")
                while True:
 # gets buffer data from the client
                    data = client_socket.recv(BUFFERSIZE)

 # if there is nothing we failed and break
                    if not data:
                        print(f"Connection with {client_address} closed.")
                        break

 # comfirms that we receive the message
 # decode the buffer and print that received message
                    print(f"Received from {client_address}: {data.decode()}")
 # converts the message to uppercase
                    response = data.decode().upper()
 # send that uppercase response back to the client
                    client_socket.sendall(response.encode())
if __name__ == "__main__":
 main()