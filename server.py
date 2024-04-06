import socket # Used for creating network sockets for communication.
import subprocess # Used to execute commands on the server's system.
import threading # Used for creating worker threads to handle multiple client connections concurrently
import os # Used for changing the working directory

def Server(connected):
    while True:
        # status = "200"
        data = connected.recv(2048)
        cmd = str(data.decode("utf-8"))
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
                    except FileNotFoundError:
                        error_msg = "Directory not found.".encode("utf-8")
                        connected.sendall(error_msg)  # Send error message to client
                    # connected.sendall(status.encode("utf-8"))
                    # print("Change Path Successfully!!!")
        elif cmd.split()[0] == "pwd":
                current_dir = os.getcwd()  # Get the current working directory
                connected.sendall(current_dir.encode("utf-8"))  # Send it back to the client
        else:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            output, error = process.communicate()
            if error:
                output = error
            connected.sendall(output)
    connected.close()


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = int(input("Enter port you want the server to run on:"))
    s.bind(('0.0.0.0', port))
    s.listen(3)
    print("Waiting for connection!!!.............")
    try:
        while True:
            connected, addr = s.accept()
            print('Connected to :', addr[0], ':', addr[1]) # print out the ip of the client and the port of the client 
            # Create a new thread using threading.Thread
            thread = threading.Thread(target=Server, args=(connected,))
            thread.start()  # Start the thread execution
    except KeyboardInterrupt:
        print("Server closing")
    finally:
        s.close()

if __name__ == '__main__':
    main()
