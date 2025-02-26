from socket import socket , AF_INET , SOCK_STREAM  #IT is use for the main communication part
from threading import Thread #Use for concurent thread here 
IP_ADD = "10.160.4.213" #It has to be string
PORT = 5555

LIMIT = 5
STORAGE =[]


def listen_client(info , name):
    while True:
        try:
            msg = info.recv(2048).decode('UTF-8')
            if msg !='':
                data = name+':'+msg
                send_msg_all(data)
            else:
                print(f'[SERVER] :- message is not recived {name}')
        except Exception as error:
            print('Error :',error)

def send_msg(info ,msg):
    info.sendall(msg.encode())

def send_msg_all(info):
    for data in STORAGE:
        send_msg(data[1] , info)            

def client_server(info):
    while True:
        try:
            name = info.recv(2048).decode('UTF-8')
            if name !='':
                STORAGE.append((name , info ,))
                data = name+' : '+'is connected to the server'
                send_msg_all(data)
            else:
                print('Name is not recived here ')
        except Exception as error:
            print('Error :',error)
        Thread(target=listen_client , args=((info , name))).start()

def main(): #Server crearing here 
    server = socket(AF_INET, SOCK_STREAM)
    try:
        server.bind((IP_ADD , PORT))
        print('[SERVER] Connection searching for the user')
    except Exception as error:
        print('Error :',error)
    server.listen(LIMIT)
    while True:
        path , add = server.accept()
        print(f'[SERVER] Connection with user is established at server {add[0]} {add[1]}')
        Thread(target=client_server , args=(path,)).start() 


if __name__ == '__main__':
    main()