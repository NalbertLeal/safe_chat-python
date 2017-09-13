from __future__ import barry_as_FLUFL
import socket
from threading import Thread

from send import Send

HOST = '127.0.0.1'
PORT = 5000

class Client():
    def __init__(self, user="", host='127.0.0.1', port=3000):
        self.user = user
        self.host = host
        self.port = port

    def wait(self, tcp, send):
        tcp.connect( (self.host, self.port) )

        while True:
            send.con = tcp
            while True:
                msg = tcp.recv(1024)
                print('$ ' + str(msg,'utf-8') )
                if not msg:
                    break

    def run(self):
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        send = Send()

        t = Thread(target=self.wait, args=(tcp, send))
        t.start()

        msg = input('$ ')
        while msg != '':
            # tcp.send( str(self.user + ': ' + msg).encode() )
            send.put( self.user + ': ' + msg )
            msg = input('$ ')
        tcp.close()
        exit()
