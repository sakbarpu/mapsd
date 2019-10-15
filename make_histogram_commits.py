'''
Get unique users file as input which has commits for each
user. Grab the information about commits and make a
histogram. Store hists to file along with data.

'''

import sys, os
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import matplotlib.ticker as mtick
import pickle
import numpy


in_file = sys.argv[1]
out_dir = sys.argv[2]

f = open(in_file)
data = []
c = 0

GATHER_STATS = False
top_k = []
top_k_names = []

bottom_k = []
bottom_k_names = []
k=100

FILTER = True
if FILTER:
	min_commits_threshold = 20
	max_commits_threshold = 100000
else: 
	min_commits_threshold = 0
	max_commits_threshold = inf

for line in f:
	line_split = line.strip().split(" ")
	name = line_split[0]
	commits = int(line_split[1].strip())

	#Analysing the names with highest commits we saw some are
	#just bots monitoring the website. They usually have [bot] at
	#the end. Upon going to their web page on github it was seen
	#that there were either no repos or some garbage repos.
	if name.endswith("[bot]"): continue
	if name.endswith("bot"): continue
	if name.endswith("Bot"): continue
	if name.endswith("BOT"): continue

	if FILTER:
		if commits <= min_commits_threshold: continue
		if commits >= max_commits_threshold: continue

	#The following code is to maintain top k stats while
	#iterating. Top k as in top k commits. Keep the user names as
	#well. Basically a priority queue is maintained for the
	#commits as well as for names.
	if GATHER_STATS:
		if len(top_k) == 0: 
			top_k.append(commits)
			top_k_names.append(name)

		elif commits > min(top_k):
			if len(top_k) < k:
				top_k.append(commits)
				top_k_names.append(name)
			elif len(top_k) == k:
				top_k[0] = commits
				top_k_names[0] = name
				
		tmp = [(y,x) for y,x in sorted(zip(top_k,top_k_names))]
		top_k = []
		top_k_names = []
		for y,x in tmp: 
			top_k.append(y)
			top_k_names.append(x)

		#The following code is the same for bottom k
		if len(bottom_k) == 0: 
			bottom_k.append(commits)
			bottom_k_names.append(name)

		elif commits < max(bottom_k):
			if len(bottom_k) < k:
				bottom_k.append(commits)
				bottom_k_names.append(name)
			elif len(bottom_k) == k:
				bottom_k[0] = commits
				bottom_k_names[0] = name
				
		tmp = [(y,x) for y,x in sorted(zip(bottom_k,bottom_k_names), reverse=True)]
		bottom_k = []
		bottom_k_names = []
		for y,x in tmp: 
			bottom_k.append(y)
			bottom_k_names.append(x)
		if c % 10000 == 0: print (c)
	c+=1

	#append commits to data. after the loop we visualize it.
	data.append(commits)
	
#print top and bottom k names and commits
if GATHER_STATS:
	print ("TOP K STATS:")
	for x,y in zip(top_k_names,top_k): print (x,y)
	print ("\n\n BOTTOM K STAT")
	for x,y  in zip(bottom_k_names, bottom_k): print (x,y)

# plot and show stats for overall
print ("Number of users analysed (after filtering):",c)
print ("Minimum:", min(data), 
	"Maximum:", max(data), 
	"Mean:", int(numpy.mean(data)), 
	"Median:", numpy.median(data))

l = [min_commits_threshold, 100, 1000, 10000, 20000, 40000, 60000, 80000, 100000]
frq = []
edges = []
for c in range(len(l)-1):
	tmp1, tmp2 = numpy.histogram(data, 50, range=(l[c],l[c+1]))

	fig, ax = plt.subplots()
	ax.bar(tmp2[:-1], tmp1, width=100, align="edge", log=True)
	ax.set_title("User histogram based on commits " + str(l[c]) + " - " + str(l[c+1])) 
	ax.set_xlabel("Commits")
	ax.set_ylabel("Log(number of users)")
	plt.savefig(os.path.join(out_dir,"commits_"+str(l[c])+"_"+str(l[c+1])+".png"))
	
	o_file = open(os.path.join(out_dir,"commits_"+str(l[c])+"_"+str(l[c+1])+".p"),"wb")
	pickle.dump((tmp1,tmp2), o_file)
	
	frq.extend(tmp1)
	edges.extend(tmp2[:-1])

fig, ax = plt.subplots()
ax.bar(edges, frq, width=100, align="edge", log=True) 
ax.set_title("User histogram based on commits") 
ax.set_xlabel("Commits")
ax.set_ylabel("Log(number of users)")
l.remove(20)
l.remove(1000)
ax.set_xticks(l)
ax.tick_params(axis='both', which='major', labelsize=10)
plt.savefig(os.path.join(out_dir,"commits_overall.png"))

o_file = open(os.path.join(out_dir,"commits_overall.p"),'wb')
pickle.dump((frq,edges), o_file)
