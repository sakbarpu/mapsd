'''
Go through the unique users file and read few users from
it. Go to the github webpages of these users and download
the html data from their webpage. Extract the country and 
other information from that webpage if present.
'''

import sys, os
import re
import urllib.request, urllib.error
import time
from math import ceil

user_file = sys.argv[1] #where is user file
start_users = int(sys.argv[2]) #from where to start read
end_users = int(sys.argv[3]) #from to end reading
out_dir = sys.argv[4] #which dir to save output
out_file = os.path.join(out_dir, "mapsd_" + str(start_users) + "_" + str(end_users) + ".csv")
if os.path.exists(out_file):
	print ("Out file already there. Check if this batch is done already. Or remove the file and restart process")
	exit()
github_page = "https://github.com/" #homepage for github

counter = start_users #counter for users in the file
num_users_done = 0 #num of users done
percent_users_to_write = 5 #this percent users to write inside the loop (kind of like event)
num_users_to_write = ceil((percent_users_to_write/100) * (end_users - start_users))
num_users_couldnot_find = 0 #couldn't find this many users
users = open(user_file) #users file to read
for i in range(start_users): users.next()
start = time.time() #time
mapsd = {} #data to store (a dict for each user and info)

print ("Reading users file from", start_users, "to", end_users)
print ("Percent users to write at a time", percent_users_to_write)
print ("Num users to write at a time", num_users_to_write)
for u in users: #loop over all the users in the file
	u_split = u.strip().split()
	user = u_split[0]
	num_commits = u_split[1]

	if counter == end_users: break
	counter += 1
	
	user_homepage = github_page + user + "?tab=repositories"
	print (user_homepage)
	try:
		conn = urllib.request.urlopen(user_homepage)
	except urllib.error.HTTPError as e:
		print ("Couln't find ", user_homepage)
		num_users_couldnot_find += 1
	except urllib.error.URLError as e:
		print ("Couln't find ", user_homepage)
		num_users_couldnot_find += 1
	else:
		data = conn.read().decode('utf-8')

		match_country = re.search('\"Home location: (.*)\" class', data)
		if match_country: country = match_country.group(1)
		else: continue

		match_langs = re.findall('<span itemprop=\"programmingLanguage\">(.*)</span>', data)
		if match_langs:	langs = match_langs
		else: langs = []

		match_reponames = re.findall('itemprop=\"name codeRepository\" >\n(.*)</a>', data)
		if match_reponames: reponames = [x.strip() for x in match_reponames]
		else: reponames = []

		match_repodescs = re.findall('itemprop=\"description\">\n(.*)',data)
		print ("\n")
		if match_repodescs: 
			for x in match_repodescs: print (x)
		else: repodescs = []

		mapsd[user] = [num_commits, country, langs]
		#print (mapsd[user])
	
	num_users_done += 1
	if num_users_done % num_users_to_write == 0:  
		with open(out_file, "a") as map_f:
				for u_map, u_val in mapsd.items():
					map_f.write(u_map +
\
" ;;; " + u_val[0] + " ;;; " + u_val[1] + " ;;; " +
",".join(u_val[2]) + " ;;; " + ",".join(u_val[3] + ";;".join(u_val[4]) + "\n")
		mapsd = {}
				

print ("Data saved at ", out_file)
print ("Done in time:" , time.time()-start)
