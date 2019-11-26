
out = open('native_1dtja.txt', 'a+')
out.truncate()

with open('1dtja_native.pdb') as f:
	for line in f:
		words = line.split()
		if len(words) > 2 and words[2] == 'CA': # line with CA coorniates
			out.write(' ' + words[6] + ' ' + words[7] + ' ' + words[8])
		if ('TER' or 'ENDMDL') in words:
			out.write('\n')
out.close()
