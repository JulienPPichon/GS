import argparse


def get_args(argv = None):
	"""Analyze panther subfamily enrichment for a species compared to other ones. Outputs sorted file per ratio for each comparisons."""	
	parser = argparse.ArgumentParser()
	parser.add_argument("-n", "--names", help="Panther file containing family function")
	parser.add_argument('-i', "--input_files", nargs='*', help="List of the input Panther files to compare. Species of interest should be first.")
	return parser.parse_args(argv)


def get_familly_function(file_names):
	familly_function = {}
	with open("names.tab", "r") as filin_names:
		for line in filin_names:
			line = line.strip()
			line = line.split("\t")
			if line[0].split(".")[1] == "mag":
				familly_function[line[0].split(".")[0]] = line[1]
	return familly_function


def count_familly(list_file, subfamilly_function):
	familly_dict = {}
	subfamilly_dict = {}
	for filename in list_file:
		with open(filename, "r") as filin:
			analyzed_genes = set()
			familly_dict[filename] = {}
			subfamilly_dict[filename] = {}
			for line in filin:
				line = line.strip()
				line = line.split("\t")
				if line[0] not in analyzed_genes:
					if line[1].count(":") == 0:
						if line[1] not in familly_dict[filename]:
							familly_dict[filename][line[1]] = 1
						else:
							familly_dict[filename][line[1]] += 1
					else:
						familly = line[1].split(":")[0]
						subfamilly = line[1]
						if familly not in familly_dict[filename]:
							familly_dict[filename][familly] = 1
							subfamilly_dict[filename][subfamilly] = 1
							subfamilly_function[subfamilly] = line[2]
						else:
							familly_dict[filename][familly] += 1
							if subfamilly not in subfamilly_dict[filename]:
								subfamilly_dict[filename][subfamilly] = 1
								subfamilly_function[subfamilly] = line[2]
							else:
								subfamilly_dict[filename][subfamilly] += 1
				analyzed_genes.add(line[0])	
	return [familly_dict, subfamilly_dict, subfamilly_function]


def create_ratio(list_file, subfamilly_dict):
	ratio_dict = {}
	unique_dict = {}
	for filename in list_file[1:]:
		ratio_dict[list_file[0] + str(filename)] = {}
		unique_dict[list_file[0] + str(filename)] = {}
		for subfamilly in subfamilly_dict[list_file[0]]:
			if subfamilly in subfamilly_dict[filename]:
				ratio_dict[list_file[0] + str(filename)][subfamilly] = round(subfamilly_dict[list_file[0]][subfamilly] / subfamilly_dict[filename][subfamilly], 2)
			else:
				unique_dict[list_file[0] + str(filename)][subfamilly] = subfamilly_dict[list_file[0]][subfamilly]
	return [ratio_dict, unique_dict]


def create_unique_output(unique_dict, subfamilly_function):
	for unique in unique_dict:
		with open(unique + "unique.txt", "w") as filout:
			for subfamilly in dict(sorted(unique_dict[unique].items(), key=lambda item: item[1])):
				filout.write(subfamilly + "\t" + str(unique_dict[unique][subfamilly]) + "\t" + subfamilly_function[subfamilly] + "\n")
		

def create_ratio_output(ratio_dict, subfamilly_dict, subfamilly_function):	
	for ratio in ratio_dict:
		dict_name = ratio.split("_")[1]
		with open(ratio + ".txt", "w") as filout:
			for subfamilly in dict(sorted(ratio_dict[ratio].items(), key=lambda item: item[1])):
				filout.write(subfamilly + "\t" + str(ratio_dict[ratio][subfamilly]) + "\t" + str(subfamilly_dict["gs.pthr"][subfamilly]) + "\t" + str(subfamilly_dict[dict_name][subfamilly]) + "\t" + subfamilly_function[subfamilly] + "\n")


if __name__ == "__main__":

	argvals = None
	args = get_args(argvals)
	familly_function = get_familly_function(args.names)
	subfamilly_function = {}
	familly_dict, subfamilly_dict, subfamilly_function = count_familly(args.input_files, subfamilly_function)
	ratio_dict, unique_dict = create_ratio(args.input_files, subfamilly_dict)
	create_unique_output(unique_dict, subfamilly_function)
	create_ratio_output(ratio_dict, subfamilly_dict, subfamilly_function)
	
