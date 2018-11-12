#!/usr/bin/env python3
import sys
import re

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
			
			#If it finds the count, pull out the number
			if re.findall(count, nextline): 
				for linecount in re.finditer(r"(.*>)([1-9]+)(<.*)", nextline):
					info = str(organismname+"\t"+linecount.group(2)+"\n")
					outfile.write(info)
			
			#When it finds the next taxon, stop looking - otherwise we'll get false counts
			elif re.findall(nextID, nextline): 
				break
			
			#Do I really need this? If it doesn't find the next taxon or the count, continue going through
			else: 
				continue



############# Definition of variables #############

#First argument is the input file you want analyzed
diamond_matches = sys.argv[1]
#Add error if not *.dmnd.krona.html 
#Put something here to check for two arguments

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

#Opens a file to write the results to:
for base in re.finditer(r"(^.+\.)all.+", diamond_matches):
	basename = base.group(1)

outfilename = basename+"DMNDparsed.outfile.txt"
outfile = open(outfilename, "w")

#Opens the file and in every line looks for the organism defined
with open(diamond_matches, "r") as input_file:
	#Write the header to file
	outfile.write("Organism"+"\t"+"Count"+"\n")
	
	#Look for each organism in the list and pull out counts/name if found
	for line in input_file:
		for organism in organismlist:
			organismFinder(organism)

outfile.close()

#Later this will also will create a graph!
#Now we need this as a percentage
#And it'll pop out a graph for all the samples?
#Organism on the x axis, % on the y axis
#Sample coloured columns

