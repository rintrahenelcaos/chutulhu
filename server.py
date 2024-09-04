import socket
from _thread import *
import sys

hostname = socket.gethostname()
IP_addr = socket.gethostbyname(hostname)
server = "10.160.4.213"
port = 5555

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.bind((server, port))

except socket.error as error:
    str(error)
    
sock.listen(2)
print("Waitng for connection")

def client(conn):
    
    reply = ""
    while True:
        try: 
            data = conn.recv(2048)
            reply = data.decode("utf-8")
            
            if not data: 
                print("disconected")
                break
            else: 
                print("received: ", reply)
                print("sending: ", reply)
            
            conn.sendall(str.encode(reply))
        
        except: 
            break

while True:
    conn, addr = sock.accept()
    print("connected to: ", addr)
    
    start_new_thread(client, (conn,)) 
