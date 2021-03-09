This script extracts the transcripts that are expressed in a selected tissue using the clustering summary of isoseq pipeline.

usage: extract_tissue.py [-h] [-i FILENAME] [-c COLUMN] [-o FILOUT]

optional arguments:

-h, --help: show this help message and exit

-i FILENAME, --filename FILENAME: Take the clustering summary file as input.
                    
-c COLUMN, --column COLUMN: The column number of the specific tissue in the input file.

-o FILOUT, --filout FILOUT: Output a txt file with the list of transcripts for the specified tissue.
