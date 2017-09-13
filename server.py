import socket

class Server():
    def __init__(self, host='127.0.0.1', port=3000):
        self.host = host
        self.port = port

    def run(self,):
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp.bind( (self.host, self.port) )
        tcp.listen(1)

        while True:
            con, client = tcp.accept()
            print('connected: ', client)
            while True:
                msg = con.recv(1024)
                if not msg:
                    break
                print(client, msg)
            print('Finished: ', client)
            con.close()
