import sys
# Get input file and output file name
infile = sys.argv[1]
name = sys.argv[2]+".txt"
# Open input file and create text file
file = open(infile)
output = open(name, "w=")
# Transcribe only the lines that are characters
file.seek(0)
for line in file:
    if line[0].isalpha():
        output.write(line)
