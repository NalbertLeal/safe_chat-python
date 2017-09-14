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

	#recebe uma mensagem string em texto plano (ex.: 'teste')
	#gera uma string  de tamanho múltiplo de 8, 
	#no qual a cada 8, equivale ao char criptografado
	def Encode(self, message):
		encoded = ''
		#encripta cada caractere da mensagem por vez
		#gerando uma string cujos valores são apenas 0 e 1 (ex.:'10101010'), o qual representa o caractere encriptado
		for i in range(0, len(message)):
			######################## manipulacao de tipos #########################
			#muda o valor do char para uma string com os valores binarios dele, trazendo formatado com tamanho 8 bits
			inBin = charToBinaryStringFormat(message[i])
			#fk ocorre uma vez com a primeira chave
			ip = self.encodeFK(inBin, self.k1p8)
			#SW switch transposicao do resultado de fK, trocando os primeiros 4 bits com os ultimos 4 bits
			#ipa = permutation(sw, ip)
			ip = permutation(sw, ip)
			#fk ocorre uma vez com a segunda chave
			ip1 = self.encodeFK(ip, self.k2p8)
			#une a mensagem em binário até ela possuir todos os caracteres encriptados
			encoded = encoded + ip1

		#no final une todas as strings que representam os caracteres encriptados
		return encoded

	#recebe a string que representa todos os caracteres encriptados
	#e retorna uma string em texto plano decriptada
	def Decode(self, message):
		decoded = ''
		j = 0
		for i in range(0, len(message)):
			#pega de 8 em 8 bits da mensagem (já que representa um caractere criptogrado) para decriptar
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

	#funcao fk, comum a encriptacao e a decriptacao
	def encodeFK(self, message, key):
		########################### funcao fK ###############################
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
		cipher = rightBits + message[4:]

		return cipher

	#gera as chaves k1 (k1p8) e k2 (k2p8)
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

#faz a permutacao da nova ordem que ficará o novo dado a ordenar, com o dado a ser manipulado(toOrder)
def permutation(order, toOrder):
	ordered = ''
	for i in range(len(order)):
		ordered = ordered + toOrder[order[i]-1]
	return ordered

#resultado de s0 e s1, são passados dois blocos de 4 bits e devolvidos um de 4 bits, já concatenados a partir do resultado s0 e s1
def s0s1(left4, right4):
	#encontra as posições a se busca na matriz s0
	i = int(left4[0] + left4[3], 2)
	j = int(left4[1] + left4[2], 2)
	#busca na constante definida globalmente, o resultado do s0
	left4 = bin(tableS0[i][j])[2:].zfill(4)

	#mesmo processo anterior, mas usando a constante s1 e os elementos da direita
	i = int(right4[0] + right4[3], 2)
	j = int(right4[1] + right4[2], 2)
	right4 = bin(tableS0[i][j])[2:].zfill(4)

	return left4 + right4

#gera uma string de binario correspondente ao valor decimal passado
def decimalToBinaryString(value):
	#transforma o char que representa o inteiro em um valor inteiro de fato
	x = ''
	#só é usando para a chave de 10 bits, entao o tamanho é estatico
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

#formata a string que representa o binario de um char no char correspondente
def binaryStringToChar(message):
	n = int(message, 2)
	return chr(n)

#xor de dois valores
def xor(value1, value2, valueSize):
	n = ''
	for i in range(valueSize):
		if value1[i]==value2[i]:
			n = n + '0'
		else:
			n = n + '1'
	return n

