'''
Using the country_list library create a list of all
countries in many different languages (~620). Store them in
a disk.

'''

import sys, os
from country_list import available_languages
from country_list import countries_for_language

out_dir = sys.argv[1]

#create a dict for each language. for each language key load
#the country names in that language as a list and store.
countries = {}
for lang in available_languages():
	countries[lang] = [v for k, v in dict(countries_for_language(lang)).items()]

#write country names list in a separate file for each language
for lang, countrynames in countries.items():
	with open(os.path.join(out_dir,lang+".txt"), "w") as out_f:
		for countryname in countrynames:
			out_f.write(countryname + "\n")

#write 2 letter country codes for each language as well
with open(os.path.join(out_dir,"country_codes.txt"), "w") as out_f:
	for country_code in dict(countries_for_language('en')).keys():
		out_f.write(country_code + "\n")

