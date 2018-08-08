import os
import sys
import tokenize

#Usage: convert_to_fasta.py [variant interval folder] [fasta file] [sequence output]

if len(sys.argv) < 4 or sys.argv[2][-6] <> ".fasta":
    print ("Usage: convert_to_fasta.py [variant interval folder] [fasta file] [sequence output]")
    exit()

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)

# Create folder for bed file
seq_file_folder = sys.argv[3]
folder_split = seq_file_folder.split("/")
if "~" in folder_split:
    folder_split.remove("~")
    folder_split[0] = "~/" + folder_split[0]

for i in range(len(folder_split)):
    if i > 0:
        folder_split[i] = folder_split[i-1] + folder_split[i]

for folder in folder_split:
    createFolder(folder)

all_bed_file = []
dirs = os.listdir(sys.argv[1])

for file in dirs:
    if file[-12:] == "interval.bed":
        all_bed_file.append(file[:-12])

for file in all_bed_file:
    bed = sys.argv[1] + "/" + file + "interval.bed"
    fasta = sys.argv[2]
    output_var = sys.argv[3] + "/" + file + "_var.bed"
    command_line = "bedtools getfasta -fi " + fasta + " -bed " + bed + " -name -tab -fo " + output_var
    os.system(command_line)