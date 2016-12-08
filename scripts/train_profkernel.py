import sys
import math
import os.path
import re
import subprocess

#python2.7 train_profkernel.py /mnt/project/pp2_1617/xna_raharjaschmidt split 3 rna /mnt/project/pp2_1617/xna_raharjaschmidt/profkernel_models

training_data_dir = sys.argv[1]
training_prefix = sys.argv[2]
number_splits = int(sys.argv[3])
training_infix = sys.argv[4]
training_output_dir = sys.argv[5]

for i in range(0, number_splits):
	fasta_file = os.path.join(training_data_dir, training_prefix + '.' + str(i) + '.' + training_infix + '.fasta')
	profile_file = os.path.join(training_data_dir, training_prefix + '.' + str(i) + '.' + training_infix + '.profile')
	class_file = os.path.join(training_data_dir, training_prefix + '.' + str(i) + '.' + training_infix + '.class.list')

	for k in range(3, 8):
		for s in range(2, k-1):
			out_dir = os.path.join(training_output_dir, training_prefix + '.' + str(i) + '.' + training_infix + '.k' + str(k) + 's' + str(s))
			subprocess.call(['mkdir', out_dir])		
			subprocess.call(['profkernel_workflow', '-f', fasta_file, '-p', profile_file, '-l', class_file, '-o', out_dir, '-k', k, '-s', s])