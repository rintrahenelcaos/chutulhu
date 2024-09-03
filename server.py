import socket
import _thread
import sys

server = ""
port = 5555

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.bind((server, port))

except socket.error as error:
    str(error)