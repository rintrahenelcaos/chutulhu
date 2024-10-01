# server.py
import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 12345))
server.listen()
clients = []

hostname = socket.gethostname()
IP_address = socket.gethostbyname(hostname)
PORT = 5555

def main():
    
    print("Starting")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP_address, PORT))
    
    server.listen()
    print(f"[LISTENING] Server is listening on {IP_address}:{PORT}")

while True:
    conn, addr = server.accept()
    
def client_handler(connection):
    while True:
        message = connection.recv(1024)
        broadcast_message(message)

def broadcast_message(message):
    for client in clients:
        client.send(message)



while True:
    client_connection, client_address = server.accept()
    clients.append(client_connection)
    thread = threading.Thread(target=client_handler, args=(client_connection,))
    thread.start()