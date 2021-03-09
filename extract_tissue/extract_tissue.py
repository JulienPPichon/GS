#!/bin/env python3

"""Extract the transcripts that are expressed in a selected tissue using the clustering summary of isoseq pipeline."""

import argparse


def get_args(argv = None):
	"""Retrieves the arguments of the program. Returns: An object that contains the arguments."""	
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--filename", help="Take the clustering summary file as input.")
	parser.add_argument("-c", "--column", type=int, help="The column number of the specific tissue in the input file.")
	parser.add_argument("-o", "--filout", help="Output a txt file with the list of transcripts for the specified tissue.")
	return parser.parse_args(argv)


def read_input(filename, column):
	transcripts = []
	with open(filename, "r") as filin:
		for n, line in enumerate(filin):
			if n == 0:
				continue
			else:
				line = line.strip()
				line = line.split(",")
				if int(line[column]) != 0:
					transcripts.append(line[0])
	return transcripts


def write_output(filout_name, transcripts):
	with open(filout_name, "w") as filout:
		for transcript in transcripts:
			filout.write("KP_pool_HQ_" + transcript + "\n")


if __name__ == "__main__":

	argvals = None
	args = get_args(argvals)
	transcripts = read_input(args.filename, args.column)
	write_output(args.filout, transcripts)


			
			
		
