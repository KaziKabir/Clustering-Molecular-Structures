import numpy as np
from Bio.SVDSuperimposer import SVDSuperimposer
from numpy import array, dot

sup = SVDSuperimposer()

samples = []
refs = []

rmsd = open('1dtja_rmsd_5000.txt', 'a+')
rmsd.truncate()

with open('native_1dtja.txt') as n:
	for line in n:
		l = [float(t) for t in line.split()]
		refs = [l[i:i+3] for i in range(0, len(l), 3)]

x = array(refs, 'f')



with open('onedtja_CA_5000.txt') as f:
	for line in f:
		l = [float(t) for t in line.split()]
		l = l[1:]
		samples = [l[i:i+3] for i in range(0, len(l), 3)]
		y = array(samples, 'f')

		sup.set(x, y)
		sup.run()
		rms = sup.get_rms()
		rmsd.write(str(rms) + '\n')


rmsd.close()
