from __future__ import barry_as_FLUFL
import socket

HOST = '127.0.0.1'
PORT = 5000

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST, PORT)
tcp.connect(dest)
print('Para sair use CTRL+X\n')
msg = input()
while msg != '':
    tcp.send(msg.encode())
    msg = input()
tcp.close()
