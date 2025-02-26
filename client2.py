from socket import socket, SOCK_STREAM , AF_INET
from threading import Thread

IP_ADD = "10.160.4.213" #It has to be string
PORT = 5555

def listen_to_msg(client):
    while 1:
        msg = client.recv(2048).decode('UTF-8')
        if msg != ' ':
            username = msg.split(':')[0]
            content = msg.split(':')[1]
            print(f'[{username}] :- {content}')
        else:
            print('[SERVER] :-  msg is not recived from the server ')

def send_msg_to_server(client):
    while 1:
        message = input('Message : ')
        if message != '':
            client.sendall(message.encode())
        else:
            print('Print the message is not recived from the user')

def communicate_to_server(client):
    username = input("Enter username here :- ")
    if username != ' ':
        client.sendall(username.encode())
    else:
        print('[SERVER] :- username is not recived from the server ')
    Thread(target=listen_to_msg , args=(client,)).start()
    send_msg_to_server(client)

def main():
    server = socket(AF_INET , SOCK_STREAM)
    try:
        server.connect((IP_ADD , PORT))
    except:
        print(f'[SERVER] :- Connection is not properly estabilished pls check {IP_ADD} and {PORT}')
    communicate_to_server(server)

if __name__ == '__main__':
    main()