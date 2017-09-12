
class sdes():

	#CIPHER = sdes(14)
	#CIPHER.encode(message)

	def __init__(self, key):
		
		self.k10 = key
		self.k1p8 = 0
		self.k2p8 = 0

		self.tableS0 = [[1, 0, 3, 2], [3, 2, 1, 0], [0, 2, 1, 3], [3, 1, 3, 2]]
		self.tableS1 = [[1, 1, 2, 3], [2, 0, 1, 3], [3, 0, 1, 0], [2, 1, 0, 3]]

		self.sdesK1K2(key)

	def startWithKey(self, key, message):
		
		k10 = key
		
		sdesK1K2(key)

		Encode(message)

	def Encode(self, message):
		
		finalMessageBytes = message.encode()

		block = 0

		blockPart1 = 0
		blockPart2 = 0

		OriginalBlockPart2 = 0

		for index in range(0, len(finalMessageBytes))

			block = self.ip( finalMessageBytes[index] )

			# get part 1 and part 2 from IP result

			blockPart1 = block >> 4
			blockPart1 = blockPart1 << 12
			blockPart1 = blockPart1 >> 8

			blockPart2 = block << 12
			blockPart2 = blockPart2 >> 12

			OriginalBlockPart2 = blockPart2 // will be used in the end

			# Expansion of the blockPart2
			blockPart2 = self.ep(blockPart2)

			# xor
			blockPart2 = (blockPart2 ^ self.k1p8)

			# divide in 2 parts the blockPart2

			blockPart21 = 0
			blockPart22 = 0

			blockPart21 = blockPart2 >> 4
			blockPart21 = blockPart21 << 12
			blockPart21 = blockPart21 >> 8

			blockPart22 = blockPart2 << 12
			blockPart22 = blockPart22 >> 12

			# 8 bits to 4 using functions S0 and S1

			blockPart2 = self.s0s1(blockPart21, blockPart22)

			temp = 0
			temp1 = 0

			temp = blockPart2 >> 2
			temp = temp << 15
			temp = temp >> 12
			temp1 = temp1 | temp

			temp = blockPart2 << 15
			temp = temp >> 13
			temp1 = temp1 | temp

			temp = blockPart2 >> 1
			temp = temp << 15
			temp = temp >> 14
			temp1 = temp1 | temp

			temp = blockPart2 >> 3
			temp = temp << 15
			temp = temp >> 15
			temp1 = temp1 | temp

			# second xor (blockPart1 and blockPart2)

			block = (((blockPart1 >> 4) ^ blockPart2) << 4) | OriginalBlockPart2

			# SWAP

			temp = 0
			temp1 = 0

			temp = block >> 4
			temp = temp << 12
			temp = temp >> 12

			temp1 = block << 12
			temp1 = temp1 >> 8

			block = temp1 | temp

			# repeat code above (less the swap) but now using the self.k2p8 --------------------------

			# get part 1 and part 2 from IP result

			blockPart1 = block >> 4
			blockPart1 = blockPart1 << 12
			blockPart1 = blockPart1 >> 8

			blockPart2 = block << 12
			blockPart2 = blockPart2 >> 12

			OriginalBlockPart2 = blockPart2 // will be used in the end

			# Expansion of the blockPart2
			blockPart2 = self.ep(blockPart2)

			# xor
			blockPart2 = (blockPart2 ^ self.k2p8)

			# divide in 2 parts the blockPart2
			blockPart21x = 0
			blockPart22x = 0

			blockPart21x = blockPart2 >> 4
			blockPart21x = blockPart21x << 12
			blockPart21x = blockPart21x >> 8

			blockPart22x = blockPart2 << 12
			blockPart22x = blockPart22x >> 12

			# 8 bits to 4 using functions S0 and S1

			blockPart2 = self.s0s1(blockPart21x, blockPart22x)

			tempx = 0
			temp1x = 0

			tempx = blockPart2 >> 2
			tempx = tempx << 15
			tempx = tempx >> 12
			temp1x = temp1x | tempx

			tempx = blockPart2 << 15
			tempx = tempx >> 13
			temp1x = temp1x | tempx

			tempx = blockPart2 >> 1
			tempx = tempx << 15
			tempx = tempx >> 14
			temp1x = temp1x | tempx

			tempx = blockPart2 >> 3
			tempx = tempx << 15
			tempx = tempx >> 15
			temp1x = temp1x | tempx

			# second xor (blockPart1 and blockPart2)
			finalMessageBytes[index] = self.ip1( (((blockPart1 >> 4) ^ blockPart2) << 4) | OriginalBlockPart2 )

		return finalMessageBytes


	def Decode(self, message):

		finalMessageBytes = message.encode()

		block = 0

		blockPart1 = 0
		blockPart2 = 0

		OriginalBlockPart2 = 0

		for index in range(0, len(finalMessageBytes))
			block = self.ip( finalMessageBytes[index] )

			# get part 1 and part 2 from IP result

			blockPart1 = block >> 4
			blockPart1 = blockPart1 << 12
			blockPart1 = blockPart1 >> 8

			blockPart2 = block << 12
			blockPart2 = blockPart2 >> 12

			OriginalBlockPart2 = blockPart2 // will be used in the end

			# Expansion of the blockPart2
			blockPart2 = self.ep(blockPart2)

			# xor of second part of block with key of 10
			blockPart2 = (blockPart2 ^ self.k1p8)

			# divide in 2 parts the blockPart2

			blockPart21 = 0
			blockPart22 = 0

			blockPart21 = blockPart2 >> 4
			blockPart21 = blockPart21 << 12
			blockPart21 = blockPart21 >> 8

			blockPart22 = blockPart2 << 12
			blockPart22 = blockPart22 >> 12

			# 8 bits to 4 using functions S0 and S1

			blockPart2 = self.s0s1(blockPart21, blockPart22)

			temp = 0
			temp1 = 0

			temp = blockPart2 >> 2
			temp = temp << 15
			temp = temp >> 12
			temp1 = temp1 | temp

			temp = blockPart2 << 15
			temp = temp >> 13
			temp1 = temp1 | temp

			temp = blockPart2 >> 1
			temp = temp << 15
			temp = temp >> 14
			temp1 = temp1 | temp

			temp = blockPart2 >> 3
			temp = temp << 15
			temp = temp >> 15
			temp1 = temp1 | temp

			# second xor (blockPart1 and blockPart2)

			block = (((blockPart1 >> 4) ^ blockPart2) << 4) | OriginalBlockPart2

			# SWAP

			temp = 0
			temp1 = 0

			temp = block >> 4
			temp = temp << 12
			temp = temp >> 12

			temp1 = block << 12
			temp1 = temp1 >> 8

			block = temp1 | temp

			# repeat code above (less the swap) but now using the self.k2p8 --------------------------

			# get part 1 and part 2 from IP result

			blockPart1 = block >> 4
			blockPart1 = blockPart1 << 12
			blockPart1 = blockPart1 >> 8

			blockPart2 = block << 12
			blockPart2 = blockPart2 >> 12

			OriginalBlockPart2 = blockPart2 // will be used in the end

			# Expansion of the blockPart2
			blockPart2 = self.ep(blockPart2)

			# xor
			blockPart2 = (blockPart2 ^ self.k2p8)

			# divide in 2 parts the blockPart2

			blockPart21x = 0
			blockPart22x = 0

			blockPart21x = blockPart2 >> 4
			blockPart21x = blockPart21x << 12
			blockPart21x = blockPart21x >> 8

			blockPart22x = blockPart2 << 12
			blockPart22x = blockPart22x >> 12

			# 8 bits to 4 using functions S0 and S1

			blockPart2 = self.s0s1(blockPart21x, blockPart22x)

			tempx = 0
			temp1x = 0

			tempx = blockPart2 >> 2
			tempx = tempx << 15
			tempx = tempx >> 12
			temp1x = temp1x | tempx

			tempx = blockPart2 << 15
			tempx = tempx >> 13
			temp1x = temp1x | tempx

			tempx = blockPart2 >> 1
			tempx = tempx << 15
			tempx = tempx >> 14
			temp1x = temp1x | tempx

			tempx = blockPart2 >> 3
			tempx = tempx << 15
			tempx = tempx >> 15
			temp1x = temp1x | tempx

			# second xor (blockPart1 and blockPart2)

			finalMessageBytes[index] = self.ip1( (((blockPart1 >> 4) ^ blockPart2) << 4) | OriginalBlockPart2 )

		return finalMessageBytes


	def sdesK1K2(self):
		tempK10 = 0

		tempK101 = 0
		tempK102 = 0

		shitfPart1 = 0
		shitfPart2 = 0

		tempKp8 = 0

		# SHIFT 1 part 1 ------------------------------------------

		# 0000001111000000

		tempK101 = self.k10 >> 6
		tempK101 = tempK101 << 12
		tempK101 = tempK101 >> 6


		# 0000000000100000

		tempK102 = self.k10 >> 5
		tempK102 = tempK102 << 15
		tempK102 = tempK102 << 10

		# 0000000000100000 | 0000001111000000 = 0000001111100000

		shitfPart1 = tempK101 | tempK102

		# SHIFT 1 part 2 ------------------------------------------

		# 0000000000011110

		tempK101 = 0
		tempK101 = self.k10 >> 1
		tempK101 = tempK101 << 12
		tempK101 = tempK101 >> 11

		# 0000000000000001

		tempK102 = 0
		tempK102 = self.k10 << 15
		tempK102 = tempK102 >> 15

		# 0000000000000001 | 0000000000011110 = 0000000000011111

		shitfPart2 = tempK101 | tempK102

		# the Key after the shift ---------------------------------

		shiftFinal = shitfPart1 | shitfPart2

		# K1 generation -------------------------------------------

		tempK10 = 0
		tempK10 = shiftFinal >> 4
		tempK10 = tempK10 << 15
		tempK10 = tempK10 >> 8
		tempKp8 = tempKp8 | tempK10

		tempK10 = 0
		tempK10 = shiftFinal >> 7
		tempK10 = tempK10 << 15
		tempK10 = tempK10 >> 9
		tempKp8 = tempKp8 | tempK10

		tempK10 = 0
		tempK10 = shiftFinal >> 3
		tempK10 = tempK10 << 15
		tempK10 = tempK10 >> 10
		tempKp8 = tempKp8 | tempK10

		tempK10 = 0
		tempK10 = shiftFinal>> 6
		tempK10 = tempK10 << 15
		tempK10 = tempK10 >> 11
		tempKp8 = tempKp8 | tempK10

		tempK10 = 0
		tempK10 = shiftFinal >> 2
		tempK10 = tempK10 << 15
		tempK10 = tempK10 >> 12
		tempKp8 = tempKp8 | tempK10

		tempK10 = 0
		tempK10 = shiftFinal >> 5
		tempK10 = tempK10 << 15
		tempK10 = tempK10 >> 13
		tempKp8 = tempKp8 | tempK10

		tempK10 = 0
		tempK10 = shiftFinal << 15
		tempK10 = tempK10 >> 14
		tempKp8 = tempKp8 | tempK10

		tempK10 = 0
		tempK10 = shiftFinal >> 1
		tempK10 = tempK10 << 15
		tempK10 = tempK10 >> 15
		tempKp8 = tempKp8 | tempK10

		############################  atribuição k1p8  ############################
		k1p8 = tempKp8
		############################  atribuição k1p8  ############################

		# shift 2 part 1.1 ---------------------------------------

		tempK101 = 0
		tempK102 = 0
		shitfPart1 = 0
		shitfPart2 = 0

		# 0000001111000000

		tempK101 = shiftFinal >> 6
		tempK101 = tempK101 << 12
		tempK101 = tempK101 >> 6

		# 0000000000100000

		tempK102 = shiftFinal >> 5
		tempK102 = tempK102 << 15
		tempK102 = tempK102 >> 10

		# 0000000000100000 | 0000001111000000 = 0000001111100000

		shitfPart1 = tempK101 | tempK102

		# shift 2 part 1.2 ---------------------------------------

		tempK101 = 0
		tempK102 = 0
		shitfPart1 = 0
		shitfPart2 = 0

		# 0000001111000000

		tempK101 = shitfPart1 >> 6
		tempK101 = tempK101 << 12
		tempK101 = tempK101 >> 6

		# 0000000000100000

		tempK102 = shitfPart1 >> 5
		tempK102 = tempK102 << 15
		tempK102 = tempK102 >> 10

		# 0000000000100000 | 0000001111000000 = 0000001111100000

		shitfPart1 = tempK101 | tempK102

		# shift 2 part 2.1 ---------------------------------------

		tempK101 = 0
		tempK102 = 0
		shitfPart1 = 0
		shitfPart2 = 0

		# 0000000000011110

		tempK101 = shiftFinal >> 1
		tempK101 = tempK101 << 12
		tempK101 = tempK101 >> 11

		# 0000000000000001

		tempK102 = shiftFinal << 15
		tempK102 = tempK102 >> 15

		# 0000000000000001 | 0000000000011110 = 0000000000011111

		shitfPart2 = tempK101 | tempK102

		# shift 2 part 2.2 ---------------------------------------

		tempK101 = 0
		tempK102 = 0
		shitfPart1 = 0
		shitfPart2 = 0

		# 0000000000011110

		tempK101 = shitfPart2 >> 1
		tempK101 = tempK101 << 12
		tempK101 = tempK101 >> 11

		# 0000000000000001

		tempK102 = shitfPart2 << 15
		tempK102 = tempK102 >> 15

		# 0000000000000001 | 0000000000011110 = 0000000000011111

		shitfPart2 = tempK101 | tempK102

		# the Key after the shift ---------------------------------

		shiftFinal = shitfPart1 | shitfPart2

		# K2 generation ----------------------------------------
		tempKp8 = 0

		tempK10 = 0
		tempK10 = shiftFinal >> 4
		tempK10 = tempK10 << 15
		tempK10 = tempK10 >> 8
		tempKp8 = tempKp8 | tempK10

		tempK10 = 0
		tempK10 = shiftFinal >> 7
		tempK10 = tempK10 << 15
		tempK10 = tempK10 >> 9
		tempKp8 = tempKp8 | tempK10

		tempK10 = 0
		tempK10 = shiftFinal >> 3
		tempK10 = tempK10 << 15
		tempK10 = tempK10 >> 10
		tempKp8 = tempKp8 | tempK10

		tempK10 = 0
		tempK10 = shiftFinal >> 6
		tempK10 = tempK10 << 15
		tempK10 = tempK10 >> 11
		tempKp8 = tempKp8 | tempK10

		tempK10 = 0
		tempK10 = shiftFinal >> 2
		tempK10 = tempK10 << 15
		tempK10 = tempK10 >> 12
		tempKp8 = tempKp8 | tempK10

		tempK10 = 0
		tempK10 = shiftFinal >> 5
		tempK10 = tempK10 << 15
		tempK10 = tempK10 >> 13
		tempKp8 = tempKp8 | tempK10

		tempK10 = 0
		tempK10 = shiftFinal << 15
		tempK10 = tempK10 >> 14
		tempKp8 = tempKp8 | tempK10

		tempK10 = 0
		tempK10 = shiftFinal >> 1
		tempK10 = tempK10 << 15
		tempK10 = tempK10 >> 15
		tempKp8 = tempKp8 | tempK10

		############################  atribuição k2p8  ############################
		k2p8 = tempKp8
		############################  atribuição k2p8  ############################

	# initial permutation
	def ip(self, value):
		tempValue = 0
		tempPermutation = 0

		tempPermutation = 0
		tempPermutation = value >> 6
		tempPermutation = tempPermutation << 15
		tempPermutation = tempPermutation >> 8
		tempValue = tempValue | tempPermutation

		tempPermutation = 0
		tempPermutation = value >> 2
		tempPermutation = tempPermutation << 15
		tempPermutation = tempPermutation >> 9
		tempValue = tempValue | tempPermutation

		tempPermutation = 0
		tempPermutation = value >> 5
		tempPermutation = tempPermutation << 15
		tempPermutation = tempPermutation >> 10
		tempValue = tempValue | tempPermutation

		tempPermutation = 0
		tempPermutation = value >> 7
		tempPermutation = tempPermutation << 15
		tempPermutation = tempPermutation >> 11
		tempValue = tempValue | tempPermutation

		tempPermutation = 0
		tempPermutation = value >> 4
		tempPermutation = tempPermutation << 15
		tempPermutation = tempPermutation >> 12
		tempValue = tempValue | tempPermutation

		tempPermutation = 0
		tempPermutation = value << 15
		tempPermutation = tempPermutation >> 13
		tempValue = tempValue | tempPermutation

		tempPermutation = 0
		tempPermutation = value >> 3
		tempPermutation = tempPermutation << 15
		tempPermutation = tempPermutation >> 14
		tempValue = tempValue | tempPermutation

		tempPermutation = 0
		tempPermutation = value >> 1
		tempPermutation = tempPermutation << 15
		tempPermutation = tempPermutation >> 15
		tempValue = tempValue | tempPermutation

		return tempValue


	# initial permutation -1, for decrypt
	def ip1(self, value):
		tempValue = 0
		tempPermutation = 0

		tempPermutation = 0
		tempPermutation = value >> 4
		tempPermutation = tempPermutation << 15
		tempPermutation = tempPermutation >> 8
		tempValue = tempValue | tempPermutation

		tempPermutation = 0
		tempPermutation = value >> 7
		tempPermutation = tempPermutation << 15
		tempPermutation = tempPermutation >> 9
		tempValue = tempValue | tempPermutation

		tempPermutation = 0
		tempPermutation = value >> 5
		tempPermutation = tempPermutation << 15
		tempPermutation = tempPermutation >> 10
		tempValue = tempValue | tempPermutation

		tempPermutation = 0
		tempPermutation = value >> 3
		tempPermutation = tempPermutation << 15
		tempPermutation = tempPermutation >> 11
		tempValue = tempValue | tempPermutation

		tempPermutation = 0
		tempPermutation = value >> 1
		tempPermutation = tempPermutation << 15
		tempPermutation = tempPermutation >> 12
		tempValue = tempValue | tempPermutation

		tempPermutation = 0
		tempPermutation = value >> 6
		tempPermutation = tempPermutation << 15
		tempPermutation = tempPermutation >> 13
		tempValue = tempValue | tempPermutation

		tempPermutation = 0
		tempPermutation = value << 15
		tempPermutation = tempPermutation >> 14
		tempValue = tempValue | tempPermutation

		tempPermutation = 0
		tempPermutation = value >> 2
		tempPermutation = tempPermutation << 15
		tempPermutation = tempPermutation >> 15
		tempValue = tempValue | tempPermutation

		return tempValue


	# expansion of 4 bits in 8
	def ep(self, value):
		tempValue = 0
		tempPermutation = 0

		tempPermutation = 0
		tempPermutation = value << 15
		tempPermutation = tempPermutation >> 8
		tempValue = tempValue | tempPermutation

		tempPermutation = 0
		tempPermutation = value >> 3
		tempPermutation = tempPermutation << 15
		tempPermutation = tempPermutation >> 9
		tempValue = tempValue | tempPermutation

		tempPermutation = 0
		tempPermutation = value >> 2
		tempPermutation = tempPermutation << 15
		tempPermutation = tempPermutation >> 10
		tempValue = tempValue | tempPermutation

		tempPermutation = 0
		tempPermutation = value >> 1
		tempPermutation = tempPermutation << 15
		tempPermutation = tempPermutation >> 11
		tempValue = tempValue | tempPermutation

		tempPermutation = 0
		tempPermutation = value >> 2
		tempPermutation = tempPermutation << 15
		tempPermutation = tempPermutation >> 12
		tempValue = tempValue | tempPermutation

		tempPermutation = 0
		tempPermutation = value >> 1
		tempPermutation = tempPermutation << 15
		tempPermutation = tempPermutation >> 13
		tempValue = tempValue | tempPermutation

		tempPermutation = 0
		tempPermutation = value << 15
		tempPermutation = tempPermutation >> 14
		tempValue = tempValue | tempPermutation

		tempPermutation = 0
		tempPermutation = value >> 3
		tempPermutation = tempPermutation << 15
		tempPermutation = tempPermutation >> 15
		tempValue = tempValue | tempPermutation

		return tempValue

	# s0s2, função baseada na matriz
	def s0s1(self, blockPart21, blockPart22):

	  i1 = blockPart21 >> 6
	  i1 = i1 << 14
	  i1 = i1 >> 14

	  j1 = blockPart22 >> 2
	  j1 = j1 << 14
	  j1 = j1 >> 14

	  i2 = blockPart21 >> 4
	  i2 = i2 << 14
	  i2 = i2 >> 14

	  j2 = blockPart22 << 14
	  j2 = j2 >> 14

	  resultPart1 = tableS0[j1][i1] << 2

	  resultPart2 = tableS1[j2][i2]

	  return (resultPart1 | resultPart2)

