import sys, os
from country_list import available_languages
from country_list import countries_for_language

out_dir = sys.argv[1]

countries = {}
for lang in available_languages():
	countries[lang] = [v for k, v in dict(countries_for_language(lang)).items()]

for lang, countrynames in countries.items():
	with open(os.path.join(out_dir,lang+".txt"), "w") as out_f:
		for countryname in countrynames:
			out_f.write(countryname + "\n")

with open(os.path.join(out_dir,"country_codes.txt"), "w") as out_f:
	for country_code in dict(countries_for_language('en')).keys():
		out_f.write(country_code + "\n")

