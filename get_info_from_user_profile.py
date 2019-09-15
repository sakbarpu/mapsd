'''
Go through the unique users file and read few users from
it. Go to the github webpages of these users and download
the html data from their webpage. Extract the country and 
other information from that webpage if present.
'''

import sys, os
import re
import urllib.request, urllib.error
import time, datetime
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
percent_users_to_write = 5 #this percent users to write inside the loop (kind of like event)
num_users_total = end_users - start_users
num_users_to_write = ceil((percent_users_to_write/100) * num_users_total)

num_users_done = 0 #num of users done
num_users_couldnot_find = 0 #couldn't find this many users
num_users_no_country = 0
num_users_no_langs = 0
num_users_no_repos = 0
num_users_no_descs = 0

users = open(user_file) #users file to read
for i in range(start_users): users.readline()

start_time = time.time() #time
mapsd = {} #data to store (a dict for each user and info)

print ("Reading users file from", start_users, "to", end_users)
print ("Percent users to write at a time", percent_users_to_write)
print ("Num users to write at a time", num_users_to_write)
for u in users: #loop over all the users in the file
	num_users_done += 1
	u_split = u.strip().split()
	user = u_split[0]
	num_commits = u_split[1]

	if counter == end_users: break
	counter += 1
	
	user_homepage = github_page + user + "?tab=repositories"
	try:
		conn = urllib.request.urlopen(user_homepage)
	except urllib.error.HTTPError as e:
		num_users_couldnot_find += 1
	except urllib.error.URLError as e:
		num_users_couldnot_find += 1
	else:
		data = conn.read().decode('utf-8')

		match_country = re.search('\"Home location: (.*)\" class', data)
		if match_country: country = match_country.group(1)
		else: 	
			num_users_no_country += 1
			continue

		match_langs = re.findall('<span itemprop=\"programmingLanguage\">(.*)</span>', data)
		if match_langs:	langs = match_langs
		else: 
			num_users_no_langs += 1
			langs = []

		match_reponames = re.findall('itemprop=\"name codeRepository\" >\n(.*)</a>', data)
		if match_reponames: reponames = [x.strip() for x in match_reponames]
		else: 
			num_users_no_repos += 1
			reponames = []

		match_repodescs = re.findall('itemprop=\"description\">\n(.*)',data)
		if match_repodescs: repodescs = match_repodescs
		else: 
			num_users_no_descs += 1
			repodescs = []

		mapsd[user] = [num_users_done, num_commits, country, langs, reponames, repodescs]
		#print (mapsd[user])

	if num_users_done % num_users_to_write == 0 or num_users_done == num_users_total:  
		with open(out_file, "a") as map_f:
				for u_map, u_val in mapsd.items():
					map_f.write(str(u_val[0]) + " ;;; " + 
							u_map + " ;;; " + 
							u_val[1] + " ;;; " + 
							u_val[2] + " ;;; " + 
							",".join(u_val[3]) + " ;;; " + 
							",".join(u_val[4]) + " ;;; " +
							 ";;".join(u_val[5]) + "\n")

		print ("Users:: Total:", num_users_total ,", Done: ", num_users_done, 
			", 404 Not found: ", num_users_couldnot_find, 
			", No country: ", num_users_no_country, 
			", No languages: ", num_users_no_langs, 
			", No repositories: ", num_users_no_repos, 
			", No descriptions: ", num_users_no_descs, 
			", Time:: ", datetime.timedelta(seconds=time.time() - start_time))

		mapsd = {}
				

print ("Data saved at ", out_file)
print ("Done in time:" , time.time()-start_time)
