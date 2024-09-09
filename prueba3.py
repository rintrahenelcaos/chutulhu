import socket
from _thread import *
import sys

hostname = socket.gethostname()
IP_addr = socket.gethostbyname(hostname)
print(IP_addr)