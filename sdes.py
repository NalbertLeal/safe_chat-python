import binascii

pot2 = [512, 256, 128, 64, 32, 16, 8, 4, 2, 1]
p10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
p8 = [6, 3, 7, 4, 8, 5, 10, 9]
ep = [4, 1, 2, 3, 2, 3, 4, 1]
p4 = [2, 4, 3, 1]
ls1 = [2, 3, 4, 5, 1, 7, 8, 9, 10, 6]
ls2 = [3, 4, 5, 1, 2, 8, 9, 10, 6, 7]
sw = [5, 6, 7, 8, 1, 2, 3, 4]
tableS0 = [[1, 0, 3, 2], [3, 2, 1, 0], [0, 2, 1, 3], [3, 1, 3, 2]]
tableS1 = [[1, 1, 2, 3], [2, 0, 1, 3], [3, 0, 1, 0], [2, 1, 0, 3]]

class des():

	def __init__(self, key):

		self.k10 = key
		self.k1p8 = 0
		self.k2p8 = 0

		self.sdesK1K2()

	def Encode(self, message):
		encoded = ''
		for i in range(0, len(message)):
			#muda o valor do char para uma string com os valores binarios dele, trazendo formatado em 8 bits
			inBin = charToBinaryStringFormat(message[i])
			print(inBin)
			#fk ocorre uma vez com a primeira chave
			ip = self.encodeFK(inBin, self.k1p8)
			#SW switch transposicao do resultado de fK, trocando os primeiros 4 bits com os ultimos 4 bits
			#ipa = permutation(sw, ip)
			ip = permutation(sw, ip)
			#fk ocorre uma vez com a segunda chave
			ip1 = self.encodeFK(ip, self.k2p8)
			#print(inBin, "=>>", ip1)
			#print(binaryStringToChar(inBin), "=>>", binaryStringToChar(ip1))
			#print(ip1, "=", charToBinaryStringFormat(binaryStringToChar(ip1)), "/char:", binaryStringToChar(ip1))
			encoded = encoded + ip1 #binaryStringToChar(ip1)

		return encoded

	def Decode(self, message):
		decoded = ''
		j = 0
		for i in range(0, len(message)):
			#pega de 8 em 8 bits da mensagem
			inBin = message[j : j+8]
			#processo de decriptacao ocorre como na encriptação, apenas a ordem das chaves muda
			#fk ocorre uma vez com a primeira chave
			ip = self.encodeFK(inBin, self.k2p8)
			#SW switch transposicao do resultado de fK, trocando os primeiros 4 bits com os ultimos 4 bits
			ip = permutation(sw, ip)
			#fk ocorre uma vez com a segunda chave
			ip1 = self.encodeFK(ip, self.k1p8)
			#converte em char e une a mensagem até ela se completar
			decoded = decoded + binaryStringToChar(ip1)

			#verifica se chegou ao fim da mensagem
			j = j + 8
			if j==len(message):
				break

		return decoded

	def encodeFK(self, message, key):
		######################## manipulacao de tipos #########################
		#muda o valor do char para uma string com os valores binarios dele, já vem formatado em 8 bits
		#x = charToBinaryStringFormat(message)
		#print("char: ", message, " bin: ", x)

		########################### encriptacao ###############################
		#expansão da segunda metade dos 8-bits do texto plano com o vetor ep
		rightBits = permutation(ep, message[4:])
		#xor (ou exclusivo) da ultima expansão com a primeira chave
		rightBits = xor(rightBits, key, 8)
		#s0 e s1, com a primeira e segunda metade do resultado
		rightBits = s0s1( rightBits[:4], rightBits[4:])
		#permutacao com p4
		rightBits = permutation(p4, rightBits)
		#xor dos 4 bits modificados(rightBits, resultado do p4) com os 4 bits da esquerda
		rightBits = xor(rightBits, message[:4], 4)
		#os 4 bits a esquerda modificados(rightBits) vão para o inicio, e os 4 bits da direita da mensagem inicial para o final
		#SW switch transposicao
		cipher = rightBits + message[4:]
		#print("cifra ", cipher)

		return cipher

	def sdesK1K2(self):

		#gera uma string de binario correspondente ao valor decimal passado
		self.k10 = decimalToBinaryString(self.k10)

		#geração de k2
		#Permutacao inicial de 10 (p10)
		tempk1 = permutation(p10, self.k10)
		#LS-1 da primeira e segunda metade, posicoes finais de cada elemento ja definidos na constante ls1
		tempk1 = permutation(ls1, tempk1)
		#permutacao SW (p8) do resultado
		self.k1p8 = permutation(p8, tempk1)

		#geração de k2
		#LS-2 do resultado de LS-1
		tempk2 = permutation(ls2, tempk1)
		#permutacao SW (p8) do resultado
		self.k2p8 = permutation(p8, tempk2)
		#print("k ", self.k10)
		#print("k1 ", self.k1p8)
		#print("k2 ",self.k2p8)

#faz a permutacao da nova ordem que ficará o novo dado a ordenar, com o dado a ser manipulado(toOrder)
def permutation(order, toOrder):
	ordered = ''
	for i in range(len(order)):
		ordered = ordered + toOrder[order[i]-1]
	return ordered

#são passados dois blocos de 4 bits e devolvidos um de 4 bits
def s0s1(left4, right4):
	i = int(left4[0] + left4[3], 2)
	j = int(left4[1] + left4[2], 2)
	left4 = bin(tableS0[i][j])[2:].zfill(4)
	i = int(right4[0] + right4[3], 2)
	j = int(right4[1] + right4[2], 2)
	right4 = bin(tableS0[i][j])[2:].zfill(4)
	#print("s0s1", binaryStringToCharFormat(left4 + right4))
	#print("s0s1", (left4 + right4))
	return left4 + right4

#gera uma string de binario correspondente ao valor decimal passado
def decimalToBinaryString(value):
	#transforma o char em valor inteiro
	x = ''
	for i in range(10):
		if value - pot2[i] >= 0:
			x = x + '1'
			value = value - pot2[i]
		else:
			x = x + '0'
	return x

#gera binario de uma string
#só será passado um char ao invés de string completa, considerando a cifra de bloco
def charToBinaryString(message):
	"""
	print("bbbbbbbbbbbbbbbb", message)
	print("bbbbbbbbbbbbbbbb", message.encode())
	print("bbbbbbbbbbbbbbbb", int.from_bytes(message.encode(), 'big'))
	print("bbbbbbbbbbbbbbbb", bin(int.from_bytes(message.encode(), 'big')))
	"""
	return bin(int.from_bytes(message.encode(), 'big'))

#formata o resultado retirando o "0b" inicial que identifica o binario
def charToBinaryStringFormat(message):
	n = charToBinaryString(message)
	#retira os bits iniciais "0b" (usando a mensagem a partir do 3 caractere)
	#ex: o método acima retorna '0b10011001' retira-se os 2 primeiros chars ('0b' representa o formato binário) ficando apenas '10011001'
	n = n[2:]
	#caso a string venha menor que 8 (pois não considera os zeros a esquerda), a completa adicionando os zero não significativos a esquerda
	#adequando-a ao tamanho de 8 caracteres, cada representando 1 bit
	while len(n)<8:
		n = '0' + n
	return n

def binaryStringToChar(message):
	n = int(message, 2)
	return chr(n)
	"""
	print('n = ', n)
	print((n.bit_length()+7) // 8)
	print(n.to_bytes( 1, 'big'))
	print(n.to_bytes( (n.bit_length()+7) // 8, 'big').decode())
	return n.to_bytes( (n.bit_length()+7) // 8, 'big').decode()
	"""

#formata o resultado adicionando o "0b" inicial que identifica o binario
def binaryStringToCharFormat(message):

	n = '0b' + message
	#print("msg", n)
	n = binaryStringToChar(n)
	#print(n)
	n = '0b' + n
	return n

def xor(value1, value2, valueSize):
	#stop here

	n = ''
	for i in range(valueSize):
		if value1[i]==value2[i]:
			n = n + '0'
		else:
			n = n + '1'
	return n

#SW switch transposicao do resultado de fK, trocando os primeiros 4 bits com os ultimos 4 bits
def SW(data):
	x = data[4:] + data[:4]
	return x
