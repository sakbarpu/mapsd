import sys, os
import itertools
import numpy
from preprocessor import Preprocessor

from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

from pprint import pprint

class LineSentences:
        '''
        The purpose of this class is to read sentences/documents from a single file.
        The format of the file is such that each document is on a separate line.

        '''

        def __init__(self, inpath):

                self.infile = open(inpath, encoding="iso-8859-15")

        def __iter__(self):

                self.infile.seek(0)
                for line in itertools.islice(self.infile, None):
                        yield line

        def __len__(self):
                self.infile.seek(0)
                c = 0
                for line in itertools.islice(self.infile, None):
                        c+=1
                return c

        def __getitem__(self, key):
                self.infile.seek(0)
                if type(key) is int:
                        return next(itertools.islice(self.infile, key, key+1))
                elif type(key) is tuple:
                        tmp = []
                        for x in itertools.islice(self.infile, key[0], key[1]):
                                tmp.append(x)
                        return tmp

in_path = sys.argv[1]
out_path = sys.argv[2] #output dir
stop_words = set(stopwords.words("english"))

print ("\n")
print ("----------------------------------------------------------------------------------")
print ("Input dir where all the repo names and descs files for all the countries are there")
print (in_path)

print ("Output dir where preprocessed files are saved")
print (out_path)

#if not os.path.exists(os.path.join(out_path,"processed_content.txt")):
files = []
for r, d, f in os.walk(in_path):
	for fi in f:
		if fi.endswith(".csv"): continue
		files.append(os.path.join(r, fi))

files = sorted(files)
preprocessor = Preprocessor()
for fi in files:
	with open(os.path.join(out_path,os.path.basename(fi)),"w") as fo:
		with open(fi) as f:
			for whole_line in f:
				if whole_line == "\n": continue
				whole_line = whole_line.split(";;;")
				reponames = whole_line[0].split(",")
				repodescs = whole_line[1].split(";;")
				whole_line = reponames + repodescs
				for line in whole_line:
					line = preprocessor.cleanhtml(line)
					line = " ".join([l for l in line.split(" ") if not l in stop_words])
					preprocessor.raw_content = line
					preprocessor.perform_preprocessing()
					line = preprocessor.processed_content 
				
					if len(line.split(" ")) >= 5: fo.write(line + "\n")



