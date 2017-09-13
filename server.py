import socket
from threading import Thread

from send import Send

class Server():
    def __init__(self, user="", host='127.0.0.2', port=3000):
        self.user = user
        self.host = host
        self.port = port

    def wait(self, tcp, send):
        tcp.bind( (self.host, self.port) )
        tcp.listen(1)

        while True:
            con, client = tcp.accept()
            send.con = con
            print('connected: ', client)
            while True:
                msg = con.recv(1024)
                if not msg:
                    break
                print('$ ' + str(msg, 'utf-8'))
            print('Finished: ', client)
            con.close()

    def run(self):
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        send = Send()
        t = Thread(target=self.wait, args=(tcp, send))
        t.start()

        msg = input('$ ')
        while msg != '':
            send.put( self.user + ': ' + msg )
            msg = input('$ ')

        t.join()
        tcp.close()
        exit()
