
class Send():
    def __init__(self):
        self.msg = ''
        self.new = False
        self.con = None

    def put(self, msg):
        self.msg = msg
        if self.con != None:
            self.con.send(str.encode(self.msg))

    def put_bytes(self, bytes):
        self.msg = bytes
        if self.con != None:
            self.con.send(self.msg)
