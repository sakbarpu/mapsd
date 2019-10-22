'''
Go through the mapsd files and draw country wise stats from
it. Go to each file and create unique country names.
Identify country names in the list of actual names with
tags. Create and save dictionary for each country name
identified as key and all the info about that country will
be value for that key.
'''

import sys, os
import re
import time, datetime
from iso3166 import countries
from collections import Counter

# COMMIT_FILTER = 1000

mapsd_file = sys.argv[1] #where is user file
out_dir = sys.argv[2] #which dir to save output
out_file = os.path.join(out_dir, "countrywise_" + os.path.basename(mapsd_file))
if os.path.exists(out_file):
	print ("Out file already there. Check if this batch is done already. Or remove the file and restart process")
	exit()

counter = 0 #counter for users in the file
mapsd = open(mapsd_file) #mapsd file to read
start_time = time.time() #time
countrywise = {}
for m in mapsd: #loop over all the users in the file
	counter += 1
	m_split = m.split(" ;;; ")
	country = m_split[3]
	commits = m_split[2]
	langs = m_split[4]
	reponames = m_split[5]
	repodescs = m_split[6]
	if country in countrywise: #if found in dict
		countrywise[country][0].append(commits)
		countrywise[country][1].append(langs)
		countrywise[country][2].append(reponames)
		countrywise[country][3].append(repodescs)
	else: #if not found in dict create new entry
		countrywise[country] = [[commits], [langs], [reponames], [repodescs]]

#for cn in countrywise.keys(): print (cn)

#From here onwards we try to normalize the country names
#Basically we know what countries are there in the world
#We try to identify which countries are mentioned in 
#the countrywise dict

#load actual country names
actual_countrycodes = open("../data/country_names/country_codes.txt").read().split("\n")
actual_countrynames_in_en = [x.lower() for x in open("../data/country_names/en.txt").read().split("\n")]
actual_countrynames_diff_langs = {}
diff_langs = os.listdir("../data/country_names/")
for lang in diff_langs:
	if lang == "country_codes.txt": continue
	if lang == "en.txt": continue
	langname = lang[:-4]
	actual_countrynames_diff_langs[langname] = [x.lower() for x in open(os.path.join("../data/country_names/",lang)).read().split("\n")]

#get mapping from 3 letter country codes to 2 letter actual codes that we have used as identifiers for countries in mapsd
actual_countrycodes_3letter = {}
for cc in actual_countrycodes:
	if cc not in countries: 
		continue
	actual_countrycodes_3letter[countries.get(cc.lower()).alpha3] = cc
actual_countrycodes_3letter["ACI"] = "AC"

#load cities database ~25000 cities
#(cityname,countryname,subcountryname)
cities = [x.lower() for x in open("../world-cities/data/world-cities.csv").read().strip().split("\n")]
cities = [x.split(",")[:-1] for x in cities[1:]]
mapping_countries_incitiesdatabase_to_actual_codes = {}
for city_entry in cities:
	city_country = city_entry[1]
	if city_country in actual_countrynames_in_en:
		mapping_countries_incitiesdatabase_to_actual_codes[city_country] = actual_countrycodes[actual_countrynames_in_en.index(city_country)]


#Example: (1) Vancouver, B.C. (2) Toronto, OR (3) Vancouver, BC (4) Burnaby, BC (5) Montreal, QC
#People in Canada US and many other countries has a habit of abbreviating province/state names.
#Create a database of list of provinces and states and codes
#Replace the province names by codes in world-cities database
#Check if there is a entry in that database for the string we have 

#load state codes for US states
us_state_codes = [x.lower() for x in open("../data/us_states/state_codes.txt").read().split("\n")]
us_state_names = [x.lower() for x in open("../data/us_states/state_names.txt").read().split("\n")]
#load province codes for Canada provinces
canada_province_codes = [x.lower() for x in open("../data/canada_provinces/province_codes.txt").read().split("\n")]
canada_province_names = [x.lower() for x in open("../data/canada_provinces/province_names.txt").read().split("\n")]
#load province codes for Australia provinces
australia_province_codes = [x.lower() for x in open("../data/australia_provinces/province_codes.txt").read().split("\n")]
australia_province_names = [x.lower() for x in open("../data/australia_provinces/province_names.txt").read().split("\n")]
#load province codes for Brazil provinces
brazil_province_codes = [x.lower() for x in open("../data/brazil_provinces/province_codes.txt").read().split("\n")]
brazil_province_names = [x.lower() for x in open("../data/brazil_provinces/province_names.txt").read().split("\n")]
#load province codes for China provinces
china_province_codes = [x.lower() for x in open("../data/china_provinces/province_codes.txt").read().split("\n")]
china_province_names = [x.lower() for x in open("../data/china_provinces/province_names.txt").read().split("\n")]
#load province codes for Japan provinces
japan_province_codes = [x.lower() for x in open("../data/japan_provinces/province_codes.txt").read().split("\n")]
japan_province_names = [x.lower() for x in open("../data/japan_provinces/province_names.txt").read().split("\n")]
#load province codes for Pakistan provinces
pakistan_province_codes = [x.lower() for x in open("../data/pakistan_provinces/province_codes.txt").read().split("\n")]
pakistan_province_names = [x.lower() for x in open("../data/pakistan_provinces/province_names.txt").read().split("\n")]
#load province codes for India states
india_state_codes = [x.lower() for x in open("../data/india_states/state_codes.txt").read().split("\n")]
india_state_names = [x.lower() for x in open("../data/india_states/state_names.txt").read().split("\n")]
#load province codes for Mexico states
mexico_state_codes = [x.lower() for x in open("../data/mexico_states/state_codes.txt").read().split("\n")]
mexico_state_names = [x.lower() for x in open("../data/mexico_states/state_names.txt").read().split("\n")]

#add more city entries with US state names replaced with codes
cities_to_add = []
for city_ in cities:
	if city_[1] == "united states":
		if city_[2] == '"washington':
			new_entry = [city_[0],city_[1],"DC"]
		else:
			new_entry = [city_[0],city_[1],us_state_codes[us_state_names.index(city_[2])]]
		cities_to_add.append(new_entry)
for city_ in cities_to_add: cities.append(city_)
#add more city entries with Canada province names replaced with codes
cities_to_add = []
for city_ in cities:
	if city_[1] == "canada":
		new_entry = [city_[0],city_[1],canada_province_codes[canada_province_names.index(city_[2])]]
		cities_to_add.append(new_entry)
for city_ in cities_to_add: cities.append(city_)
#add more city entries with Australia province names replaced with codes
cities_to_add = []
for city_ in cities:
	if city_[1] == "australia":
		if city_[2] == 'act':
			new_entry = [city_[0],city_[1],'ACT']
		else:
			new_entry = [city_[0],city_[1],australia_province_codes[australia_province_names.index(city_[2])]]
		cities_to_add.append(new_entry)
for city_ in cities_to_add: cities.append(city_)
#add more city entries with Brazil province names replaced with codes
cities_to_add = []
for city_ in cities:
	if city_[1] == "brazil":
		if city_[2] == "federal district": city_[2] = "distrito federal"
		new_entry = [city_[0],city_[1],brazil_province_codes[brazil_province_names.index(city_[2])]]
		cities_to_add.append(new_entry)
for city_ in cities_to_add: cities.append(city_)
#add more city entries with China province names replaced with codes
cities_to_add = []
for city_ in cities:
	if city_[1] == "china":
		if city_[2] == "ningxia hui autonomous region": city_[2] = "ningxia" 
		if city_[2] == "inner mongolia": city_[2] = "nei mongol" 
		new_entry = [city_[0],city_[1],china_province_codes[china_province_names.index(city_[2])]]
		cities_to_add.append(new_entry)
for city_ in cities_to_add: cities.append(city_)
#add more city entries with Japan province names replaced with codes
cities_to_add = []
for city_ in cities:
	if city_[1] == "japan":
		new_entry = [city_[0],city_[1],japan_province_codes[japan_province_names.index(city_[2])]]
		cities_to_add.append(new_entry)
for city_ in cities_to_add: cities.append(city_)
#add more city entries with India state names replaced with codes
cities_to_add = []
for city_ in cities:
	if city_[1] == "india":
		if city_[2] == "odisha": city_[2] = "orissa"
		if city_[2] == "puducherry": city_[2] = "pondicherry"
		new_entry = [city_[0],city_[1],india_state_codes[india_state_names.index(city_[2])]]
		cities_to_add.append(new_entry)
for city_ in cities_to_add: cities.append(city_)
#add more city entries with Mexico state names replaced with codes
cities_to_add = []
for city_ in cities:
	if city_[1] == "mexico":
		if city_[2] == "state of mexico": city_[2] = "mexico"
		if city_[2] == "mexico city": city_[2] = "mexico"
		if city_[2] == "baja california": city_[2] = "baja california sur"
		new_entry = [city_[0],city_[1],mexico_state_codes[mexico_state_names.index(city_[2])]]
		cities_to_add.append(new_entry)
for city_ in cities_to_add: cities.append(city_)

#Example: (1) London, UK (2) Shenzhen, CN (3) Raleigh, US (4) Bangalore, IN (5) Dunedin, NZ 
#Some people like to abbreviate country names in 2 letters code
#Replace in the world-cities csv file country names by 2 letters code
#Check if the string presented is there in that database
cities_to_add = []
for city_ in cities:
	country_name_tmp = city_[1]
	if country_name_tmp == "antigua and barbuda": country_name_tmp = "antigua & barbuda"
	if country_name_tmp == "aland islands": country_name_tmp = "Åland Islands".lower()
	if country_name_tmp == "saint barthelemy": country_name_tmp = "St. Barthélemy".lower()
	if country_name_tmp == "democratic republic of the congo": country_name_tmp = "Congo - Kinshasa".lower()
	if country_name_tmp == "republic of the congo": country_name_tmp = "Congo - Brazzaville".lower()
	if country_name_tmp == "ivory coast": country_name_tmp = "Côte d’Ivoire".lower()
	if country_name_tmp == "cabo verde": country_name_tmp = "cape verde".lower()
	if country_name_tmp == "curacao": country_name_tmp = "Curaçao".lower()
	if country_name_tmp == "hong kong": country_name_tmp = "Hong Kong SAR China".lower()
	if country_name_tmp == "macao": country_name_tmp = "Macao SAR China".lower()
	if country_name_tmp == "saint kitts and nevis": country_name_tmp = "St. Kitts & Nevis".lower()
	if country_name_tmp == "saint lucia": country_name_tmp = "St. Lucia".lower()
	if country_name_tmp == "saint martin": country_name_tmp = "St. Martin".lower()
	if country_name_tmp == "saint helena": country_name_tmp = "St. Helena".lower()
	if country_name_tmp == "svalbard and jan mayen":country_name_tmp = "Svalbard & Jan Mayen".lower()
	if country_name_tmp == "saint pierre and miquelon":country_name_tmp = "St. Pierre & Miquelon".lower()
	if country_name_tmp == "reunion":country_name_tmp = "Réunion".lower()
	if country_name_tmp == "turks and caicos islands":country_name_tmp = "Turks & Caicos Islands".lower()
	if country_name_tmp == "trinidad and tobago":country_name_tmp = "Trinidad & Tobago".lower()
	if country_name_tmp == ' d.c."': country_name_tmp = "United States".lower()
	if country_name_tmp == 'vatican': country_name_tmp = "Vatican City".lower()
	if country_name_tmp == 'saint vincent and the grenadines': country_name_tmp = "St. Vincent & Grenadines".lower()
	if country_name_tmp == 'wallis and futuna': country_name_tmp = "Wallis & Futuna".lower()
	country_code_tmp = actual_countrycodes[actual_countrynames_in_en.index(country_name_tmp)]
	new_entry = [city_[0], city_[1], country_code_tmp]
	cities_to_add.append(new_entry)
for city_ in cities_to_add: cities.append(city_)

#loop over extracted country names to try to identify them
#in the list of actual country names
c = 0
final_data = {}
for cc in actual_countrycodes:
	final_data[cc] = []

#read the cities2countries 1000 list 
#this is the list of largest 1000 cities
#we use it in getting country info
#mainly because largest cities are just mentioned without
#country info because they are so large and famous
largest_cities = {}
with open("../data/cities_1000/cities2countries_1000.txt") as f:
	for line in f:
		line_split = line.strip().split(",")
		large_city = line_split[0].strip().lower()
		large_city_country = line_split[1].strip().lower()
		largest_cities[large_city] = large_city_country


'''
Overall logic to identify the country names from this vague
string that we get from the github tags. 

First split the string by comma separator. 

(solid logic)
For each substring check if it is a country name in english. 
If yes then success.

(solid logic)
If not then search in any of the other ~620 languages. 
If a substring is found as a country name in any of the other 
languages then success. 

(somewhat wishy washy logic)
If not then search for a substring in the 3 letter codes for 
countries. If a substring is present in the 3 letter codes for 
countries we have found the country and success. 

(very wishy washy logic, ignore it may be)
If not then see if the location tag as present is comma 
separated and one of the substrings in this comma separated 
string is the code of a US state. If it is then the country 
name is US and success. 

(somewhat wishy washy logic)
If not search in the database of ~25000 cities. The cities
databse has three things for each entry (1) city name, (2)
subcountry name (3) country name. If the location tag is
multipart comma separated, then match parts with the three
things associated with each entry in the cities database. If
at least two of them match then success and we have found
the country name.

(more wishy washy logics to be put in place as well)
see below in todos

'''

progress_counter = 0
for x in countrywise.keys():

	if progress_counter%100 == 0: print (progress_counter, "/", len(countrywise.keys()))
	progress_counter+=1

	success = False
	x_split = x.strip().split(",") #if location tag is comma separated
	y_split = x.strip().split(" ") #if location tag is space separated
	z_split = x.strip().split("-") #if location tag is dash separated

	if success == False:
		for n in x_split:
			n = n.strip().lower().replace(".","")
			# Example: (1) Toronto, Canada (2) Germany (3) Sofia, Bulgaria (4) wuhan,china (5) NOIDA, INDIA
			if n in actual_countrynames_in_en: #if name found in english list of country names
				c+=1 
				if actual_countrycodes[actual_countrynames_in_en.index(n)] == "AL": print (x)
				final_data[actual_countrycodes[actual_countrynames_in_en.index(n)]].append(countrywise[x])
				success = True
				break
			else: #Example: (1) Puebla, México (2) Brno, Czech Republic (3) Украина (4) Charlottesville, Virginia, USA (5) 中国 
				for lang, cns in actual_countrynames_diff_langs.items(): #search for the name in all other languages country names
					if n in cns:
						c+=1
						if actual_countrycodes[cns.index(n)] == "AL": print (x)
						final_data[actual_countrycodes[cns.index(n)]].append(countrywise[x])
						success = True
						break
	#Example: (1) FRA 	
	if success == False: #if can't find by name then search in 3 letter country codes
		for n in x_split:
			if n in actual_countrycodes_3letter:
				c+=1
				final_data[actual_countrycodes_3letter[n]].append(countrywise[x])
				success = True
				#print (x)
				break

	#Example: (1) Hyderabad ,Telangana (2) Utrecht, The Netherlands (3) Sunnyvale, CA (4) East Palo Alto, California 
	#(5) São Paulo,SP - Brasil (6) Chamba, Himachal Pradesh (7) Beijing, P.R.China
	if success == False: #look into the cities database
		if len(x_split) > 1:
			x_split = [x.strip().lower() for x in x_split]
			for city_entry in cities:
				count_match = 0
				for a1 in x_split: 
					for a2 in city_entry: 
						if a1 == a2: 
							count_match+=1
				#The entries much match in at least two locations	
				if count_match >= 2:
					c+=1
					final_data[mapping_countries_incitiesdatabase_to_actual_codes[city_entry[1]]].append(countrywise[x])
					success = True
					break
	
	#Example: (1) istanbul (2) karachi (3) paris
	#Get the top 1000 cities in the world and map their names to their respective countries
	#This is based on the fact that those cities are so famous that mostly people living there refer to their location as their city and ignore the country info
	if success == False:
		if len(x_split) > 1:
			x_split = [x.strip().lower() for x in x_split]
			for large_city in largest_cities:
				for a1 in x_split:
					if a1 == large_city:
						#print (a1)
						c+=1
						final_data[mapping_countries_incitiesdatabase_to_actual_codes[largest_cities[large_city]]].append(countrywise[x])
						success = True
						break




	#Example: (1) Wrocław Poland (2) Westford MA (3) Seattle WA (4) Guangzhou China (5) Espírito Santo - Brasil
	#(6) Hefei China (7) Cambridge UK (8) Aurora CO (9) Quito - Ecuador (10) London UK
 	#People sometimes will not put comma separator in the string to separate city and country names or city and subcountry names
	#Separate the string using space separator. Remove any special symbols in the string.
	#Then search for the substrings in the world-cities database
	if success == False: #look into the cities database
		if len(y_split) > 1:
			y_split = [y.strip().lower() for y in y_split]
			for city_entry in cities:
				count_match = 0
				for a1 in y_split: 
					for a2 in city_entry: 
						if a1 == a2: 
							count_match+=1
				#The entries much match in at least two locations	
				if count_match >= 2:
					c+=1
					#print (mapping_countries_incitiesdatabase_to_actual_codes[city_entry[1]],y_split)
					final_data[mapping_countries_incitiesdatabase_to_actual_codes[city_entry[1]]].append(countrywise[x])
					success = True
					break

	if success == False: #look into the cities database
		if len(z_split) > 1:
			z_split = [z.strip().lower() for z in z_split]
			for city_entry in cities:
				count_match = 0
				for a1 in z_split: 
					for a2 in city_entry: 
						if a1 == a2: 
							count_match+=1
				#The entries much match in at least two locations	
				if count_match >= 2:
					c+=1
					#print (mapping_countries_incitiesdatabase_to_actual_codes[city_entry[1]],z_split)
					final_data[mapping_countries_incitiesdatabase_to_actual_codes[city_entry[1]]].append(countrywise[x])
					success = True
					break

	#Example: (1) San Francisco Bay Area, CA (2) Athens, GA (3) Stanford, CA (4) Hillsboro, OR (5) Bangalore, IN
	if success == False: #if above straightforward looking for country names in the different language database does not work
		if len(x_split) > 1: #look at US state names
			for n in x_split:
				n = n.strip().lower().replace(".","")
				if n in us_state_codes:
					c+=1
					final_data['US'].append(countrywise[x])	
					success == True
					#print (x)
					break


	#Example: (1) Purdue University (2) Facebook HQ
	# Names of organizations to be mapped to their respective countries. 
	#WE ARE IGNORING SUCH CASES BECAUSE THEY RARELY OCCUR AND ARE HARD TO CATCH
	#Look for a database where universities are mapped to country names. 
	#Look for another database where companies (especially software companies) are mapped to their respective databases.



	#if success == False: print (x)

#print ("\n")		
print (c, " countries out of ", len(countrywise.keys()), " entries identified")


#Flatten the final_data out
#Up until now it has following format. There is a key for a
#country code. Inside that key are values as a list. This
#list has many lists. Each of these lists has information
#about [[many commits], [many langs], [many reponames], [many
#repodescs]]. For each country code we have many of the
#above lists. We need to flatten this list so that we
#have just one list of the above format for each country
#code.

#print (list(final_data.keys()))
total_commits = 0
with open(out_file, "w") as out_f:
	out_f.write("Code1 \t Code2 \t Name \t #Developers \t #Commits \t #Languages\n")
	for country_code in final_data.keys():
		country_data = final_data[country_code]

		country_commits = []
		country_langs = []
		country_reponames = []
		country_repodescs = []
		for entry in country_data:
			country_commits.extend(entry[0])
			country_langs.extend([item for sublist in [x.split(",") for x in entry[1]] for item in sublist])
			country_reponames.extend([x.split(",") for x in entry[2]])
			country_repodescs.extend([x.split(";;;") for x in entry[3]])
		
		total_commits+=len(country_commits)

		country_commits = [int(x) for x in country_commits]
		country_langs = Counter(country_langs).most_common()

		if country_code.lower() == "ac": alpha3code = "ACIS"
		elif country_code.lower() == "ic": alpha3code = "CAIS"
		elif country_code.lower() == "ea": alpha3code = "CMEA"
		elif country_code.lower() == "dg": alpha3code = "DGCA"
		elif country_code.lower() == "xa": alpha3code = "FGXA"
		elif country_code.lower() == "xb": alpha3code = "FGXB"
		elif country_code.lower() == "ta": alpha3code = "TDCU"
		elif country_code.lower() == '': continue
		else: alpha3code = str(countries.get(country_code.lower()).alpha3)

		out_f.write(str(country_code) + "\t" + str(alpha3code) + "\t" + 
				str(actual_countrynames_in_en[actual_countrycodes.index(country_code)]) + "\t" + 
				str(len(country_commits)) + "\t" + str(sum(country_commits)) + "\t" + 
				",".join([str(x) +":"+ str(y) for x,y in country_langs]) + "\n")

print ("TOT", total_commits)
print ("Done in time:" , time.time()-start_time)


