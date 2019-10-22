import sys, os
from html.parser import HTMLParser
import re

#converts a cities 2 countries list of html file to txt
#python make_city2county_1000.py clean_cities2countries_1000.html cities2countries_1000.txt 

class MyHTMLParser(HTMLParser):

	def __init__(self):
		super().__init__()
		self.prev_pos = self.getpos()
		self.data = []
	
	#see if the curr pos is not prev pos
	#then this is a new line and a new data for a new city
	def handle_data(self, data):
		curr_pos = self.getpos()
		if list(curr_pos)[0] != list(self.prev_pos)[0]: 
			print(self.prev_pos, self.getpos(), "Encountered some data  :", data)
			self.prev_pos = self.getpos()
			self.data.append(data)
			

content = open(sys.argv[1]).read()

parser = MyHTMLParser()
parser.feed(content)
data = parser.data

#remove any brackets and content within it like (NY)
for c in range(len(data)):
	x = data[c]
	start = x.find( '(' )
	end = x.find( ')' )
	if start != -1 and end != -1:
		data[c] = x[:start]+x[end+1:]	
	
#write to file
with open(sys.argv[2], 'w') as f:
	for d in parser.data:
		f.write(d + "\n")
