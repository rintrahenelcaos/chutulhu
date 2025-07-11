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
data = ["NONE","NONE"]
#data = [Exchange_object("NONE"), Exchange_object("NONE")]
factions_code = ["NONE","NONE"]

pre_game_confirmation = ["NONE", "NONE"]
in_course_confirmation = ["NONE", "NONE"]

separated_game_logs = [[]]

def broadcast(msg, player):
    try:
        for ind_client in clients:
            if clients.index(ind_client) != player:
                #msg = msg + str(clients.index(ind_client))
                ind_client.sendall(msg.encode(FORMAT))
                
    except Exception as error:
            print('Error :',error)
        
def handle_client(conn, addr, player):
    print(f"[NEW CONNECTION] {addr} connected.")
    faction = conn.recv(SIZE).decode(FORMAT)
    print(faction)
    data[player] = faction
    for cl in range(len(data)):
        if cl != player:
            conn.sendall(data[cl].encode(FORMAT))

    connected = True
    enemy_on_line = False
    while connected:
        try:
            
            cargo = conn.recv(SIZE).decode(FORMAT)
            
            #data[player] = cargo
            
            
            
            if cargo == DISCONNECT_MSG:
                
                print("player disconnected")
                connected = False
            #elif cargo.split("]", 1)[0] == "BATCH" :
            #    pre_game_confirmation[player] = cargo
            #    print("IN SERVER ======> ",pre_game_confirmation)
            #    if pre_game_confirmation[0] != "NONE" and pre_game_confirmation[1] != "NONE":
            #        for dat in range(len(pre_game_confirmation)):
            #            if dat != player:
            #        
            #                conn.sendall((pre_game_confirmation[dat]).encode(FORMAT))    
            #        pre_game_confirmation = ["NONE", "NONE"]
            #    else: 
            #        conn.sendall(("NONE").encode(FORMAT))  
            else:
                #if data[player] != cargo:
                data[player] = cargo
                #for dat in range(len(data)):
                #    if dat == player:
                #        data[dat] = cargo
                    
           
                for dat in range(len(data)):
                    if dat != player:
                    
                        conn.sendall((data[dat]).encode(FORMAT))
                    #if data[dat] != "NONE":   # prevent repeated msg, dissable due to rapid fire msg
                        #print("=====> ON SERVER: ", data)
                        #data[dat] = "NONE"
                    #    
                    #    data[dat] = ""
                
                    
            
                            
            #print(f"[{addr}] {cargo}")
            
            
            
        except Exception as error:
                 
            pass
    
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