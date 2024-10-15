import socket
import threading
from pickleobj import Exchange_object
import pickle


IP = socket.gethostbyname(socket.gethostname())
IP = "192.168.1.2"
PORT = 5566
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"

connected = True

EXCHANGE = Exchange_object("NONE")

def listening(client):
    while connected:
        msg = client.recv(SIZE).decode(FORMAT)
        if msg != "":
            print(f"[BROADCASTED]: {msg}")


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
        if msg == "pickle":
            client.send(pickle.dumps(EXCHANGE))
        else:
            client.send(msg.encode(FORMAT))

        if msg == DISCONNECT_MSG:
            connected = False
            exit()
        """else:
            msgr = client.recv(SIZE).decode(FORMAT)
            print(f"[SERVER] {msgr}")"""
        """broadcasted = client.recv(SIZE).decode(FORMAT)
        print(f"[BROADCASTED] {broadcasted}")"""

if __name__ == "__main__":
    main()