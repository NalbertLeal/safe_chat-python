import socket
from threading import Thread

from send import Send
from bmp_image_proccess import Bmp_image_proccess

class Server():
    def __init__(self, user="", host='127.0.0.2', port=3000):
        self.user = user
        self.host = host
        self.port = port

    def wait(self, tcp, send, bmp_processor):
        tcp.bind( (self.host, self.port) )
        tcp.listen(1)

        while True:
            con, client = tcp.accept()
            send.con = con
            print('connected: ', client)
            while True:
                msg = con.recv(1024 * 1024 * 10)
                if not msg:
                    break
                # print('$ ' + str(msg, 'utf-8'))
                bmp_processor.write_img('img_received.BMP', msg)
                msg = bmp_processor.read_img_message('img_received.BMP')
                print('$ ' + msg)
            print('Finished: ', client)
            con.close()

    def run(self):
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        bmp_processor = Bmp_image_proccess()
        send = Send()
        t = Thread(target=self.wait, args=(tcp, send, bmp_processor))
        t.start()

        msg = input('$ ')
        while msg != '':
            bmp_processor.write_img_message('img.BMP', 'send_img.BMP', msg)
            msg = bmp_processor.read_img('send_img.BMP')
            send.put_bytes( msg )
            msg = input('$ ')

        t.join()
        tcp.close()
        exit()
