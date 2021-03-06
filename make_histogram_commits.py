'''
Get unique users file as input which has commits for each
user. Grab the information about commits and make a
histogram. Store hists to file along with data.
(ONE TIME EXECUTION)

'''

'''
results of analysing after making commits histogram:

(1) bots are there (found while exploration of data): 

there are bots that have accounts at github. they have
names ending in "[bot]" and have the most traffic (commits)
for github. we don't include them in histogram. one such
both is greenkeeper[bot].

(2) 20 to 100000 commits make sense (again exploration study):

filtering for more than 20 and less than 100000 commits
makes sense. manually analyzed few accounts less than 20 and
they all look newbies. and few have more than 100000 commits
and are considered outliers. so we reject them as well. more
than 100000 commits in one year is simply not realistic. the
reason we reject more than 100000 is because they are few
and they badly skew the histogram.

(3) 10 million users became 3 million users:

filtering reduced the number of users from 10 million to
3 million.

(4) mostly bots and newbies are there (hence, the reduction):

most accounts on github are either bots or newbies. few
are "experts" having large number of commits.

(5) the stats are as follows:

number of users analysed (after filtering):: 2787647
commits:: minimum: 21 maximum: 99039 mean: 129 median: 52

(6) histogram shows that most users are within 1000 commits.
very few are "experts" and have more than 1000 commits. 

(7) in particular:
     num_commits: num_users
>=20	 commits: 2787647
>=100	 commits: 742220
>=1000	 commits: 38096
>=10000	 commits: 866
>=20000	 commits: 288
>=40000	 commits: 109
>=60000	 commits: 50
>=80000	 commits: 20
>=100000 commits: 0

20-100 	     commits: 2045427  
100-1000     commits: 704124
1000-10000   commits: 37230
10000-20000  commits: 578
20000-40000  commits: 179
40000-60000  commits: 59
60000-80000  commits: 30
80000-100000 commits: 20

     		 commits
>= 20 		:359722380
>= 100 		:267056584
>= 1000		:95992996
>= 10000	:19544457
>= 20000 	:11765155
>= 40000 	:6703684
>= 60000 	:3868332
>= 80000 	:814353
>= 100000 	:0

20-100		:92665796
100-1000	:171063588
1000-10000	:76448539
10000-20000	:7779302
20000-40000	:5061471
40000-60000	:2835352
60000-80000	:2053979
80000-100000	:814353

(8) average (commits/users for different range):

20-100		: 45 
100-1000	: 242
1000-10000	: 2053
10000-20000	: 13459
20000-40000	: 28276
40000-60000	: 48056
60000-80000	: 68465
80000-100000	: 40717



'''

import sys, os
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import matplotlib.ticker as mtick
import pickle
import numpy
from bisect import bisect

in_file = sys.argv[1]
out_dir = sys.argv[2]

f = open(in_file)
data = []
c = 0

#top and bottom users in terms of commits
GATHER_STATS = False
top_k = []
top_k_names = []

bottom_k = []
bottom_k_names = []
k=100

#filter based on min and max commit threshold
FILTER = True
if FILTER:
	min_commits_threshold = 20
	max_commits_threshold = 100000
else: 
	min_commits_threshold = 0
	max_commits_threshold = inf

#loop over each unique user in file
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

	#if commits not within min to max range then drop this user
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
#	if c == 10000: break
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
print ("Number of commits done by those users:", sum(data))
print ("Minimum:", min(data), 
	"Maximum:", max(data), 
	"Mean:", int(numpy.mean(data)), 
	"Median:", numpy.median(data))

#to plot we need these jumps (bins) in the commits
l = [min_commits_threshold, 100, 1000, 10000, 20000, 40000, 60000, 80000, 100000]

data_sorted = sorted(data)
print ("users")
for c in l:
	print (">=", c, len(data_sorted) - bisect(data_sorted,c))	
print ("commits")
for c in l:
	print (">=", c, sum(data_sorted[bisect(data_sorted,c):]))

#Plot histograms for each range(x,y)
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

#Plot the overall histogram
fig, ax = plt.subplots()
ax.bar(edges, frq, width=100, align="edge", log=True) 
ax.set_title("User histogram based on commits") 
ax.set_xlabel("Commits")
ax.set_ylabel("Log(number of users)")
l.remove(20)
l.remove(1000)
ax.set_xticks(l)
ax.tick_params(axis='both', which='major', labelsize=10)

#print some stats on the overall commits plot
ax.text(50000, 160000, 
	'      commits   : users', fontweight='bold')
ax.text(30000, 100000, 
	'[20-100]              92665796  : 2045427')
ax.text(30000, 65000, 
	'[100-1000]        171063588  : 704124')
ax.text(30000, 40000, 
	'[1000-10000]      76448539  : 37230')
ax.text(30000, 25000, 
	'[10000-20000]      7779302  : 578')
ax.text(30000, 16000, 
	'[20000-40000]      5061471  : 179')
ax.text(30000, 10000, 
	'[40000-60000]      2835352  : 59')
ax.text(30000, 6500, 
	'[60000-80000]      2053979  : 30')
ax.text(30000, 4500, 
	'[80000-100000]      814353  : 20')
ax.text(35000, 2600, 
	'[Total]          359722380  : 2787647')

ax.text(25000, 1600,
	'Notice 9480368 users  --filter-->  2787647 users')

ax.text(40500, 500, 
	'Commits: Min: 21, Max: 99039 ')
ax.text(56000, 300,
	'Mean: 129, Med: 52')



plt.savefig(os.path.join(out_dir,"commits_overall.png"))

o_file = open(os.path.join(out_dir,"commits_overall.p"),'wb')
pickle.dump((frq,edges), o_file)


