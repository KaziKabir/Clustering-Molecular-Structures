import numpy as np
import xml.etree.ElementTree as ET
from Bio.SVDSuperimposer import SVDSuperimposer
from math import sqrt
from numpy import array, dot
import random
import operator
import os
import sys
import pickle
from sklearn.decomposition import PCA
import math
import scipy.io
import matplotlib.pyplot as plt


def align(coordinate_file):
	'''
	1. Input: File contains lines, where each line contains the coordinates of a model,
	e.g., if model 1 has 70 atoms, each with 3 coordinates  (3*70 = 210 coordinates),
	then the line corresponding model 1 is like this:  210 x1 y1 z1 x2 y2 z2 ... x70 y70 z70

	2. Alignes all the model with the first model in the cordinate_file.

	3. Returns: a dictionary of aligned models. Each model, i.e., each entry (value)
	in the dictionary is a flattened numpy array.

	'''

	modelDict = {}
	ind = 0
	ref = []
	sup = SVDSuperimposer()
	with open(coordinate_file) as f:
		for line in f:
			if ind == 0:
				l = [float(t) for t in line.split()]
				l = l[1:]
				samples = [l[i:i+3] for i in range(0, len(l), 3)]
				ref = array(samples, 'f')

				modelDict[ind] = np.ravel(ref)
				ind += 1
			else:
				l = [float(t) for t in line.split()]
				l = l[1:]
				samples = [l[i:i+3] for i in range(0, len(l), 3)]
				seq = array(samples, 'f')
				s = sup.set(ref, seq)
				sup.run()
				z = sup.get_transformed()
				modelDict[ind] = np.ravel(z)
				ind += 1
	return modelDict, ref




def center(aligned_dict):
	'''
	1. input: a dictionary where each value is a model in the form of a flattened array,
	and each array contains the coordinates of the atoms of that model.

	2. Method:
		a. Constructs an m by n array where m is the total number of coorniates of
		all atoms (e.g., for 1ail with 70 atoms,  m = 70 * 3 = 270), and n is the number of models

		b. returns: the centered array, i.e., the result of the above method
	'''

	biglist = []
	for key, val in aligned_dict.items():
		biglist.append(val)
	data = np.array(biglist)
	data = data.T
	mean = data.mean(axis=1).reshape(-1, 1)
	data = data - data.mean(axis=1).reshape(-1, 1)
	return data, mean


def Eig(data):
	'''
	Input: Centerd or scaled data of size m by n. n = number of models, m = total number of coordinates in each model.
	Method:
		1. prepare the data: divides each element by sqrt(n-1)
		2. calculate the covariance matrix, which is a square matrix. Numpy's linalg.eig requires
		   a square matrix
		3. run numpy's linalg.eig on data
		4. collect the eigenvalues and eigenvectors
		5. Compute the projected data by multiplying the eigenvectors/principle_components with the data

	OUtputs:
		1. eigenvalues
		2. eigenvectors
		3. projected data
	'''
	#calculate the covariance matrix, which is a square matrix. Numpy's linalg.eig requires a square matrix
	n_minus_1 = data.shape[1]-1
	mult = np.dot(data, np.transpose(data))
	cov = np.divide(mult, n_minus_1)
	eigenvals, eigenvecs = np.linalg.eig(cov)
	idx = np.argsort(eigenvals)[::-1]
	eigenvals = eigenvals[idx]
	eigenvecs = eigenvecs[:, idx]
	eigenvecs_all = eigenvecs

	projected_data_eig1 = np.dot(eigenvecs.T, data)

	eigenvecs = eigenvecs[:, :5]    # retain the top 5 pcs
	projected_data_eig5 = np.dot(eigenvecs.T, data)
	return eigenvals, eigenvecs_all, projected_data_eig1, projected_data_eig5


def accSum(eigenvals):
	'''
	Input: eigenvalues as a 1D array or list
	Method: Divides each eigenvalue by the highest value in the list/array, then multiplies each of them with 100 to generate percentage of accumulated variances
	Output: returns the accumulated variances
	'''
	non_zero_eigvals = eigenvals[ 0 < eigenvals ]
	accSum = np.cumsum(non_zero_eigvals)
	accSum /= accSum[ accSum.shape[0] - 1 ]
	accSum *= 100
	return accSum


def main():
	'''
	Requires the location of the coordinate file.
	Each file contains lines, where each line contains the coordinates of a model, e.g., if model 1 has 70 atoms, each with 3 coordinates  (3*70 = 210 coordinates),
	then the line corresponding model 1 is like this:  210 x1 y1 z1 x2 y2 z2 ... x70 y70 z70

	'''
	coordinate_file = 'onedtja_CA_5000.txt'



	# align the models with the first one in the file. No need to call this function if already pickled to disk.

	aligned_dict, ref = align(coordinate_file)


	# center the data by subtracting the mean of the rows from each row element. No need to do it again if centered data is already pickled to disk.
	centered_data, mean = center(aligned_dict)


	# compute the eigenvalues and eigenvectors using numpy's linalg.eig
	eigenvalues, eigenvecs, projected_data_eig1, projected_data_eig5 = Eig(centered_data)
	accSum_eig = accSum(eigenvalues)
	#print(accSum_eig)

	var_5pcs = accSum_eig[4] # cumulative variance covered by first 5 pcs
	#print(var_5pcs)

	var = accSum_eig[0:25] # variance for first 25 pcs

	plt.plot(var, 'o-', color='darkblue')

	plt.xticks([i for i in range(0,25)], ['PC'+str(i+1) for i in range(0,25)], fontsize=12, rotation=90)

	plt.xlabel("Principal Components", fontsize=12)
	plt.ylabel("Cumulative Variance", fontsize=12)

	plt.axhline(y = var_5pcs, linestyle='--', color='red') # cumulative variance covered by first five pcs
	plt.axvline(x = 4, linestyle='--', color='green')

	#plt.show()

	plt.savefig('plot_CumVar_25pcs.png', orientation='landscape', figsize=(10,10), dpi = 600, transparent = True)

	projected_data_eig5 = projected_data_eig5.T

	five_pcs = projected_data_eig5

	with open('pc1-5_1dtja_5000.txt', 'w') as f:
		np.savetxt(f, five_pcs, delimiter = ' ', fmt='%1.8f')



if __name__ == '__main__':
	main()
