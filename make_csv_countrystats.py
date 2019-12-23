import sys

if sys.argv[3] == "developers":
	data = []
	with open(sys.argv[1]) as f:
		for line in f:
			line_split = line.split("\t")
			data.append([line_split[1].strip(), line_split[2].strip(), line_split[3].strip()])


	with open(sys.argv[2], "w") as f:
		for d in data:
			f.write(d[0] + "\t" + d[1] + "\t" + d[2] + "\n")

elif sys.argv[3] == "commits":
	data = []
	with open(sys.argv[1]) as f:
		for line in f:
			line_split = line.split("\t")
			data.append([line_split[1].strip(), line_split[2].strip(), line_split[4].strip()])


	with open(sys.argv[2], "w") as f:
		for d in data:
			f.write(d[0] + "\t" + d[1] + "\t" + d[2] + "\n")

