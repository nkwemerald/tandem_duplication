import os
import sys
import tokenize
import gzip

#Usage: create_TD_ref_file.py [vcf.gz folder] [bed file output folder] [LS if LOWSUPPORT included]
#Recommend to separate folder with TD interval file

if len(sys.argv) < 3:
    print ("Usage: create_TD_ref_file.py [vcf.gz folder] [bed file output folder] [LS if LOWSUPPORT included]")
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
        folder_split[i] = folder_split[i-1] + "/" + folder_split[i]

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
    # input file name as vcf, by raw_input
    vcf = vcf_folder + file + ".vcf.gz"
    # input file name as bed for output by raw_input
    bed = bed_file_folder + file + "_ref" + ".bed"

    # open the file named vcf for reading
    vcf_file = gzip.open(vcf, 'rb')
    # open the file named bed for writing
    bed_file = open(bed, "w")

    numbering = 1
    for line in vcf_file:
        # do not operate when the lines with "#"
        if not str(line)[0] == "#":
            # split the line into a list called row
            row = line.split("\t")
            # condition for including or excluding LOWSUPPORT
            if len(sys.argv) == 4:
                if sys.argv[3] == "LS":
                    condition = (row[6] == "PASS" or row[6] == "." or row[6] == "LOWSUPPORT") and len(row[4]) > 6 and len(row[4]) < 52
                else:
                    condition = (row[6] == "PASS" or row[6] == ".") and len(row[4]) > 6 and len(row[4]) < 52
            else:
                condition = (row[6] == "PASS" or row[6] == ".") and len(row[4]) > 6 and len(row[4]) < 52

            # write for PASS only and screen for variant length within 6 to 50
            if condition:
                ref = []
                row[0] = "chr" + str(row[0]) + "-" + str(numbering) + "-" + row[2]
                ref.append(row[0])
                variant_only = row[4][1:]
                ref.append(variant_only)
                ref_line = "\t".join(ref) + "\n"
                bed_file.write(ref_line)
                bed_file.write(ref_line)
                numbering += 1

    # close files
    vcf_file.close()
    bed_file.close()