import socket # Used for creating network sockets for communication.
import subprocess # Used to execute commands on the server's system.
import threading # Used for creating worker threads to handle multiple client connections concurrently
import os # Used for changing the working directory

def Server(connected):
    while True:
        data = connected.recv(2048) # Receives up to 2048 bytes of data from the client.
        cmd = str(data.decode("utf-8")) # Decodes the received data into a string (UTF-8 encoding) and stores it in the variable.
        if not data:
            print("bash: End Connection!!!!!")
            break
        elif cmd.split()[0] == "cd":
                if len(cmd.split()) == 1:  # Check for no additional arguments
                    current_dir = os.getcwd()  # Get the current working directory
                    connected.sendall(current_dir.encode("utf-8"))  # Send it back to the client
                else:
                    try:
                        os.chdir(cmd[3:])  # Attempt to change directory
                        current_dir = os.getcwd()  # Get the new working directory
                        connected.sendall(current_dir.encode("utf-8"))  # Send new directory
                    except FileNotFoundError: # use try catch in python to catch whenever the case is that there are no directory found
                        error_msg = "Directory not found.".encode("utf-8")
                        connected.sendall(error_msg)  # Send error message to client
        else:
            # process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            process = subprocess.Popen(["powershell", "-Command", cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE) # using powershell
            output, error = process.communicate()
            if error:
                output = error
            connected.sendall(output) # send the output to the client
    connected.close()


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #  Creates a TCP socket.
    port = int(input("Enter port you want the server to run on:"))
    s.bind(('0.0.0.0', port)) # Binds the socket to all available network interfaces on the specified port.
    s.listen(3) #  Starts listening for connections, with a maximum backlog of 3 pending connections.
    print("Waiting for connection!!!.............")
    try:
        while True:
            connected, addr = s.accept() # Accepts a connection, obtaining a new socket for communication and the client's address.
            print('Connected to :', addr[0], ':', addr[1]) # print out the ip of the client and the port of the client 
            # Create a new thread using threading.Thread
            thread = threading.Thread(target=Server, args=(connected,)) # Creates a new thread to handle the client
            thread.start()  # Start the thread execution
    except KeyboardInterrupt: #  Catches a keyboard interrupt (Ctrl+C).
        print("Server closing")
    finally:
        s.close()

if __name__ == '__main__':
    main()
