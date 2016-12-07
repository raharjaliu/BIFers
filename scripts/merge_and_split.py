import sys
import math
import os.path
import re

def split_files(pos_dir_path, neg_dir_path, out_path, part_holdout, split_num, infix):

	# preprocess positive paths
	pos_fastas = [os.path.join(pos_dir_path, d) for d in os.listdir(pos_dir_path) 
					if os.path.isfile(os.path.join(pos_dir_path, d)) and 'fasta' in d and not d.endswith('pssm')]
	pos_fastas = {re.findall(r'\d+', q)[-1]: q for q in pos_fastas}
	pos_pssms = [os.path.join(pos_dir_path, d) for d in os.listdir(pos_dir_path) 
					if os.path.isfile(os.path.join(pos_dir_path, d)) and 'fasta' in d and d.endswith('pssm')]
	pos_pssms = {re.findall(r'\d+', q)[-1]: q for q in pos_pssms}
	pos = [(pos_fastas[q], pos_pssms[q]) for q in pos_fastas.keys() if q in pos_pssms.keys()]
	print "#" * 100
	print infix + " POS SET ALL"
	print len(pos)

	# preprocess negative paths
	neg_fastas = [os.path.join(neg_dir_path, d) for d in os.listdir(neg_dir_path) 
					if os.path.isfile(os.path.join(neg_dir_path, d)) and 'fasta' in d and not d.endswith('pssm')]
	neg_fastas = {re.findall(r'\d+', q)[-1]: q for q in neg_fastas}
	neg_pssms = [os.path.join(neg_dir_path, d) for d in os.listdir(neg_dir_path) 
					if os.path.isfile(os.path.join(neg_dir_path, d)) and 'fasta' in d and d.endswith('pssm')]
	neg_pssms = {re.findall(r'\d+', q)[-1]: q for q in neg_pssms}
	neg = [(neg_fastas[q], neg_pssms[q]) for q in neg_fastas.keys() if q in neg_pssms.keys()]

	print "#" * 100
	print infix + " NEG SET ALL"
	print len(neg)

	# defined positive holdout and training set
	pos_end_holdout = int(len(pos) * part_holdout)
	pos_holdout = pos[:pos_end_holdout]
	pos_split = pos[pos_end_holdout:]

	# split positive set
	pos_splits = {}
	split_sizes = []
	for this_split in range(split_num):
		split_sizes.append(len(pos_split) / split_num)
	for this_split in range(len(pos_split) % split_num):
		split_sizes[this_split] += 1
	for this_split in range(split_num):
		pos_splits[this_split] = pos_split[(this_split * split_sizes[this_split]):
									min(len(pos_split), (this_split + 1) * split_sizes[this_split])]


	print "#" * 100
	print infix + " POS SPLIT ALL"
	print [len(pos_splits[q]) for q in pos_splits.keys()]

	# defined negative holdout and training set
	neg_end_holdout = int(len(neg) * part_holdout)
	neg_holdout = neg[:neg_end_holdout]
	neg_split = neg[neg_end_holdout:]

	# split negative set
	neg_splits = {}
	split_sizes = []
	for this_split in range(split_num):
		split_sizes.append(len(neg_split) / split_num)
	for i in range(len(neg_split) % split_num):
		split_sizes[i] += 1
	for this_split in range(split_num):
		neg_splits[this_split] = neg_split[(this_split * split_sizes[this_split]):
									min(len(neg_split), (this_split + 1) * split_sizes[this_split])]

	print "#" * 100
	print infix + " NEG SPLIT ALL"
	print [len(neg_splits[q]) for q in neg_splits.keys()]

	# combine positive and negative holdout sets and write files
	pos_id = '\n'.join([(open(q[0], 'r').read().split('\n')[0].split(' ')[0][1:] + '\npositive') for q in pos_holdout])
	neg_id = '\n'.join([(open(q[0], 'r').read().split('\n')[0].split(' ')[0][1:].split('|')[1] + '\nnegative') for q in neg_holdout])
	holdout_id = pos_id + '\n' + neg_id

	## read and merge both fasta and profile string for positive and negative set
	holdout_string_pos = '\n'.join([(open(q[0], 'r').read()[:-1] + '\n' + open(q[1], 'r').read()[:-1]) for q in pos_holdout])
	holdout_string_neg = '\n'.join([('>' + open(q[0], 'r').read()[:-1].split('\n')[0].split(' ')[0].split('|')[1] + 
										'\n' + open(q[0], 'r').read()[:-1].split('\n')[1] + 
										'\n' + open(q[1], 'r').read()[:-1]) for q in neg_holdout])
	holdout_string = holdout_string_pos + '\n' + holdout_string_neg

	## read and merge fasta string for positive and negative set
	holdout_string_fasta_pos = '\n'.join([(open(q[0], 'r').read()[:-1]) for q in pos_holdout])
	holdout_string_fasta_neg = '\n'.join([('>' + open(q[0], 'r').read()[:-1].split('\n')[0].split(' ')[0].split('|')[1] + 
											'\n' + open(q[0], 'r').read()[:-1].split('\n')[1]) for q in neg_holdout])
	holdout_string_fasta = holdout_string_fasta_pos + '\n' + holdout_string_fasta_neg

	## read and merge profile string for positive and negative set
	holdout_string_profiles_pos = '\n'.join([(open(q[0], 'r').read().split('\n')[0].split(' ')[0] + 
												'\n' +open(q[1], 'r').read()[:-1]) for q in pos_holdout])
	holdout_string_profiles_neg = '\n'.join([('>' + open(q[0], 'r').read()[:-1].split('\n')[0].split(' ')[0].split('|')[1] + 
												'\n' + open(q[1], 'r').read()[:-1]) for q in neg_holdout])
	holdout_string_profiles = holdout_string_profiles_pos + '\n' + holdout_string_profiles_neg

	# holdout = pos_holdout + neg_holdout
	# holdout_string = '\n'.join([(open(q[0], 'r').read()[:-1] + '\n' + open(q[1], 'r').read()[:-1]) for q in holdout])
	# holdout_string_fasta = '\n'.join([(open(q[0], 'r').read()[:-1]) for q in holdout])
	# holdout_string_profiles = '\n\n'.join([(open(q[0], 'r').read().split('\n')[0].split(' ')[0] + '\n' + open(q[1], 'r').read()[:-1]) for q in holdout])

	holdout_file = open(os.path.join(out_path, 'holdout.' + infix) ,'w')
	holdout_file.write(holdout_string)
	holdout_file.close()
	holdout_file_fasta = open(os.path.join(out_path, 'holdout.' + infix + '.fasta') ,'w')
	holdout_file_fasta.write(holdout_string_fasta)
	holdout_file_fasta.close()
	holdout_file_profile = open(os.path.join(out_path, 'holdout.' + infix + '.profile') ,'w')
	holdout_file_profile.write(holdout_string_profiles)
	holdout_file_profile.close()
	holdout_pos_list = open(os.path.join(out_path, 'holdout.' + infix + '.pos.list') ,'w')
	holdout_pos_list.write(pos_id)
	holdout_pos_list.close()
	holdout_neg_list = open(os.path.join(out_path, 'holdout.' + infix + '.neg.list') ,'w')
	holdout_neg_list.write(neg_id)
	holdout_neg_list.close()
	holdout_neg_list = open(os.path.join(out_path, 'holdout.' + infix + '.class.list') ,'w')
	holdout_neg_list.write(holdout_id)
	holdout_neg_list.close()

	for split in pos_splits.keys():

		print split

		pos_id = '\n'.join([('>' + open(q[0], 'r').read().split('\n')[0].split(' ')[0][1:] + '\npositive') for q in pos_splits[split]])
		neg_id = '\n'.join([('>' + open(q[0], 'r').read().split('\n')[0].split(' ')[0][1:].split('|')[1] + '\nnegative') for q in neg_splits[split]])
		class_id = pos_id + '\n' + neg_id

		## read and merge both fasta and profile string for positive and negative set
		this_split_string_pos = '\n'.join([(open(q[0], 'r').read()[:-1] + '\n' + open(q[1], 'r').read()[:-1]) for q in pos_splits[split]])
		this_split_string_neg = '\n'.join([('>' + open(q[0], 'r').read()[:-1].split('\n')[0].split(' ')[0].split('|')[1] + 
											'\n' + open(q[0], 'r').read()[:-1].split('\n')[1] + 
											'\n' + open(q[1], 'r').read()[:-1]) for q in neg_splits[split]])
		this_split_string = this_split_string_pos + '\n' + this_split_string_neg

		## read and merge fasta string for positive and negative set
		this_split_string_fasta_pos = '\n'.join([(open(q[0], 'r').read()[:-1]) for q in pos_splits[split]])
		this_split_string_fasta_neg = '\n'.join([('>' + open(q[0], 'r').read()[:-1].split('\n')[0].split(' ')[0].split('|')[1] + 
													'\n' + open(q[0], 'r').read()[:-1].split('\n')[1]) for q in neg_splits[split]])
		this_split_string_fasta = this_split_string_fasta_pos + '\n' + this_split_string_fasta_neg

		## read and merge profile string for positive and negative set
		this_split_string_profiles_pos = '\n'.join([(open(q[0], 'r').read().split('\n')[0].split(' ')[0] + 
														'\n' + open(q[1], 'r').read()[:-1]) for q in pos_splits[split]])
		this_split_string_profiles_neg = '\n'.join([('>' + open(q[0], 'r').read()[:-1].split('\n')[0].split(' ')[0].split('|')[1] + 
														'\n' + open(q[1], 'r').read()[:-1]) for q in neg_splits[split]])
		this_split_string_profiles = this_split_string_profiles_pos + '\n' + this_split_string_profiles_neg

		# this_split = pos_splits[split] + neg_splits[split]
		# this_split_string = '\n'.join([(open(q[0], 'r').read()[:-1] + '\n' + open(q[1], 'r').read()[:-1]) for q in this_split])
		# this_split_string_fasta = '\n'.join([(open(q[0], 'r').read()[:-1]) for q in this_split])
		# this_split_string_profiles = '\n\n'.join([(open(q[0], 'r').read().split('\n')[0].split(' ')[0] + '\n' + open(q[1], 'r').read()[:-1]) for q in this_split])
		
		this_split_file = open(os.path.join(out_path, 'split.' + str(split) + '.' + infix) ,'w')
		this_split_file.write(this_split_string)
		this_split_file.close()
		this_split_file_fasta = open(os.path.join(out_path, 'split.' + str(split) + '.' + infix + '.fasta') ,'w')
		this_split_file_fasta.write(this_split_string_fasta)
		this_split_file_fasta.close()
		this_split_file_profile = open(os.path.join(out_path, 'split.' + str(split) + '.' + infix + '.profile') ,'w')
		this_split_file_profile.write(this_split_string_profiles)
		this_split_file_profile.close()
		this_split_pos_list = open(os.path.join(out_path, 'split.' + str(split) + '.' + infix + '.pos.list') ,'w')
		this_split_pos_list.write(pos_id)
		this_split_pos_list.close()
		this_split_neg_list = open(os.path.join(out_path, 'split.' + str(split) + '.' + infix + '.neg.list') ,'w')
		this_split_neg_list.write(neg_id)
		this_split_neg_list.close()
		this_split_class_list = open(os.path.join(out_path, 'split.' + str(split) + '.' + infix + '.class.list') ,'w')
		this_split_class_list.write(class_id)
		this_split_class_list.close()


if  __name__ =='__main__':

	## merge_and_split.py /mnt/project/pp2_1617/data/xna/splitDNA/ /mnt/project/pp2_1617/data/xna/splitNegativeHumanReduced/ /mnt/project/pp2_1617/data/xna/ppRNA/ /mnt/project/pp2_1617/data/xna/splitNegativeHumanReduced/ /mnt/project/pp2_1617/xna_raharjaschmidt/ 0.1 3

	dna_pos_set_path = sys.argv[1]
	dna_neg_set_path = sys.argv[2]
	rna_pos_set_path = sys.argv[3]
	rna_neg_set_path = sys.argv[4]
	out_path = sys.argv[5]
	part_holdout = float(sys.argv[6])
	split_num = int(sys.argv[7])

	print (dna_pos_set_path, 
		dna_neg_set_path, 
		rna_pos_set_path,
		rna_neg_set_path,
		part_holdout,
		split_num)

	split_files(dna_pos_set_path, dna_neg_set_path, out_path, part_holdout, split_num, 'dna')
	split_files(rna_pos_set_path, rna_neg_set_path, out_path, part_holdout, split_num, 'rna')





