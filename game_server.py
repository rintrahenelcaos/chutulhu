import socket
import threading
import pickle
from pickleobj import Exchange_object
import sys


IP = socket.gethostbyname(socket.gethostname())
PORT = 5555
ADDR = (IP, PORT)
SIZE = 40000
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"

clients = []
broadcast_msg = ""
data = ["str", "str"]
data = [Exchange_object("NONE"), Exchange_object("NONE")]
factions_code = ["NONE","NONE"]

def broadcast(msg, player):
    try:
        for ind_client in clients:
            if clients.index(ind_client) != player:
                msg = msg + str(clients.index(ind_client))
                ind_client.send(msg.encode(FORMAT))
                
    except Exception as error:
            print('Error :',error)
        
def handle_client(conn, addr, player):
    print(f"[NEW CONNECTION] {addr} connected.")
    faction = conn.recv(SIZE).decode(FORMAT)
    print(faction)
    factions_code[player] = faction

    connected = True
    while connected:
        try:
            cargo = pickle.loads(conn.recv(SIZE))
            #msg = conn.recv(SIZE).decode(FORMAT)

            data[player] = cargo
            #data[player] = msg
            """if msg == DISCONNECT_MSG:
                #conn.shutdown()
                connected = False"""
            if cargo== DISCONNECT_MSG:
                print("player disconnected")
                connected = False
                
            print(f"[{addr}] {cargo}")
            #print(f"[{addr}] {msg}")
            for dat in range(len(data)):
                if dat == player:
                    data[dat] = cargo
                    #data[dat] = msg
            for dat in range(len(data)):
                if dat != player:
                    conn.send(pickle.dumps(data[dat]))
                    #conn.send((data[dat]).encode(FORMAT))
            #msg = f"Msg received: {msg}"
            #msg_server = f"recieved: {msg}"
            
            """if msg != "":
                pass
                broadcast(msg, player)"""
        except Exception as error:
            #print('Error :',error)        
            pass
    #conn.shutdown()
    conn.close()
    clients.remove(conn)
    exit() 

def main():
    
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind(ADDR)
    except Exception as error:
        print('Error :',error)
    server.listen(2)
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")

    while True:
        conn, addr = server.accept()
        clients.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr, clients.index(conn)))
        thread.start()
        
       
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
        print("clients lenght: ", len(clients))


        

if __name__ == "__main__":
    main()