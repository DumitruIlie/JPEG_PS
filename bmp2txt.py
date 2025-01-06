# Ilie Dumitru

import matplotlib.pyplot as plt
import numpy as np
import sys

def main():
	img=plt.imread(sys.argv[-1])

	if len(img.shape) not in  {2, 3}:
		raise Exception("Image shape not ok")
	if len(img.shape)==2:
		N, M=img.shape
		print(N, M, 1)
		for i in range(N):
			print(*(img[i]*255).astype(np.uint8))
	elif img.shape[2]>2:
		N, M, C=img.shape
		print(N, M, 3)
		for i in range(N):
			print(*(img[i, :, :3].reshape(-1)*255).astype(np.uint8))


if __name__=="__main__":
	main()
