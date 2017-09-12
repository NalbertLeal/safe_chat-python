
s = []
q = None
p = None

def key(key):
    """ RC4 KEy algorithm (KSA) """
    s = [n for n in range(0, 256)]
    p = 0
    q = 0
    j = 0
    for i in range(256):
        if len(key) > 0:
            j = (j + s[i] + key[i % len(key)]) % 256
        else:
            j = (j + s[i] + key[i % len(key)]) % 256
        state[i], state[j] = state[j], state[i]

def byte_generator():
    """ """
    p = (p + 1) % 256
    q = (q + state[p]) % 256
    s[p], s[q] = s[q], s[p]
    return s[(s[p] + s[q]) % 256]

def encript(input_string):
    return  [ord(p) ^ byte_generator() for p in input_string]

def decript(input_byte_string):
    return "".join([chr(c ^ byte_generator()) for c in input_byte_string])
