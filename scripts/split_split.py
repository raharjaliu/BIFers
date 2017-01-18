import sys
import math
import os.path
import re
import subprocess

#python2.7 split_split.py /mnt/project/pp2_1617/xna_raharjaschmidt split.0.dna /mnt/project/pp2_1617/xna_raharjaschmidt/test_splits 64

split_dir = sys.argv[1]
split_name = sys.argv[2]
out_dir = sys.argv[3]
subsplit_size = int(sys.argv[4])

fasta_file = os.path.join(split_dir, split_name + '.fasta')
profile_file = os.path.join(split_dir, split_name + '.profile')
class_file = os.path.join(split_dir, split_name + '.class.list')

fasta_lines = open(fasta_file, 'r').readlines()
subsplit_nr = 0
current_proteins = 0
subsplit_fasta = ''
for line in fasta_lines:
	if line.startswith('>'):
		if current_proteins == subsplit_size:
			open(os.path.join(out_dir, split_name + '.' + str(subsplit_nr) + '.fasta'), 'w').write(subsplit_fasta)
			current_proteins = 1
			subsplit_fasta = ''
			subsplit_nr += 1
		else:
			current_proteins += 1
	subsplit_fasta += line

open(os.path.join(out_dir, split_name + '.' + str(subsplit_nr) + '.fasta'), 'w').write(subsplit_fasta)

subsplit_nr = 0
current_proteins = 0
subsplit_profile = ''
profile_lines = open(profile_file, 'r').readlines()
for line in profile_lines:
        if line.startswith('>'):
                if current_proteins == subsplit_size:
       	        	open(os.path.join(out_dir, split_name + '.' + str(subsplit_nr) + '.profile'), 'w').write(subsplit_profile)
               		current_proteins = 1
               		subsplit_profile = ''
               		subsplit_nr += 1
           	else:
                       	current_proteins += 1
        subsplit_profile += line

open(os.path.join(out_dir, split_name + '.' + str(subsplit_nr) + '.profile'), 'w').write(subsplit_profile)

class_lines = open(class_file, 'r').readlines()
subsplit_nr = 0
current_proteins = 0
subsplit_class = ''
for line in class_lines:
	if line.startswith('>'):
		if current_proteins == subsplit_size:
        		open(os.path.join(out_dir, split_name + '.' + str(subsplit_nr) + '.class.list'), 'w').write(subsplit_class)
        	        current_proteins = 1
               		subsplit_class = ''
             		subsplit_nr += 1
	        else:
        	        current_proteins += 1
        	subsplit_class += line + str(current_proteins < subsplit_size/2) + '\n'

open(os.path.join(out_dir, split_name + '.' + str(subsplit_nr) + '.class.list'), 'w').write(subsplit_class)

for i in range(0, subsplit_nr):
	fasta_file = os.path.join(out_dir, split_name + '.' + str(i) + '.fasta')
        profile_file = os.path.join(out_dir, split_name + '.' + str(i) + '.profile')
        class_file = os.path.join(out_dir, split_name + '.' + str(i) + '.class.list')
	model_dir = os.path.join(out_dir, 'model' + str(i))
	subprocess.call(['mkdir', model_dir])
	args = ['profkernel-workflow', '-f', fasta_file, '-p', profile_file, '-l', class_file, '-o', model_dir]
	print ' '.join(args)
	subprocess.call(args)



