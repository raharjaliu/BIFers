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

#python2.7 predict_profkernel.py /mnt/project/pp2_1617/xna_raharjaschmidt split 3 dna /mnt/project/pp2_1617/xna_raharjaschmidt/profkernel_models /mnt/project/pp2_1617/xna_raharjaschmidt/profkernel_predictions

for i in range(0, number_splits):
	fasta_file = os.path.join(data_dir, prefix + '.' + str(i) + '.' + infix + '.fasta')
	print 'fasta_file: ' +  fasta_file
	profile_file = os.path.join(data_dir, prefix + '.' + str(i) + '.' + infix + '.profile')
	print 'profile_file: ' + profile_file

	for j in range (0, number_splits):
		for s in range(3, 9):
			for k in range(2, s):
				model_path = os.path.join(model_dir, prefix + '.' + str(j) + '.' + infix + '.k' + str(k) + 's' + str(s))
				print 'model_path: ' + model_path
				if j != i and os.path.isdir(model_path):
					out_file = os.path.join(out_dir, prefix + '.i' + str(i) +  '.j' + str(j) + '.' + infix + '.k' + str(k) + 's' + str(s))
					print ' '.join(['profkernel-workflow', '-f', fasta_file, '-p', profile_file, '-m', model_path, '-o', out_file])
					subprocess.call(['profkernel-workflow', '-f', fasta_file, '-p', profile_file, '-m', model_path, '-o', out_file])
