from __future__ import barry_as_FLUFL
import socket
from threading import Thread

from send import Send
from bmp_image_proccess import Bmp_image_proccess
from sdes import Sdes

HOST = '127.0.0.1'
PORT = 5000

class Client():
    def __init__(self, user="", host='127.0.0.1', port=3000):
        self.user = user
        self.host = host
        self.port = port
        self.cipher = None

    def wait(self, tcp, send, bmp_processor, key):
        tcp.connect( (self.host, self.port) )

        self.cipher = Sdes(key)

        while True:
            send.con = tcp
            while True:
                msg = tcp.recv(1024 * 1024 * 10)
                # print('$ ' + str(msg,'utf-8') )
                bmp_processor.write_img('img_received.BMP', msg)
                msg = bmp_processor.read_img_message('img_received.BMP')
                msg = self.cipher.Decode(msg)
                print('$ ' + msg)
                if not msg:
                    break

    def run(self):
        bmp_processor = Bmp_image_proccess()
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        send = Send()

        # connect
        tcp.connect( (self.host, self.port) )

        # get key
        key = tcp.recv(1024 * 1024 * 10)
        bmp_processor.write_img('img_received.BMP', key)
        key = bmp_processor.read_img_message('img_received.BMP')
        self.cipher = Sdes(key)

        # restart conection
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        t = Thread(target=self.wait, args=(tcp, send, bmp_processor, key))
        t.start()

        msg = input('$ ')
        while msg != '':
            msg = self.cipher.Encode(msg)
            bmp_processor.write_img_message('img.BMP', 'send_img.BMP', msg)
            msg = bmp_processor.read_img('send_img.BMP')
            send.put_bytes( msg )
            msg = input('$ ')
        tcp.close()
        exit()
