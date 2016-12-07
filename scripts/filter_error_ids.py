import sys
import math
import os.path
import re

files_to_filter = [os.path.join(data_path, d) for d in os.listdir(data_path) 
					if os.path.isfile(os.path.join(data_path, d)) and 'fasta' in d or 'profile' in d or 'class.list' in d]

error_ids = set(open(error_ids_file, 'r').read().split('\n'))

print error_ids

for file in files_to_filter:
	out = ''
	exclude = False
	for line in open(file, 'r').readLines():
		if line.startsWith('>'):
			id = line.substring(1)
			print id
			if id in error_ids:
				exclude = True
				print "exclude" + line.substring(1)
			else:
				exclude = False
				out += line + '\n'
		else:
			if not exclude:
				out += line + '\n'

	out_file = open(file + '_filtered', w)
	out_file.write(out)
	out_file.close
