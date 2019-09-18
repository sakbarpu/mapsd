'''
Read all the actorlogins csv files saved in the actorlogin
dir and extract all the unique user actorlogins along with
how many times each user interacted with the github
platform. After extracting this information save it into a
unique users file.
'''

import os

csv_files = [x for x in os.listdir() if x.endswith('.csv')]
csv_files = sorted(csv_files)
users = {}
for f in csv_files:
	print ("Working on file", f)	
	with open(f) as fi:
		fi.readline()
		for user in fi:
			u = user.strip().split(" ")[0]
			if u in users:
				users[u] += 1
			else:
				users[u] = 1

print ("\nTotal number of unique users:", len(users))

out_file = "unique_users.csv"
print ("\nWriting unique users to file:", out_file)

with open(out_file,"w") as fo:
	for k, v in users.items():
		fo.write(k + " " + str(v) + "\n")
print ("Done")
