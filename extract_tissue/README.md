This script extracts the transcripts that are expressed in a selected tissue using the clustering summary of isoseq pipeline.

usage: extract_tissue.py [-h] [-i FILENAME] [-c COLUMN] [-o FILOUT]

-h, --help
show this help message and exit

-i FILENAME, --filename
Take the clustering summary file as input.
                    
-c COLUMN, --column
The column number of the specific tissue in the input file.

-o FILOUT, --filout
Output a txt file with the list of transcripts for the specified tissue.
