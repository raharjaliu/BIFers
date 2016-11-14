#!/usr/bin/python

from os.path import isfile

if len(sys.argv) < 4 or not isfile(sys.argv[1]) or not isfile(sys.argv[2]):
	print "Usage: generate_negative_set.py <sequences.fasta> <excluded_genes.csv> <output.fasta>";
	sys.exit();

fasta_file = sys.argv[1];
go_file = sys.argv[2];
negative_fasta = sys.argv[3];

excluded_genes = set();
with open(go_file, 'rb') as go:
	lines = go.readlines();
	for line in lines:
		excluded_genes.add(line[:-2]);

print "genes to exclude: " + str(len(excluded_genes));

out = open(negative_fasta, 'w');
with open(fasta_file, 'rb') as fasta:
	lines = fasta.readlines();
	id_line = "";
	id = ""
	sequence = "";
	exclude = True;
	for line in lines:
		if line.startswith(">"):
			if not exclude:
				out.write(id_line + sequence + "\n");
			id_line = line;
			sequence = "";
			id = id_line.split("|")[2].split("_")[0]
			if id in excluded_genes:
				exclude = True;
			else:
				exclude = False;
		else:
			sequence += line[:-2];

	if not exclude:
		out.write(id_line + sequence + "\n");

out.close();
