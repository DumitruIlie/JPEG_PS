# Ilie Dumitru

import numpy as np


def byteToBits(B):
	return ''.join([str((B>>i)&1) for i in range(7, -1, -1)])


class byteReader:
	def __init__(self, s):
		self.curr=0
		self.s=[byteToBits(x) for x in s]

	def getBit(self):
		if self.curr>=len(self.s)*8:
			raise Exception("Too few bits in byte string")
		x=self.s[self.curr//8][self.curr%8]
		self.curr+=1
		return x

	def getByte(self):
		return int(''.join([self.getBit() for _ in range(8)]), 2)

	def readInt(self):
		if self.getBit()=='0':
			return self.getByte()-128
		return self.getByte()*256+self.getByte()-16384

	def clearByte(self):
		self.curr=(self.curr+7)//8*8


def int8_16ToBinary(x):
	if -128<=x<=127:
		return f"0{bin(x+128)[2:].rjust(8, '0')}"
	return f"1{bin(16384+x)[2:].rjust(16, '0')}"


def binaryToInt8_16(s):
	if s[0]=='0':
		return int(s[1:], 2)-128
	return int(s[1:], 2)-16384


class HuffmanNode:
	def __init__(self, cnt, symbol=None, left=None, right=None):
		self.cnt=cnt
		self.symbol=symbol
		self.l=left
		self.r=right

	def __lt__(self, other):
		return self.cnt<other.cnt

	def print(self, before=[]):
		if self.symbol is not None:
			print(*before, ' ', self.symbol, sep='')
		else:
			before.append(0)
			self.l.print(before)
			before[-1]+=1
			self.r.print(before)
			before.pop()

	def toDict(self, before=[]):
		if self.symbol is not None:
			s=''.join(before)
			return {self.symbol: s}, ['0', int8_16ToBinary(self.symbol)]
		before.append('0')
		coding, decoding=self.l.toDict(before)
		before[-1]='1'
		aux=self.r.toDict(before)
		coding.update(aux[0])
		decoding.extend(aux[1])
		before.pop()
		aux=['1']
		aux.extend(decoding)
		return coding, aux

	def toBitString(self):
		return ''.join(self.toDict()[1])

	@staticmethod
	def fromBitString(br):
		if br.getBit()=='1':
			return HuffmanNode(None, None, HuffmanNode.fromBitString(br), HuffmanNode.fromBitString(br))
		return HuffmanNode(None, br.readInt(), None, None)

	def readValue(self, br):
		if self.symbol is not None:
			return self.symbol
		if br.getBit()=='0':
			return self.l.readValue(br)
		return self.r.readValue(br)


def bitstringToBytes(s):
	if len(s)==0:
		return b""
	return int(s.ljust((len(s)+7)//8*8, '0'), 2).to_bytes((len(s) + 7) // 8, byteorder='big')


matrQuantLuma=np.array(
	[
		[16, 11, 10, 16,  24,  40,  51,  61],
		[12, 12, 14, 19,  26,  28,  60,  55],
		[14, 13, 16, 24,  40,  57,  69,  56],
		[14, 17, 22, 29,  51,  87,  80,  62],
		[18, 22, 37, 56,  68, 109, 103,  77],
		[24, 35, 55, 64,  81, 104, 113,  92],
		[49, 64, 78, 87, 103, 121, 120, 101],
		[72, 92, 95, 98, 112, 100, 103,  99]
	]
)


matrQuantChroma=np.array(
	[
		[17, 18, 24, 47, 99, 99, 99, 99],
		[18, 21, 26, 66, 99, 99, 99, 99],
		[24, 26, 56, 99, 99, 99, 99, 99],
		[47, 66, 99, 99, 99, 99, 99, 99],
		[99, 99, 99, 99, 99, 99, 99, 99],
		[99, 99, 99, 99, 99, 99, 99, 99],
		[99, 99, 99, 99, 99, 99, 99, 99],
		[99, 99, 99, 99, 99, 99, 99, 99]
	]
)


def quantQuality(mat, Q):
	scale=5000/Q if Q<50 else 200-2*Q
	mat=np.round((scale*mat)/100).astype(np.uint16)
	mat[mat==0]=1
	return mat


computedLuma=dict()
def quantLuma(Q):
	if Q in computedLuma:
		return computedLuma[Q]
	computedLuma[Q]=quantQuality(matrQuantLuma, Q)
	return computedLuma[Q]


computedChroma=dict()
def quantChroma(Q):
	if Q in computedChroma:
		return computedChroma[Q]
	computedChroma[Q]=quantQuality(matrQuantChroma, Q)
	return computedChroma[Q]


def rgb2ybr(r, g, b):
	r/=255
	g/=255
	b/=255
	return np.round((0.3*r+0.587*g+0.114*b)*255-128), np.round((-0.168736*r-0.331264*g+0.5*b)*255), np.round((0.5*r-0.418688*g-0.081312*b)*255)


def ybr2rgb(y, cb, cr):
	y=(y+128)/255
	cb=cb/255
	cr=cr/255
	return np.round((y+1.4*cr)*255), np.round((y-0.344*cb-0.71*cr)*255), np.round((y+1.772*cb-0.001*cr)*255)
