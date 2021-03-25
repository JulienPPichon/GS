"""Draw a rarefaction curve of the iso-seq sequencing effort for multiplexed samples."""

import argparse
import random
import os
import matplotlib.pyplot as plt

def get_args(argv = None):
	"""Retrieves the arguments of the program. Returns: An object that contains the arguments."""	
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--abundance_file", help="Take abundance file as input i.e. the summary.csv resulting from the isoseq3 pipeline.")
	parser.add_argument("-g", "--blast_alignment", help="File containing the blast alignment, max_target have to be one.")
	parser.add_argument("-m", "--multiple_copy", help="Path of the folder containing the busco multiple copy sequences.")
	parser.add_argument("-s", "--single_copy", help="Path of the folder containing the busco single copy sequences")
	parser.add_argument("-c", "--column_tissue", help="Column of the tissue/sample considered to draw the curve. Multiple samples can be pulled together to draw it e.g. for sample 1 to 3 : '1-3'")
	parser.add_argument("-p", "--step_number", help="Number of subsets.")
	parser.add_argument("-t", "--title_curve", help="Title of the curve.")
	return parser.parse_args(argv)


def read_abundance_file(abundance_file, column_tissue):		
	abundance_dict = {}	
	with open(abundance_file, "r") as filin:
		for n, line in enumerate(filin):
			if n == 0:
				continue
			else:
				line = line.strip()
				line = line.split(",")
				if column_tissue.find("-"):
					sample = column_tissue.split("-")
					for tissue in range(int(sample[0]), int(sample[-1]) + 1):
						if int(line[int(tissue)]) != 0:
							if line[0] not in abundance_dict:
								abundance_dict[line[0]] = int(line[int(tissue)])
							else:	
								abundance_dict[line[0]] += int(line[int(tissue)])
						else:
							continue
				else:
					if int(line[int(column_tissue)]) != 0:
						abundance_dict[line[0]] = int(line[int(column_tissue)])
					else:
						continue
	return abundance_dict
	

def find_transcripts_blast(blast_alignment, abundance_dict):
	genes_dict = {}
	nb_transcripts = 0
	with open(blast_alignment, "r") as filin:
		for line in filin:
			line = line.strip()
			line = line.split("\t")
			line[0] = line[0].split("_")[-2:]
			line[0] = line[0][0] + "/" + line[0][1]
			if line[0] in abundance_dict:
				if line[5] not in genes_dict:
					genes_dict[line[5]] = int(abundance_dict[line[0]])
					nb_transcripts += int(abundance_dict[line[0]])
				else:
					genes_dict[line[5]] += int(abundance_dict[line[0]])
					nb_transcripts += int(abundance_dict[line[0]])
			else:
				continue
	return [genes_dict, nb_transcripts]


def find_transcripts_busco(multiple_copy, single_copy, abundance_dict):
	genes_list = os.listdir(multiple_copy)
	genes_dict = {}
	nb_transcripts = 0
	for genes in genes_list:
		with open(multiple_copy + "/" + genes, "r") as filin:
			for line in filin:
				line = line.strip()
				if line.startswith(">"):
					line = line.split(":")[0].split("_")[-2:]
					line = line[0] + "/" + line[1]
					if line in abundance_dict:
						if genes not in genes_dict:
							genes_dict[genes] = int(abundance_dict[line])
							nb_transcripts += int(abundance_dict[line])
						else:
							genes_dict[genes] += int(abundance_dict[line])
							nb_transcripts += int(abundance_dict[line])
					else:
						continue
				else:
					continue
	genes_list = os.listdir(single_copy)
	for genes in genes_list:
		with open(single_copy + "/" + genes, "r") as filin:
			for line in filin:
				line = line.strip()
				if line.startswith(">"):
					line = line.split(":")[0].split("_")[-2:]
					line = line[0] + "/" + line[1]
					if line in abundance_dict:
						if genes not in genes_dict:
							genes_dict[genes] = int(abundance_dict[line])
							nb_transcripts += int(abundance_dict[line])
						else:
							genes_dict[genes] += int(abundance_dict[line])
							nb_transcripts += int(abundance_dict[line])
					else:
						continue
				else:
					continue
	return [genes_dict, nb_transcripts]


def transcripts_shuffling(genes_dict, nb_transcripts, step_number, title_curve):
	dict_subset = {}
	list_new_gene = []
	sub_transcripts = []
	old_genes = set()
	for j, subset in enumerate(range(int(step_number))):
		new_gene = 0
		for i in range(int(int(nb_transcripts)/int(step_number))):		
			gene = random.choices(list(genes_dict.keys()), weights = list(genes_dict.values()), k = 1)[0]
			if gene not in old_genes:
				new_gene += 1
			genes_dict[gene] -= 1
			old_genes.add(gene)
		if j == 0:
			list_new_gene.append(new_gene)
			sub_transcripts.append(int(int(nb_transcripts)/int(step_number)))
		else:
			list_new_gene.append(list_new_gene[-1] + new_gene)
			sub_transcripts.append(int(int(nb_transcripts)/int(step_number)) + sub_transcripts[-1])
	plt.scatter(sub_transcripts, list_new_gene)
	plt.xlabel("Number of subsampled transcripts")
	plt.ylabel("Number of genes")
	plt.title(title_curve)
	plt.show()
	
if __name__ == "__main__":

	argvals = None
	args = get_args(argvals)
	abundance_dict = read_abundance_file(args.abundance_file, args.column_tissue)
	if args.blast_alignment != None:
		genes_dict, nb_transcripts = find_transcripts_blast(args.blast_alignment, abundance_dict)
	else:
		genes_dict, nb_transcripts = find_transcripts_busco(args.multiple_copy, args.single_copy, abundance_dict)
	transcripts_shuffling(genes_dict, nb_transcripts, args.step_number, args.title_curve)
