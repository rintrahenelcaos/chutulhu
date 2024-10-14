import socket
import threading
import pickle
from pickleobj import Exchange_object

IP = socket.gethostbyname(socket.gethostname())
IP = "192.168.1.2"
PORT = 5555
ADDR = (IP, PORT)
SIZE = 40000
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"

connected = True



def listening(client):
    while connected:
        msg = client.recv(SIZE).decode(FORMAT)
        if msg != "":
            print(f"[BROADCASTED]: {msg}")
        return msg


def main():
    global connected
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print(f"[CONNECTED] Client connected to server at {IP}:{PORT}")

    #connected = True
    thread_listen = threading.Thread(target =listening, args=(client,) )
    thread_listen.start()
    while connected:
        
        msg = input("> ")
        

        client.send(msg.encode(FORMAT))

        if msg == DISCONNECT_MSG:
            connected = False
            exit()
        """else:
            msgr = client.recv(SIZE).decode(FORMAT)
            print(f"[SERVER] {msgr}")"""
        """broadcasted = client.recv(SIZE).decode(FORMAT)
        print(f"[BROADCASTED] {broadcasted}")"""

class Network:
    def __init__(self) -> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def connect(self, faction):
        self.client.connect(ADDR) 
        print(f"[CONNECTED] Client connected to server at {IP}:{PORT}")
        self.client.send(faction.encode(FORMAT))
    
    def send(self, cargo):
        try:
            self.client.send(pickle.dumps(cargo))
            #self.client.send(msg.encode(FORMAT))
            data = pickle.loads(self.client.recv(SIZE))
            #rec_msg = self.client.recv(SIZE).decode(FORMAT)
            print("in the network: ", data)
            
            """if msg == DISCONNECT_MSG:
                self.client.close()"""
            return data
        except socket.error as e:
            print(e)
            

class Network:
    def __init__(self) -> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def connect(self, faction):
        self.client.connect(ADDR) 
        print(f"[CONNECTED] Client connected to server at {IP}:{PORT}")
        self.client.send(faction.encode(FORMAT))
        thread_listen = threading.Thread(target =listening, args=(self.client,) )
        thread_listen.start()
    
    def send(self, cargo):
        try:
            self.client.send(cargo.encode(FORMAT))
            #self.client.send(msg.encode(FORMAT))
            data = pickle.loads(self.client.recv(SIZE))
            #rec_msg = self.client.recv(SIZE).decode(FORMAT)
            print("in the network: ", data)
            
            """if msg == DISCONNECT_MSG:
                self.client.close()"""
            return data
        except socket.error as e:
            print(e)
            
def listening(client):
    while connected:
        msg = client.recv(SIZE).decode(FORMAT)
        if msg != "":
            print(f"[BROADCASTED]: {msg}")
            

if __name__ == "__main__":
    main()