inputfile = open("input.train.txt", "r")
outputfile = open("input.train2.txt", "w")

outputString = ""
for line in inputfile.readlines():
    outputString = outputString + ' '.join((line.split())[1:]) + '\n'

outputfile.write(outputString)
