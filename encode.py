# Ilie Dumitru

import numpy as np
import scipy
import sys
import os
import heapq
from utils import *


zigzag=[]

def precalcZigZag():
	global zigzag
	zigzag=[(x[2], x[3]) for x in sorted([(i+j, (i+j)%2*(i-j)+j, i, j) for i in range(8) for j in range(8)])]


def huffmanEncoding(v):
	cnt=dict()
	for x in v:
		if x in cnt:
			cnt[x]+=1
		else:
			cnt[x]=1

	pq=[HuffmanNode(cnt[x], x) for x in cnt]
	heapq.heapify(pq)
	while len(pq)>1:
		a=heapq.heappop(pq)
		b=heapq.heappop(pq)
		heapq.heappush(pq, HuffmanNode(a.cnt+b.cnt, None, a, b))

	huffmanTree=heapq.heappop(pq)
	coding, decoding=huffmanTree.toDict()

	ans=[]
	for x in v:
		ans.append(coding[x])
	return bitstringToBytes(''.join(ans)), bitstringToBytes(''.join(decoding))


def encodeBlock(block, parameters):
	Q=parameters["Q"]

	if len(block.shape)==3:
		# Colorat
		Y, Cb, Cr=list(map(scipy.fft.dctn, rgb2ybr(block[:, :, 0], block[:, :, 1], block[:, :, 2])))

		Y=np.round(Y/quantLuma(Q)).astype(np.int16)
		Cb=np.round(Cb/quantChroma(Q)).astype(np.int16)
		Cr=np.round(Cr/quantChroma(Q)).astype(np.int16)

		lY=[Y[x] for x in zigzag]
		lCb=[Cb[x] for x in zigzag]
		lCr=[Cr[x] for x in zigzag]

		codeY, decodeY=huffmanEncoding(lY)
		codeCb, decodeCb=huffmanEncoding(lCb)
		codeCr, decodeCr=huffmanEncoding(lCr)

		return decodeY+codeY+decodeCb+codeCb+decodeCr+codeCr

	if len(block.shape)==2:
		# Alb-negru
		block-=128
		block=scipy.fft.dctn(block)
		block=np.round(block/quantLuma(Q)).astype(np.int16)

		linearized=[block[x] for x in zigzag]
		code, decoding=huffmanEncoding(linearized)
		return decoding+code

	# Nu ar trebui sa se ajunga aici dar cine stie?
	print(f"How did we get here? {len(block.shape)=}")


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
		elif args[i]=="-Q" or args[i]=="-q":
			if "Q" in ret:
				return "Calitatea definita de mai multe ori"
			i+=1
			if i==len(args):
				return f"Parametru asteptat dupa \"{args[i-1]}\" dar nu a fost gasit"
			try:
				ret["Q"]=int(args[i])
			except:
				return f"Calitate asteptata ca un intreg dupa \"{args[i-1]}\" dar a fost gasit \"{args[i]}\""
			i+=1
			if ret["Q"]<1 or ret["Q"]>100:
				return "Calitatea trebuie sa fie intre 1 si 100 (inlcusiv)"
		elif args[i].endswith("%"):
			try:
				ret["Q"]=int(args[i][:-1])
			except:
				return f"Calitate gasita dar formatata prost. \"{args[i]}\" dar a fost gasit \"{args[i]}\""
			i+=1
			if ret["Q"]<1 or ret["Q"]>100:
				return "Calitatea trebuie sa fie intre 1 si 100 (inlcusiv)"
		elif args[i]=="-O" or args[i]=="-o":
			if "O" in ret:
				return "Output specificat de mai multe ori"
			i+=1
			if i==len(args):
				return f"Parametru asteptat dupa \"{args[i-1]}\" dar nu a fost gasit"
			ret["O"]=args[i]
			i+=1
		elif os.path.isfile(args[i]): # Momentan nu am alti parametrii. If-ul asta ar trebui sa fie ultimul mereu
			if "file" in ret:
				return "Fisier definit de mai multe ori"
			ret["file"]=args[i]
			i+=1
		else:
			return f"Parametru necunoscut: {args[i]}"

	if "Q" not in ret:
		ret["Q"]=50
		print(f"\033[103;30;02mNu s-a primit o valoare pentru calitate. Folosim implicit Q={ret['Q']}\033[0m")

	return ret


def readInput(parameters):
	assert(parameters["file"].endswith(".txt"))
	with open(parameters["file"], "r") as fin:
		N, M, C=map(int, fin.readline().split())
		if C==1:
			img=np.zeros(((N+7)//8*8, (M+7)//8*8))
			for i in range(N):
				try:
					line=[int(x) for x in fin.readline().split()]
				except:
					print("\033[31;01mPrea putine linii in fisierul de intrare.\033[0m")
					exit(1)
				if len(line)!=M:
					print(f"\033[31;01mPrea putine elemente pe linia {i+2}.\033[0m")
					exit(1)
				img[i, :M]=np.array(line)
		elif C==3:
			img=np.zeros(((N+7)//8*8, (M+7)//8*8, 3))
			for i in range(N):
				try:
					line=[int(x) for x in fin.readline().split()]
				except:
					print("\033[31;01mPrea putine linii in fisierul de intrare.\033[0m")
					exit(1)
				if len(line)!=M*3:
					print(f"\033[31;01mPrea putine elemente pe linia {i+2}.\033[0m")
					exit(1)
				img[i, :M, :]=np.array(line).reshape((-1, 3))
		else:
			print("\033[31;01mNumarul de canale din fisier nu corespunde unei valori acceptate (1, 3)\033[0m")
			exit(1)
	return N, M, C, img


def encode(parameters):
	N, M, C, img=readInput(parameters)

	ans=bitstringToBytes(int8_16ToBinary(N)+int8_16ToBinary(M)+int8_16ToBinary(C)+int8_16ToBinary(parameters["Q"]))
	if C==1:
		for lin in range(0, img.shape[0], 8):
			for col in range(0, img.shape[1], 8):
				block=img[lin:lin+8, col:col+8].copy()
				ans+=encodeBlock(block, parameters)
	elif C==3:
		for lin in range(0, img.shape[0], 8):
			for col in range(0, img.shape[1], 8):
				block=img[lin:lin+8, col:col+8, :].copy()
				ans+=encodeBlock(block, parameters)
	else:
		# Nu ar trebui sa se poata ajunge aici dar cine stie?
		print(f"How did we get here? {C=}")
	with open(parameters["O"] if "O" in parameters else "img.myjpeg", "wb") as f:
		f.write(ans)


def main():
	precalcZigZag()
	parameters=parseParameters()
	if type(parameters)==str:
		print(f"A avut loc o eroare la citirea parametrilor.\nEroare: \033[31;01m{parameters}\033[0m")
		return

	if not ("file" in parameters and os.path.isfile(parameters["file"])):
		print("\033[31;01mNu am primit un fisier pe care sa il comprim.\033[0m")
		return

	encode(parameters)


if __name__=="__main__":
	main()
