import socket

def main():
    # Input server details
    server_ip = input("Enter server IP address: ")
    port = int(input("Enter server port you want to communicate with: "))

    # Create client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, port))

    while True:
        try:
            # Get command from user
            command = input("Enter command (or type 'exit' to quit): ")
            if command.lower() == "exit":
                break

            # Send command to server
            client_socket.send(command.encode())

            # Receive response from server
            response = client_socket.recv(4096).decode()
            print(response)

        except KeyboardInterrupt:
            print("\nTerminating connection due to Ctrl+C...")
            break

    # Close socket
    client_socket.close()

if __name__ == "__main__":
    main()
