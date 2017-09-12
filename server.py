import socket

HOST = ''
PORT = 5000
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (HOST, PORT)
tcp.bind(orig)
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
