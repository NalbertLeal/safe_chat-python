import socket
from threading import Thread

from send import Send
from bmp_image_proccess import Bmp_image_proccess
from sdes import Sdes

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
                msg = self.cipher.Decode(msg)
                print('$ ' + msg)
            print('Finished: ', client)
            con.close()

    def is_binary_string(self, bstring):
        if len([i for i in bstring if i in ['1', '0']]) == 10:
            return True
        return False

    def run(self):
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        bmp_processor = Bmp_image_proccess()
        send = Send()
        t = Thread(target=self.wait, args=(tcp, send, bmp_processor))
        t.start()


        key = ''
        while not self.is_binary_string(key):
            key = input('write the key: ')

        self.cipher = Sdes(key)

        counter = 0
        msg = input('$ ')
        while msg != '':
            if counter == 0:
                counter += 1
                bmp_processor.write_img_message('img.BMP', 'send_img.BMP', key)
                img_key = bmp_processor.read_img('send_img.BMP')
                send.put_bytes( img_key )
            msg = self.cipher.Encode(msg)
            bmp_processor.write_img_message('img.BMP', 'send_img.BMP', msg)
            msg = bmp_processor.read_img('send_img.BMP')
            send.put_bytes( msg )
            msg = input('$ ')

        t.join()
        tcp.close()
        exit()
