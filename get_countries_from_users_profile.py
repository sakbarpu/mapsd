'''
Go through the unique users file and read top few users from
it. Go to the github webpages of these users and download
the html data from their webpage. Extract the country
information from that webpage if present.
'''

import sys, os
import re
import urllib.request
import time

user_file = sys.argv[1]
how_many_users = int(sys.argv[2])
github_page = "https://github.com/"

c = 0
users = open(user_file)
start = time.time()
with open("users_countries.csv", "w") as f:
	for u in users:
		u = u.strip().split()[0]
		if c == how_many_users: break
		c+=1

		data = urllib.request.urlopen(github_page + u).read().decode('utf-8')
		m = re.search('\"Home location: (.*)\" class', data)
		if m: 
			country = m.group(1)
			f.write(u + " " + country + "\n")

print ("Done in time:" , time.time()-start)
