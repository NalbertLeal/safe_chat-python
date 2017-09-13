
class Send():
    def __init__(self):
        self.msg = ''
        self.new = True
        self.con = None

    def put(self, msg):
        self.msg = msg
        if self.con != None:
            self.con.send(str.encode(self.msg))
