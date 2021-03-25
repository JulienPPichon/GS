Draw a rarefaction curve of the iso-seq sequencing effort for multiplexed samples.

usage: rarefaction.py [-h] [-i ABUNDANCE_FILE] [-g BLAST_ALIGNMENT]
                      [-m MULTIPLE_COPY] [-s SINGLE_COPY] [-c COLUMN_TISSUE]
                      [-p STEP_NUMBER] [-t TITLE_CURVE]

-h, --help
show this help message and exit

-i ABUNDANCE_FILE, --abundance_file
Take abundance file as input i.e. the summary.csv
resulting from the isoseq3 pipeline.

-g BLAST_ALIGNMENT, --blast_alignment
File containing the blast alignment, max_target have
to be one.

-m MULTIPLE_COPY, --multiple_copy
Path of the folder containing the busco multiple copy
sequences.

-s SINGLE_COPY, --single_copy
Path of the folder containing the busco single copy
sequences

-c COLUMN_TISSUE, --column_tissue
Column of the tissue/sample considered to draw the
curve. Multiple samples can be pulled together to draw
it e.g. for sample 1 to 3 : '1-3'

-p STEP_NUMBER, --step_number
Number of subsets.

-t TITLE_CURVE, --title_curve
Title of the curve.


Example to run on blast output:

    python3 rarefaction.py -i data/example_summary.csv -g data/example_blast.txt -c 3 -p 100 -t "Rarefaction curve sample 3"
    
    
Example to run on busco output:

    python3 rarefaction.py -i data/example_summary.csv -m data/example_mbusco -s data/example_sbusco -c 3 -p 100 -t "Rarefaction curve sample 3"
