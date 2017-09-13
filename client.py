from __future__ import barry_as_FLUFL
import socket
from threading import Thread

from send import Send
from bmp_image_proccess import Bmp_image_proccess

HOST = '127.0.0.1'
PORT = 5000

class Client():
    def __init__(self, user="", host='127.0.0.1', port=3000):
        self.user = user
        self.host = host
        self.port = port

    def wait(self, tcp, send, bmp_processor):
        tcp.connect( (self.host, self.port) )

        while True:
            send.con = tcp
            while True:
                msg = tcp.recv(1024)
                # print('$ ' + str(msg,'utf-8') )
                bmp_processor.write_img('img_received.BMP', msg)
                msg = bmp_processor.read_img_message('img_received.BMP')
                print('$ ' + msg)
                if not msg:
                    break

    def run(self):
        bmp_processor = Bmp_image_proccess()
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        send = Send()

        t = Thread(target=self.wait, args=(tcp, send, bmp_processor))
        t.start()

        msg = input('$ ')
        while msg != '':
            # tcp.send( str(self.user + ': ' + msg).encode() )
            bmp_processor.write_img_message('img.BMP', 'send_img.BMP', msg)
            msg = bmp_processor.read_img('send_img.BMP')
            send.put_bytes( msg )
            msg = input('$ ')
        tcp.close()
        exit()
