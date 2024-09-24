import socket
from _thread import *
from player_turn_module import Player_Object
import pickle


hostname = socket.gethostname()
IP_addr = socket.gethostbyname(hostname)
server = IP_addr
server = "192.168.1.2"
port = 5555

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.bind((server, port))
except socket.error as e:
    str(e)

sock.listen(2)
print("Waiting for a connection, Server Started")


players = [Player_Object("INVESTIGATORS", test= True), Player_Object("SERPENT_PEOPLE", test= True)]

def threaded_client(conn, player):
    conn.send(pickle.dumps(players[player]))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            players[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]

                print("Received: ", data)
                print("Sending : ", reply)

            conn.sendall(pickle.dumps(reply))
        except:
            break

    print("Lost connection")
    conn.close()

currentPlayer = 0
while True:
    conn, addr = sock.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1