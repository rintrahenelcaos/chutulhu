import socket
import threading
import pprint
#import wikipedia

IP = socket.gethostbyname(socket.gethostname())
PORT = 5566
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"

clients = []
broadcast_msg = ""
log = []

def broadcast(msg, conn):
    try:
        for ind_client in clients:
            if conn != ind_client:
                ind_client.send(msg.encode(FORMAT))
        log.append([msg]) 
        pprint.pp(log)       
    except Exception as error:
            print('Error :',error)
    
        
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        try:
            msg = conn.recv(SIZE).decode(FORMAT)

            if msg == DISCONNECT_MSG:
                connected = False
                

            print(f"[{conn}] {msg}")

            # msg = f"Msg received: {msg}"
            #msg_server = f"recieved: {msg}"
            #conn.send(msg_server.encode(FORMAT))
            
            if msg:

                broadcast(str(conn)+msg, conn)
        except Exception as error:
            print('Error :',error)        

    conn.close()

def main():
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind(ADDR)
    except Exception as error:
        print('Error :',error)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")

    while True:
        conn, addr = server.accept()
        clients.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        
       
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


        

if __name__ == "__main__":
    main()