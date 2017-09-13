
class RC4():
    def __init__(self):
        self.s = []
        self.q = None
        self.p = None

    def key(self, key):
        """ RC4 KEy algorithm (KSA) """
        self.s = [n for n in range(0, 256)]
        self.p = 0
        self.q = 0
        j = 0
        for i in range(256):
            if len(key) > 0:
                j = (j + self.s[i] + int(key[i % len(key)]) ) % 256
            else:
                j = (j + self.s[i] + int(key[i % len(key)]) ) % 256
            self.s[i], self.s[j] = self.s[j], self.s[i]

    def byte_generator(self):
        """ """
        self.p = (self.p + 1) % 256
        self.q = (self.q + self.s[self.p]) % 256
        self.s[self.p], self.s[self.q] = self.s[self.q], self.s[self.p]
        return self.s[(self.s[self.p] + self.s[self.q]) % 256]

    def encript(self, input_string):
        return  [ord(i) ^ self.byte_generator() for i in input_string]

    def decript(self, input_byte_string):
        return "".join([chr(i ^ self.byte_generator()) for i in input_byte_string])
