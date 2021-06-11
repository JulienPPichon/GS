Filter out gene presenting no start or stop codon or having an X in the protein sequence from augustus GTF output. 
Output a GTF file and a protein fasta file.

usage: filter_and_parse_augustus.py [-h] [-i FILENAME] [-o OUTPUT]

-i FILENAME, --filename  Take augustus prediction gtf file as input.

-o OUTPUT, --output  File name of the GTF and protein output.
