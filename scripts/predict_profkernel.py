import sys
import math
import os.path
import re
import subprocess

data_dir = sys.argv[1]
prefix = sys.argv[2]
number_splits = int(sys.argv[3])
infix = sys.argv[4]
model_dir = sys.argv[5]
out_dir = sys.argv[6]

for i in range(0, number_splits):
	fasta_file = os.path.join(training_data_dir, training_prefix + '.' + str(i) + '.' + training_infix + '.fasta')
	profile_file = os.path.join(training_data_dir, training_prefix + '.' + str(i) + '.' + training_infix + '.profile')

	for j in range (0, number_splits):
		for s in range(3, 9):
			for k in range(2, s):
				model_path = os.path.join(model_dir, prefix + '.i' + str(i) + '.j' + str(j) + . + infix + '.k' + str(k) + 's' + str(s))
				if j != i and if os.path.isdir(model_path):
					out_file = os.path.join(out_dir, prefix + '.' + str(j) + . + infix + '.k' + str(k) + 's' + str(s))
					print ' '.join(['profkernel_workflow', '-f', fasta_file, '-p', profile_file, '-m', model_path, '-o', out_file])
					subprocess.call(['profkernel_workflow', '-f', fasta_file, '-p', profile_file, '-m', model_path, '-o', out_file])