import argparse

def get_args(argv = None):
	"""Filter out isoforms from a protein fasta file using the related GTF file."""	
	parser = argparse.ArgumentParser()
	parser.add_argument("-g", "--gtf_filename", help="File name of the GTF file input.")
	parser.add_argument("-p", "--prot_filename", help="File name of the protein fasta file input.")
	parser.add_argument("-o", "--out_filename", help="File name of the protein fasta file output.")
	return parser.parse_args(argv)


def choose_isoform(filename_gtf):
	set_prot = set()
	with open(filename_gtf, "r") as filin1:
		for line in filin1:
			line = line.strip()
			if line.startswith("#"):
				continue
			else:
				line = line.split("\t")
				if line[2] == "gene":
					new_gene = True
				elif line[2] == "CDS":
					if new_gene == True:
						line = line[-1].split()
						for n, column in enumerate(line):
							if column.find("protein_id") != -1:
								set_prot.add(line[n +1].split("\"")[1])
								new_gene = False
					else:
						continue
	return set_prot


def write_output(set_prot, filename_prot, filename_out):
	with open(filename_prot, "r") as filin2, open(filename_out, "w") as filout:
		keep_sequence = False
		for line in filin2:
			line = line.strip()
			if line.startswith(">"):
				keep_sequence = False
				prot_id = line.split()[0][1:]
				if prot_id in set_prot:
					keep_sequence = True
					filout.write(line + "\n")
			else:
				if keep_sequence == True:
					filout.write(line + "\n")
				else:
					continue

		
if __name__ == "__main__":

	argvals = None
	args = get_args(argvals)
	set_prot = choose_isoform(args.gtf_filename)
	write_output(set_prot, args.prot_filename, args.out_filename)
		
