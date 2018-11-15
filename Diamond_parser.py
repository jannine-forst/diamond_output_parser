#!/usr/bin/env python3
import sys
import re
import glob
import os
import time
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from matplotlib.backends.backend_pdf import PdfPages


##########################################
############# DIAMOND PARSER #############
############## JF Nov 2018 ###############
##########################################

# Input needed:
# *.dmnd.krona.html file
# This will parse the file to find the organisms  listed in the "Organisms to find" section
#Later, this will have user input and be able to cycle through all the files in a directory

############# Definition of functions #############

#A function to look for the organism name in the html file and pull out the matching name AND read count
def organismFinder(self):
	if re.findall(self, line):
		#Set the name as it is, not as it was searched for. Will list all found.
		#(e.g. search for Yersinia might bring up Yersinia pestis and Yersiniaceae)
		for name in re.finditer(r".+\"(.+)\"", line):
			organismname = name.group(1)
			nextline = next(input_file)
			
			#If it doesn't find the read count in the first line, continue through more lines until it finds it
			while not re.findall(count, nextline): 
				nextline = next(input_file)
			
			#If it finds the count, pull out the number and write the sample, name, and count to file
			if re.findall(count, nextline): 
				for linecount in re.finditer(r"(.*>)([0-9]+)(<.*)", nextline):
					info = str(basename+"\t"+organismname+"\t"+linecount.group(2)+"\n")
					outfile.write(info)
			
			#When it finds the next taxon, stop looking - otherwise we'll get false counts
			elif re.findall(nextID, nextline):
				break
			
			#Do I really need this? If it doesn't find the next taxon or the count, continue going through
			else: 
				continue

############# Definition of variables #############

#First argument is the input file you want analyzed
path_to_input_files = sys.argv[1]
#Add error if no *.dmnd.krona.html 
#Put something here to check for two arguments

#Take the time for outfile name
timestr = time.strftime("%Y.%m.%d_%H-%M")

#Variables
Total = '<node name="Root">'
count = "<count>"
nextID = "node name"

#One day this will have an option to import from a file or use this as default
#Organisms to look for:
organismlist = ["Yersinia",
	"Mycobacterium", 
	"Vibrio cholerae", 
	"Salmonella typhi", 
	"Salmonella paratyphi", 
	"Neisseria meningitidis", 
	"Chlamydia", 
	"Treponema pallidum", 
	"Clostridium tetani", 
	"Clostridium botulinum", 
	Total]


############# Program Start #############

#Creates an outfile to write to: (with date/time stamp)
outfilename = path_to_input_files+"DMNDparsed.counts.outfile."+timestr+".txt"
outfile = open(outfilename, "w")

#Put an error here in case no *.dmnd.krona.html files are found
#Write the header to file
outfile.write("Sample"+"\t"+"Organism"+"\t"+"Count"+"\n")

#Opens the directory and looks for all *.dmnd.krona.html files:
for file in glob.glob(os.path.join(path_to_input_files , '*.dmnd.krona.html')):

	#Opens the file and in every line looks for the organism defined
	with open(file, "r") as input_file:
		
		# Take the basename of each sample
		nopath = os.path.basename(file)
		for base in re.finditer(r"(.+).all.+", nopath):
 			basename = base.group(1)

		#Look for each organism in the list and pull out counts/name if found
		for line in input_file:
			for organism in organismlist:
				organismFinder(organism)

outfile.close()

############# Math Start #############
#For now, this will be a separate section and a new outfile

#Make list of dictionaries:
#[{'Name' : 'samplename', 'Organism':'organism', 'Proportion':'readcount/totalreads'}, again]

name_dict = {}
all_list = []
# each_list = []

with open(outfilename, "r") as countfile:
	for line in countfile:
 		name,organism,readcount = line.split("\t")
 		
 		#Make sure not to take the header into the graph
 		if organism != "Organism":

 			#Make sure not to take the total read # into the graph
 			if organism == "Root":
 				total_count = readcount
 				# print("Hits this bit")
 				# name_dict["Name"] = name
 				# name_dict["Organism"] = "PositiveControl"
 				# name_dict["Proportion"] = "{:2%}".format(0.01)
 				# all_list.append(name_dict.copy())

 			#Otherwise, enter into dictionary
 			else:
 				name_dict["Name"] = name
 				name_dict["Organism"] = organism
 				name_dict["Proportion"] = int(readcount)/int(total_count)
 				all_list.append(name_dict.copy())
 				# all_list.append(each_list.copy())

# print(all_list)

#This is probably a ham-fisted way of doing this but... for now

name_list = []
org_list = []
prop_list = []
sample_list = {}
new_dict = {}
new_dict_list = []

for each in all_list:
	name_list.append(each["Name"])
	org_list.append(each["Organism"])
	prop_list.append(each["Proportion"])
	title = each["Name"]

# print(org_list)
# print(prop_list)

sample = "Hello"
sample_list.clear()
multiPDF = PdfPages(path_to_input_files+"DMNDparsed.graphs.outfile."+timestr+".pdf") 

# print(len(name_list))
for i in range(len(name_list)):
	if sample == name_list[i]:
		# print("Match at sample = name_list")
		# new_dict[org_list[i]] = prop_list[i]
		# new_dict["Proportion"] = prop_list[i]
		sample_list[org_list[i]] = prop_list[i]

	else:
		if sample != "Hello":
			# print("Match at no hello")
			# print(sorted(sample_list.values()))
			plt.bar(range(len(sample_list)), list(sorted(sample_list.values())), align='center')
			plt.xticks(range(len(sample_list)), list(sorted(sample_list, key=sample_list.__getitem__)), rotation = 90)
			plt.title(sample)
			plt.xlabel("Pathogens")
			plt.ylabel("Proportion of assigned reads in total")
			plt.savefig(multiPDF, format = 'pdf', bbox_inches='tight')
			plt.clf()
			# print(sample_list)

			sample = name_list[i]
			sample_list.clear()

			sample_list["PositiveControl"] = 0.01

		else:
			# print("Match at yes hello")
			sample = name_list[i]
			sample_list.clear()
			sample_list[org_list[i]] = prop_list[i]
			sample_list["PositiveControl"] = 0.01

plt.bar(range(len(sample_list)), list(sorted(sample_list.values())), align='center')
plt.xticks(range(len(sample_list)), list(sorted(sample_list, key=sample_list.__getitem__)), rotation = 90)
plt.title(sample)
plt.xlabel("Pathogens")
plt.ylabel("Proportion of assigned reads in total")
plt.savefig(multiPDF, format = 'pdf', bbox_inches='tight')
plt.clf()

multiPDF.close()

#Now we need this as a percentage
#The graph needs to be improved to compare more samples together? Maybe?

