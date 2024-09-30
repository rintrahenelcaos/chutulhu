import socket

HOST = "10.160.4.213"
PORT = 65432

def run_client(server_ip, server_port):
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    client.connect((server_ip, server_port))
    
    while True:
        
        msg = input("Enter Message: ")
        client.send(msg.encode("utf-8")[:1024])
        
        response = client.recv(1024)
        response = response.decode("utf-8")
        
        if response == "closed":
            break
    
        print(f"Received: {response}")
        
    client.close()
    print("Connection ended")
    
    


run_client(HOST, PORT)