
if __name__ == '__main__':

    from rc4 import RC4
    from server import Server
    from client import Client
    import sys

    if len(sys.argv) > 1:
        username = os.argv[1]
        c = Client(username)
        c.run()
    else:
        print('>> Initiating the server')
        s = Server()
        s.run()
