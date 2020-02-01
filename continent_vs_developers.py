import sys
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
from num2words import num2words

#continent data downloaded from https://datahub.io/JohnSnowLabs/country-and-continent-codes-list#data 

con_f = sys.argv[1]
dev_f = sys.argv[2]

dev = {}
with open(dev_f) as f:
	for l in f:
		l = l.strip().split("\t")
		if l[0] == "Code2": continue
		dev[l[0]] = [l[1],int(l[2])]

con = {}
map_con_code_2_name = {}
with open(con_f) as f:
	for l in f:
		l = l.strip().split("\t")
		if len(l) == 3:
			con[l[2]] = [l[0],l[1]]
		map_con_code_2_name[l[1]] = l[0] 
not_there = []
cons_data = defaultdict(int)
for k in dev:
	if k in con:
		devs_value = int(dev[k][1])
		continent = con[k][1]
		cons_data[continent] += devs_value
	else:
		not_there.append(k)

#print ("not there")
#print (not_there)
#print (len(not_there))
for k, v in sorted(cons_data.items(), key=lambda item: item[1],reverse=True):
	print (k, map_con_code_2_name[k], v, num2words(v))

for k, v in sorted(cons_data.items(), key=lambda item: item[1],reverse=True):
	print (map_con_code_2_name[k], v)


