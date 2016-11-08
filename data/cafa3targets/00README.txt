This tarball contains a set of protein targets generated for the CAFA 3 challenge.
(http://biofunctionprediction.org/cafa/) 
This tarball contains:
#A folder for protein targets, with a total of 24 files in fasta format.
#A folder for mapping files, with a total of 24 files in text format.
#An Excel sheet for tracking the file names and other information.
#A PDF file explaining CAFA3 rules

##Target file format:
The fasta headers of each target file contains both the CAFA3 ID and the gene ID in the source database.

##Mapping file format:
For primarily protein-centric targets (CAFA Rules 5.1, 5.2), each line in the mapping file contains the CAFA3 ID and SwissProt gene entry name separated by tab.
For  specific term-centric  targets (CAFA3 Rules 5.3), each line in the mapping file contains the CAFA3 ID and the gene ID in their respective source database, separated by tab.
For DROME (D. melanogaster) targets, the mapping file contains both the flybase gene ID and the flybase polypeptide ID.

##Excel sheet explained:
###The "Track" column indicates to which CAFA3 track these targets belong. See CAFA3 rules for information on the different tracks.
###The "Taxonomy" column gives the NCBI taxonomy code for the target species.
###The "Counts" column gives the total number of proteins in this target species.
###The "LIMITED", "FULL" and "NO" columns give the total number of proteins in each of these knowledge categories. A "limited knowledge" target is a protein that does not have experimental annotation in the current ontology, but has experimental annotation in at least one other ontology. A "no knowledge" target is a protein that does not have experimental knowledge in any of the ontologies. A "full knowledge" target is a protein that has experimental annotation in all three ontologies.
###The "Source" column gives the source database of the sequences
###The "Link/version" column gives the link to the source databases, as well as the version of sequence files used.

