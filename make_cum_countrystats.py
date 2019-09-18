import sys, os

def combine_langs(lang1, lang2):

	if lang2 is None: return lang1
	
	for x in lang1: 
		l = x[0]
		n = x[1]
		if l in lang2:
			lang2[l] += n
		else:
			lang2[l] = n
	
	return lang2
	
in_dir = sys.argv[1]
csv_files = os.listdir(in_dir)
csv_files = [os.path.join(in_dir, x) for x in csv_files]

country_stats = {}
for country in open(csv_files[0]).read().strip().split("\n"):
	country = country.split("\t")
	country_stats[country[0]] = [country[1], country[2], 0, 0, {}]

for fn in csv_files:
	print ("Working on ", fn)
	with open(fn) as in_file:
		in_file.readline()
		for line in in_file:
			line_split = line.split("\t")
			country_code2 = line_split[0]
			country_devs = int(line_split[3])
			country_commits = int(line_split[4])
			country_langs = line_split[5].strip()

			if country_langs!='':
				country_langs = [x.split(":") for x in country_langs.strip().split(",")]
				country_langs = [[x[0],int(x[1])] for x in country_langs]

			country_stats[country_code2][2] += country_devs
			country_stats[country_code2][3] += country_commits
			country_stats[country_code2][4] = combine_langs(country_langs, country_stats[country_code2][4])
	print (country_stats["US"])


with open(os.path.join(in_dir,"cum_stats.csv"), "w") as f:
	f.write("Code1 \t Code2 \t Name \t #Developers \t #Commits \t #Languages\n")
	for k,v in sorted(country_stats.items()): 
		f.write(k + "\t" + v[0] + "\t" + v[1] + "\t" + str(v[2]) + "\t" + str(v[3]) + "\t" +  ",".join([str(x) + ":" + str(y) for x,y in v[4].items()]))
		f.write("\n")
