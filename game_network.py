import socket
import threading
import pickle
from pickleobj import Exchange_object

IP = socket.gethostbyname(socket.gethostname())
IP = "10.160.23.116"
PORT = 5555
ADDR = (IP, PORT)
SIZE = 40000
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"

#connected = True
recv_order = [""]





class Network:
    def __init__(self) -> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def connect(self, faction):
        try: 
            self.client.connect(ADDR) 
            print(f"[CONNECTED] Client connected to server at {IP}:{PORT}")
            self.client.sendall(faction.encode(FORMAT))
            return self.client.recv(SIZE).decode(FORMAT)
        except:
            pass
        
    def send_recv(self, cargo):
        try: 
            
                
            self.client.sendall(cargo.encode(FORMAT))
            return self.client.recv(SIZE).decode(FORMAT)
        except: pass
    
    def send_only(self, cargo):
        try:
            self.client.sendall(cargo.encode(FORMAT))
        except: pass
    
    def recieve_only(self):
        try:
            return self.client.recv(SIZE).decode(FORMAT)
        except: pass
        
    def closing(self):
        try: 
            self.client.sendall(DISCONNECT_MSG.encode(FORMAT))
            self.client.shutdown()
            self.client.close()
            exit()
            
        except:
            print("Unable to disconnect")

def main():
    net = Network()
    bacvk = net.connect("player")
    print(bacvk)
    conn = True
    msg = input(">")
    print(net.send_recv(msg))
    while conn:
        msg = input(">")
        #net.send_recv(msg)
        if msg == DISCONNECT_MSG:
            net.closing()
            conn = False
            exit()
        
        else: 
            print(net.send_recv(msg))
    exit()
        
    
    
    
if __name__ == "__main__":
    main()