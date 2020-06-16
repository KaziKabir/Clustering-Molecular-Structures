
out = open('onedtja_CA_5000.txt', 'a+')
out.truncate()

with open('1dtja_models_5000.pdb') as f: #pdb file having the tertiary structures
	for line in f:
		words = line.split()
		if words[0] == 'MODEL':
			out.write('222') # values for the CA coordinates per structure/model (74*3)
		if len(words) > 2 and words[2] == 'CA': # line with CA coorniates
			out.write(' ' + words[6] + ' ' + words[7] + ' ' + words[8])
		if ('TER' or 'ENDMDL') in words:
			out.write('\n')
out.close()
