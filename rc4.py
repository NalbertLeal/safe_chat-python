
class RC4():

    def __init__(self, k):
        key = []
        K = []
        self.PT = []
        self.S = []
        self.TempS = []

        #passando a key de string de binarios para uma lista de binarios
        for i in range(0, len(k)):
            key.append(int(k[i]))

        T = [] #temp, auxiliar
        #Inicializando S e T (state e temp)
        for i in range(0, 256):
            #S de 0 ate 255
            self.S.append(i)
            #T com os elementos da chave, com repeticao ou não(este apenas para o caso da chave ter tamanho 256)
            T.append(key[i%len(key)])

        j = 0
        #Permutação inicial em S
        for i in range(0, 256):
            j = (j + self.S[i] + T[i])%256
            #swap de duas posicoes
            self.S[i], self.S[j] = self.S[j], self.S[i]
    
    def code(self, message):

        i = 0
        j = 0
        K = ''
        TempS = self.S[:]
        for char in message:
            i = (i + 1)%256
            j = (j + self.S[i])%256
            #swap de duas posicoes
            TempS[i], TempS[j] = TempS[j], TempS[i]

            t = (TempS[i]+TempS[j])%256
            k = TempS[t]
            #K resultando possui a mensagem encriptada em string
            K = K + ( chr(ord(char) ^ k) )
        return K