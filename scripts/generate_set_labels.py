#!/usr/bin/python

import sys
import math
import os.path
import re

pos_list_file = sys.argv[1] + ".pos.list"
neg_list_file = sys.argv[1] + ".neg.list"
classes_files = sys.argv[1] + ".classes"

pos_list =  open(pos_list_file, 'r').read().split('\n')
neg_list =  open(neg_list_file, 'r').read().split('\n')

classes_out = open(classes_files, 'w')
for prot in pos_list:
	acc = prot.split('\t')[0]
	classes_out.write('>' + acc + '\npositive\n')

for prot in neg_list:
	acc = prot.split('|')[1]
	classes_out.write('>' + acc + '\nnegatvie\n')

classes_out.close()
