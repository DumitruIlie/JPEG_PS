# Ilie Dumitru

import numpy as np
import scipy
import matplotlib.pyplot as plt
import sys
import os
import heapq
from utils import *


zigzag=[]

def precalcZigZag():
	global zigzag
	zigzag=[(x[2], x[3]) for x in sorted([(i+j, (i+j)%2*(i-j)+j, i, j) for i in range(8) for j in range(8)])]


def parseParameters():
	args=sys.argv[1:]
	ret=dict()
	i=0
	while i<len(args):
		if args[i]=="-f" or args[i]=="--file":
			if "file" in ret:
				return "Fisier definit de mai multe ori"
			i+=1
			if i==len(args):
				return f"Parametru asteptat dupa \"{args[i-1]}\" dar nu a fost gasit"
			ret["file"]=args[i]
			i+=1
		elif os.path.isfile(args[i]): # Momentan nu am alti parametrii. If-ul asta ar trebui sa fie ultimul mereu
			if "file" in ret:
				return "Fisier definit de mai multe ori"
			ret["file"]=args[i]
			i+=1
		else:
			return f"Parametru necunoscut: {args[i]}"

	if "file" not in ret:
		return "Fisier intrare lipsa"

	return ret


def decode(bits, Q, color):
	if color:
		quants=[quantLuma(Q), quantChroma(Q), quantChroma(Q)]
		ycbcr=[]
		for channel in range(3):
			huffman=HuffmanNode.fromBitString(bits)
			bits.clearByte()
			vals=[huffman.readValue(bits) for _ in range(64)]
			bits.clearByte()
			dct=np.zeros((8, 8))
			for i in range(64):
				dct[zigzag[i]]=vals[i]
			ycbcr.append(scipy.fft.idctn(dct*quants[channel]))
		rgb=np.clip(np.round(ybr2rgb(*ycbcr)).astype(np.int16), 0, 255)
		ans=np.zeros((8, 8, 3), dtype=np.int16)
		for i in range(3):
			ans[:, :, i]=rgb[i]
		return ans

	huffman=HuffmanNode.fromBitString(bits)
	bits.clearByte()
	vals=[huffman.readValue(bits) for _ in range(64)]
	bits.clearByte()
	dct=np.zeros((8, 8))
	for i in range(64):
		dct[zigzag[i]]=vals[i]
	return scipy.fft.idctn(dct*quantLuma(Q))+128


def main():
	precalcZigZag()
	parameters=parseParameters()

	with open(parameters["file"], "rb") as f:
		inp=byteReader(bytearray(f.read()))
	N=inp.readInt()
	M=inp.readInt()
	C=inp.readInt()
	Q=inp.readInt()
	inp.clearByte()

	if C==1:
		img=np.zeros(((N+7)//8*8, (M+7)//8*8), dtype=np.int16)
		for i in range(0, N, 8):
			for j in range(0, M, 8):
				img[i:i+8, j:j+8]=decode(inp, Q, color=False)
		img=img[:N, :M]
	elif C==3:
		img=np.zeros(((N+7)//8*8, (M+7)//8*8, 3), dtype=np.int16)
		for i in range(0, N, 8):
			for j in range(0, M, 8):
				img[i:i+8, j:j+8, :]=decode(inp, Q, color=True)
		img=img[:N, :M]
	else:
		raise Exception(f"Fisier malformat. {C=}")

	plt.imshow(img, cmap="gray")
	plt.clim(0, 255)
	plt.show()


if __name__=="__main__":
	main()
