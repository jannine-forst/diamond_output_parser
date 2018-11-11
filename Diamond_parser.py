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


def organismFinder(self):
	if re.findall(self, line):
		for name in re.finditer(r".+\"(.+)\"", line):
			organismname = name.group(1)
			#print(organismname)
			nextline = next(input_file)
			while not re.findall(count, nextline):
				nextline = next(input_file)
				#print("Hit while not loop")
			if re.findall(count, nextline):
				for linecount in re.finditer(r"(.*>)([1-9]+)(<.*)", nextline):
					info = str(organismname+"\t"+linecount.group(2)+"\n")
					outfile.write(info)
				#print("Count here, later")
			elif re.findall(nextID, nextline):
				#print("End line, later")
				break
			else:
				#print("Not this line, later")
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

#Organisms to find:

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

#print(outfilename)

#Opens the file and in every line looks for the organism defined
with open(diamond_matches, "r") as input_file:
	#Write the header to file
	outfile.write("Organism"+"\t"+"Count"+"\n")
	for line in input_file:
		for organism in organismlist:
			organismFinder(organism)


#This one goes just by the name in the function
	# for line in input_file: #One day I will get this to work iteratively over each organism in a list
	# 	if organismFinder(yersinia) != None:
	# 		outfile.write(organismFinder(yersinia)+"\n") #There has to be a better way to iterate over these!
	# 	if organismFinder(Myc) != None:
	# 		outfile.write(organismFinder(Myc)+"\n")

outfile.close()

#Later this will also will create a graph!
#Now we need this as a percentage
#And it'll pop out a graph for all the samples?
#Organism on the x axis, % on the y axis
#Sample coloured columns

