import os
import sys
import tokenize

#Usage: TD_seq_matching.py [variant interval folder] [variant seq folder] [reference seq folder] [output folder]

if len(sys.argv) < 5:
    print ("Usage: TD_seq_matching.py [variant interval folder] [variant seq folder] [reference seq folder] [output folder]")
    exit()

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)

# Create folder for output file
output_file_folder = sys.argv[4]
folder_split = output_file_folder.split("/")
if "~" in folder_split:
    folder_split.remove("~")
    folder_split[0] = "~/" + folder_split[0]

for i in range(len(folder_split)):
    if i > 0:
        folder_split[i] = folder_split[i-1] + "/" + folder_split[i]

for folder in folder_split:
    createFolder(folder)

# define longest common prefix function
def longestcommonprefix(s1,s2):
    i=0
    while i < len(s1) and i < len(s2) and s1[i] == s2[i]:
        i+=1
    return s1[:i]

def seq_match(s1, s2):
    longestcommon = longestcommonprefix(s1, s2)
    lcp_length = len(longestcommon)
    if not len(s1) == len(s2):
        print ("the length of variant didn't match the reading frame")
        # quit if the length not match
        quit()
    elif longestcommon == s1:
        return ["match", str(1)]
    elif lcp_length > 6 and len(s1) % lcp_length == 0:
        match_freq = s1.count(longestcommon, 0, len(s1))
        if match_freq == len(s1) / lcp_length:
            return ["match", str(match_freq + 1)]
        else:
            return ["not match", str(match_freq + 1)]
    else:
        return ["not match", "na"]



# listing all file name
all_file = []
dirs = os.listdir(sys.argv[1])
#loop for comparing all files
for file in dirs:
    if file[-12:] == "interval.bed":
        all_file.append(file[:-12])

for file in all_file:
    var = sys.argv[2] + "/" + file + "_interval_var.bed"
    bed = sys.argv[1] + "/" + file + "_interval.bed"
    ref = sys.argv[3] + "/" + file + "_ref.bed"
    out = sys.argv[4] + "/" + file + "_output.txt"

    # open file
    var_extract = open(var, "r")
    ref_check = open(ref, "r")
    bed_interval = open(bed, "r")
    out_file = open(out, "w")

    # make the file become list
    var_list = var_extract.readlines()
    ref_list = ref_check.readlines()
    bed_list = bed_interval.readlines()
    # out_file.write("chr\tstart\tend\tID\tvariant\textract\tlength\tmatching\tcount\n")

    # quit if the length are not the same
    if not len(var_list) == len(ref_list):
        print ("The number of variants for " + file + " is the same as that of reference")
        exit()
    # matching
    for i in range(len(ref_list)):
        var_list[i] = var_list[i].split("\t")
        ref_list[i] = ref_list[i].split("\t")
        bed_list[i] = bed_list[i].split("\t")
        extract = var_list[i][1][:-1]
        s1 = ref_list[i][1][:-1].upper()
        s2 = var_list[i][1][:-1].upper()
        result = seq_match(s1, s2)
        if result[0] == "match":
            result = "\t".join(result)
            out_file.write(bed_list[i][0] + "\t" + bed_list[i][1] + "\t" + bed_list[i][2] + "\t" + bed_list[i][3][:-1] + "\n")
    # close file
    var_extract.close()
    ref_check.close()
    bed_interval.close()
    out_file.close()