import socket
import subprocess
from _thread import *
import os

#test 
def Server(connected): 
    while True: 
      status="200"
      data= connected.recv(2048)
      cmd = str(data.decode("utf-8"))
      if not data:
        print("bash: End Connection!!!!!")             
        break
      elif (cmd.split()[0] == "cd"):
        os.chdir(cmd[3:])
        connected.send(status.encode("utf-8"))
        print("Change Path Successfully!!!")
      else:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=None, shell=True)
        output = process.communicate()
        print (output[0].decode("utf-8"))
        connected.send(status.encode("utf-8"))
    connected.close() 

def main(): 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    port=int(input("Enter port:"))
    s.bind((socket.gethostname(), port)) 
    s.listen(3) 
    print("Waiting for connection!!!.............")
    try:
      while True:
            try:
              connected, addr = s.accept()  
              print('Connected to :', addr[0], ':', addr[1])
              start_new_thread(Server, (connected,))
            except socket.timeout:
              pass
            except Exception as exc:
              print(str(exc))
              print("Server closing")
              s.close()
              break
    except KeyboardInterrupt:
      print("Server closing")
      s.close()
    s.close()
  
if __name__ == '__main__':
  main()