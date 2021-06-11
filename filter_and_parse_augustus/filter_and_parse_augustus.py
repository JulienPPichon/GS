import argparse

def get_args(argv = None):
	"""Filter out gene presenting no start or stop codon or having an X in the protein sequence from augustus GTF output.
		Output a GTF file and a protein fasta file."""	
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--filename", help="Take augustus prediction gtf file as input.")
	parser.add_argument("-o", "--output", help="file name of the GTF and protein output.")
	return parser.parse_args(argv)


def filter_out(input_file):
	list_transcript = []
	with open(input_file, "r") as filin:	
		prot_seq = False
		start_codon = False
		stop_codon = False
		gene_number = 0
		transcript_number = 0
		temp_transcript = []
		for line in filin:
			line = line.strip()
			if line.startswith("#") and prot_seq == False:
				continue
			elif line.startswith("#") and prot_seq == True:
				if start_codon == False or stop_codon == False:
					start_codon == False
					stop_codon == False
					prot_seq = False
					temp_transcript = []
				elif start_codon == True and stop_codon == True:
					if line.count("X") != 0:
						start_codon == False
						stop_codon == False
						prot_seq = False
						temp_transcript = []
					else:
						if line.count("]") == 1 and line.count("[") == 0:
							temp_transcript[-1] = temp_transcript[-1] + line[2:]
							list_transcript.append(temp_transcript)
							temp_transcript = []
							prot_seq = False
							start_codon = False
							stop_codon = False
						elif line.count("[") == 1 and line.count("]") == 0:
							temp_transcript.append(line[2:])
						elif line.count("[") == 1 and line.count("]") == 1:
							temp_transcript.append(line[2:])
							list_transcript.append(temp_transcript)
							temp_transcript = []
							prot_seq = False
							start_codon = False
							stop_codon = False
						else:
							temp_transcript[-1] = temp_transcript[-1] + line[2:]
			else:
				line = line.split()
				prot_seq = True
				if line[2] == "start_codon":
					start_codon = True
				elif line[2] == "stop_codon":
					stop_codon = True
				temp_transcript.append(line)
	return list_transcript


def write_output(list_transcript, output_name):
	with open(str(output_name) + ".gff", "w") as filout, open(str(output_name) + ".faa", "w") as filout2:
		gene_number = 0
		for transcript in list_transcript:
			for line in transcript:
				if line[2] == "gene":
					gene_number += 1
					transcript_number = 0
					filout.write("\t".join(line[:-1]) + "\tgene_id \"g." + str(gene_number) + "\";\n")
				elif line[2] == "transcript":
					transcript_number += 1
					filout.write("\t".join(line[:-1]) + "\tgene_id \"g." + str(gene_number) + "\"; transcript_id \"g." + str(gene_number) + "." + str(transcript_number) + "\";\n")
				elif type(line) == str:
					filout2.write(">g." + str(gene_number) + "." + str(transcript_number) + "\n" + line[20:-1] + "\n")
				else:
					filout.write("\t".join(line[:-4]) + "\tgene_id \"g." + str(gene_number) + "\"; transcript_id \"g." + str(gene_number) + "." + str(transcript_number) + "\";\n")
					

if __name__ == "__main__":

	argvals = None
	args = get_args(argvals)
	list_transcript = filter_out(args.filename)
	write_output(list_transcript, args.output)
			
