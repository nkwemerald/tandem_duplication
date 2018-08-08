import os
import sys
import tokenize
import gzip

#Usage: create_TD_bed_file.py [vcf.gz folder] [bed file output folder]

if len(sys.argv) < 3:
    print ("Usage: create_TD_bed_file.py [vcf.gz folder] [bed file output folder]")
    exit()

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)

# Create folder for bed file
bed_file_folder = sys.argv[2]
folder_split = bed_file_folder.split("/")
if "~" in folder_split:
    folder_split.remove("~")
    folder_split[0] = "~/" + folder_split[0]

for i in range(len(folder_split)):
    if i > 0:
        folder_split[i] = folder_split[i-1] + folder_split[i]

for folder in folder_split:
    createFolder(folder)


all_vcf_file = []
dirs = os.listdir(sys.argv[1])

for file in dirs:
    if file[-7:] == ".vcf.gz":
        all_vcf_file.append(file[:-7])

if not sys.argv[1][-1] == "/":
    vcf_folder = sys.argv[1] + "/"
else:
    vcf_folder = sys.argv[1]

if not bed_file_folder[-1] == "/":
    bed_file_folder = bed_file_folder + "/"


for file in all_vcf_file:
    vcf = vcf_folder + file + ".vcf.gz"
    bed = bed_file_folder + file + "_interval.bed"

    vcf_file = gzip.open(vcf, "rb")
    bed_file = open(bed, "w")

    numbering = 1
    for line in vcf_file:
        if not str(line)[0] == "#":
            row = line.split("\t")
            if (row[6] == "PASS" or row[6] == ".") and len(row[4]) > 6 and len(row[4]) < 52:
                row_L = []
                row_R = []
                row[0] = "chr" + str(row[0])

                row[1] = int(row[1])
                row[1] -= 1

                row_L.append(row[0])
                row_R.append(row[0])

                variant_length = len(row[4]) - 1

                left_end = row[1] - variant_length + 1
                right_end = row[1] + variant_length + 1

                row_L.append(str(left_end))
                row_L.append(str(row[1] + 1))

                row_R.append(str(row[1] + 1))
                row_R.append(str(right_end))

                row_L.append(str(numbering) + "-left-" + row[2])
                row_R.append(str(numbering) + "-right-" + row[2])

                left = "\t".join(row_L) + "\n"
                right = "\t".join(row_R) + "\n"

                bed_file.write(left)
                bed_file.write(right)

                numbering += 1
    vcf_file.close()
    bed_file.close()