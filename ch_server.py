import socket

hostname = socket.gethostname()
print(hostname)
IP_host = socket.gethostbyname(hostname)
print(IP_host)

port = 5555

