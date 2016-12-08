import sys
import math
import os.path
import re
import random
import numpy as np

def check_difference_and_return_entities(data_path, pp_path):

	# list down available data in both sets
	data = [d for d in os.listdir(data_path)
					if os.path.isfile(os.path.join(data_path, d)) and 'pssm' in d]
	dirs = [d for d in os.listdir(pp_path) 
					if os.path.isdir(os.path.join(pp_path, d))]

	print "RAW DATA:"
	print data
	print "SIZE RAW DATA:"
	print len(data)
	print "RAW PP:"
	print dirs
	print "SIZE PP:"
	print len(dirs)

	# extract id in both sets
	data = [re.findall(r'\d+', q)[-1] for q in data]
	dirs = [re.findall(r'\d+', q)[-1] for q in dirs]

	print "FILE INDEX DATA:"
	print data
	print "FILE INDEX PP:"
	print dirs

	# normalize into int
	data = [int(q) for q in data]
	data.sort()
	dirs = [int(q) for q in dirs]
	dirs.sort()

	print "INT DATA SORTED:"
	print data
	print "INT PP SORTED:"
	print dirs	

	# convert list to set and calculate set diffs
	data = set(data)
	dirs = set(dirs)

	print "DATA DIFF PP"
	print data.difference(dirs)
	print "PP DIFF DATA"
	print dirs.difference(data)

	return list(dirs)


def split_list(this_list, split_num):

	splits = {}
	split_sizes = []

	for this_split in range(split_num):
		split_sizes.append(len(this_list) / split_num)
	for this_split in range(len(this_list) % split_num):
		split_sizes[this_split] += 1
	for this_split in range(split_num):
		splits[this_split] = this_list[(this_split * split_sizes[this_split]):
									min(len(this_list), (this_split + 1) * split_sizes[this_split])]

	return splits

def create_arff(index, fold):

	out = '@RELATION classfile.arff\n' + \
			'@ATTRIBUTE pos NUMERIC\n' + \
			'@ATTRIBUTE fold NUMERIC\n' + \
			'@ATTRIBUTE class {+,-}\n' + \
			'\n' + \
			'@DATA\n'

	string = {}

	binding = np.array(['-'] * index.size)
	binding[index] = '+'
	binding = list(binding)

	pos = list(np.array(range(len(binding))) + 1)

	zipped = zip(pos, binding)

	out = out + '\n'.join([str(q[0]) + ',' + str(fold) + ',' + q[1] for q in zipped])

	return out

def extract_consensus(entry):

	entries = entry.split('\n')[1:]
	entries = [q.split('\t')[3] for q in entries]
	entries = [np.array(list(q)) for q in entries]

	consensus = np.array([False] * len(entries[0]))

	for entry in entries:
		consensus = consensus | (entry == '!')

	return consensus

def extract_feature_and_write(binding_path, pp_path, split_size):

	binding = open(binding_path, 'r').read().split('\n$$\n')[:-1]
	binding_dict = {q.split('\n')[0].split('\t')[1]: extract_consensus(q) for q in binding}

	reduced = [d for d in os.listdir(pp_path) if os.path.isdir(os.path.join(pp_path, d))]
	reduced_dict = {q: binding_dict[q] for q in reduced}

	# print dna_reduced_dict
	reduced_splits = split_list(reduced_dict.keys(), split_size)

	results = {}

	for split in reduced_splits.keys():
		this_keys = reduced_splits[split]
		for key in this_keys:
			results[key] = create_arff(binding_dict[key], split)

	# print dna_binding_dict
	# print dna_results
	for key in results.keys():

		this_arff = open(os.path.join(pp_path, key, 'classfile.arff'), 'w')
		this_arff.write(results[key])
		this_arff.close()


if  __name__ =='__main__':

	"""
	How to exract features from PP results:
	1.) call this script:
	create_arff.py /mnt/project/pp2_1617/data/xna/splitDNA/ /mnt/project/pp2_1617/data/xna/ppDNA/ /mnt/project/pp2_1617/data/xna/splitRNA/ /mnt/project/pp2_1617/data/xna/ppRNA/ /mnt/project/pp2_1617/xna_raharjaschmidt/machine_learning/ 3

	2.) call pp features
	python2.7 pp2features.py -p /mnt/project/pp2_1617/xna_raharjaschmidt/machine_learning/ppDNA2/ -a classfile.arff -f /mnt/project/pp2_1617/xna_raharjaschmidt/machine_learning/pp2features.config --arff-file=/mnt/project/pp2_1617/xna_raharjaschmidt/machine_learning/dna.arff
	python2.7 pp2features.py -p /mnt/project/pp2_1617/xna_raharjaschmidt/machine_learning/ppRNA2/ -a classfile.arff -f /mnt/project/pp2_1617/xna_raharjaschmidt/machine_learning/pp2features.config --arff-file=/mnt/project/pp2_1617/xna_raharjaschmidt/machine_learning/rna_big.arff
	"""

	dna_binding_path = sys.argv[1]
	dna_pp_path = sys.argv[2]
	rna_binding_path = sys.argv[3]
	rna_pp_path = sys.argv[4]
	split_size = int(sys.argv[5])

	extract_feature_and_write(dna_binding_path, dna_pp_path, split_size)
	extract_feature_and_write(rna_binding_path, rna_pp_path, split_size)