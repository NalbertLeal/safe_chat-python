
if __name__ == '__main__':

from rc4 import RC4
from server import Server
from client import Client
from os import args

if len(args) > 1:
    username = args[1]
    c = Client(username)
    c.run()
else:
    s = Server()
    s.run()
