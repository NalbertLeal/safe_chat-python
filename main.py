
if __name__ == '__main__':

    from rc4 import RC4
    from server import Server
    from client import Client
    import sys

    if len(sys.argv) == 3:
        print('user: ' + sys.argv[1], ', host: ' + sys.argv[2])
        c = Client(user=sys.argv[1], host=sys.argv[2])
        c.run()
    elif len(sys.argv) == 2:
        print('>>> Initiating the server')
        s = Server(user=sys.argv[1])
        s.run()
    else:
        print(""">>> Must pass the username (client and server) and client need\n
a second parameter, the server IP """)
