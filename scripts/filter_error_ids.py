import sys
import math
import os.path
import re

data_path = sys.argv[1]
error_ids_file = sys.argv[2]

files_to_filter = [os.path.join(data_path, d) for d in os.listdir(data_path) 
					if os.path.isfile(os.path.join(data_path, d)) and 'split' in d and ('fasta' in d or 'profile' in d or 'class.list' in d) and not 'filtered' in d]

error_ids = set(open(error_ids_file, 'r').read().split('\n'))
print error_ids

for file in files_to_filter:
	print file
	out = ''
	exclude = False
	for line in open(file, 'r').readlines():
		if line.startswith('>'):
			id = line[1:]
			if id in error_ids:
				exclude = True
				print "exclude: " + line[1:]
			else:
				exclude = False
				out += line
		else:
			if not exclude:
				out += line

	out_file = open(file + '_filtered', 'w')
	out_file.write(out)
	out_file.close
