import sys
import os

def get_mapping(reduced_file):

	reduced = open(reduced_file, 'r').read().split('>')[1:]

	mapping = {}
	counter = 1

	for entry in reduced:

		mapping[counter] = entry.split('\n')[0]
		counter += 1

	return mapping

'''
Rename ppXNA subdirectories from ordering number to gene id
'''	
if  __name__ =='__main__':

	## rename_directory.py /mnt/project/pp2_1617/xna_raharjaschmidt/dna_reduced.fasta /mnt/project/pp2_1617/xna_raharjaschmidt/rna_reduced.fasta /mnt/project/pp2_1617/xna_raharjaschmidt/machine_learning/ppDNA2/ /mnt/project/pp2_1617/xna_raharjaschmidt/machine_learning/ppRNA2/

	dna_reduced = sys.argv[1]
	rna_reduced = sys.argv[2]
	dna_pp_top_path = sys.argv[3]
	rna_pp_top_path = sys.argv[4]

	dna_mapping = get_mapping(dna_reduced)
	dna_subdirs = [q for q in os.listdir(dna_pp_top_path) if os.path.isdir(os.path.join(dna_pp_top_path, q))]
	dna_subdirs_mapped = [dna_mapping[int(q)] for q in dna_subdirs]
	dna_zipped = zip(dna_subdirs, dna_subdirs_mapped)

	rna_mapping = get_mapping(rna_reduced)
	rna_subdirs = [q for q in os.listdir(rna_pp_top_path) if os.path.isdir(os.path.join(rna_pp_top_path, q))]
	rna_subdirs_mapped = [rna_mapping[int(q)] for q in rna_subdirs]
	rna_zipped = zip(rna_subdirs, rna_subdirs_mapped)	

	map(lambda x: os.rename(os.path.join(dna_pp_top_path, x[0]), os.path.join(dna_pp_top_path, x[1])), dna_zipped)
	map(lambda x: os.rename(os.path.join(rna_pp_top_path, x[0]), os.path.join(rna_pp_top_path, x[1])), rna_zipped)

