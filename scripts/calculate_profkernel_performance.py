import sys
import math
import os.path
import re
import subprocess

#python2.7 calculate_profkernel_performance.py /mnt/project/pp2_1617/xna_raharjaschmidt /mnt/project/pp2_1617/xna_raharjaschmidt/profkernel_predictions split 3 dna /mnt/project/pp2_1617/xna_raharjaschmidt/performance_dna.tsv

classes_dir = sys.argv[1]
prediction_dir = sys.argv[2]
prefix = sys.argv[2]
number_splits = int(sys.argv[3])
infix = sys.argv[4]
out_file = sys.argv[6]

out = open(out_file, 'w')
out.write('\tAccurracy\tSensitivity\tSpecificty\tF1')

for i in range(0, number_splits):
	classes_file = os.path.join(classes_dir, prefix + '.' + i + '.' + infix + '.class.list')
	classes_lines = open(classes_file).readlines()
	classes = {}
	curId = ''
	for line in classes_lines:
		if line.startswith('>'):
			curId = line[1:]
		else:
			classes[curId] = line
	for j in range(0, number_splits):
		for s in range(3, 9):
			for k in range(2, s):
				tp = 0
				fp = 0
				tn = 0
				fn = 0
				prediction_file = os.path.join(prediction_dir, prefix + '.i' + str(i) +  '.j' + str(j) + '.' + infix + '.k' + str(k) + 's' + str(s))
				prediction_lines = open(prediction_file, 'r').readlines()[2:]
				prediction = {}
				for line in prediction_lines:
					split = line.split('\t')
					prediction{split[0]} = split[1]
					if split[1] == 'positive':
						if classes[split[0]] == 'positive':
							tp += 1
						else:
							fp += 1
					else:
						if classes[split[0]] == 'positive':
							fn += 1
						else:
							tn += 1
				if len(prediction_lines) > 0:
					accurracy = (tp + tn)/(tp + fp + fn + tn)
					sensitivity = tp/(tp + fn)
					specificty = tn(fp + tn)
					f1 = (2 * tp) / (2 * tp + fp + fn + tn)
					out.write(prefix + '.i' + str(i) +  '.j' + str(j) + '.' + infix + '.k' + str(k) + 's' + str(s)) + '\t' + accurracy + '\t' + sensitivity + '\t' + specificty + '\t' + f1)
out.close()