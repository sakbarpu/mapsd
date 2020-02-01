import sys
import matplotlib.pyplot as plt
import numpy as np

#population and gdp from https://data.worldbank.org/ 

gdp_f = sys.argv[1]
pop_f = sys.argv[2]
dev_f = sys.argv[3]

gdp = {}
with open(gdp_f) as f:
	for l in f:
		l = l.strip().split("\t")
		if len(l) == 3: 
			gdp[l[1]] = [l[0],l[2]]
print (gdp.keys())

pop = {}
with open(pop_f) as f:
	for l in f:
		l = l.strip().split("\t")
		if len(l) == 3:
			pop[l[1]] = [l[0],l[2]]
print (pop.keys())

dev = {}
with open(dev_f) as f:
	for l in f:
		l = l.strip().split("\t")
		if l[0] == "Code2": continue
		dev[l[0]] = [l[1],l[2]]
print (dev.keys())

not_there = []
gdps_data = []
devs_data = []
country_data = []
for k in dev:
	if k in gdp:
		country_name = gdp[k][0]
		population_value = float(pop[k][1])*1000
		gdp_value = float(gdp[k][1])
		devs_value = float(dev[k][1])
#		if population_value < 1000000 or population_value > 400000000: 
#			print (country_name, population_value)
#			continue
		country_data.append(country_name)
		#gdps_data.append(gdp_value/population_value)
		gdps_data.append(gdp_value)
		devs_data.append(devs_value)
	else:
		not_there.append(k)

#print ("not there")
#print (not_there)
#print (len(not_there))
i = 0
for c, g, d in zip(country_data, gdps_data, devs_data):
	print (i, c, g, d)
	i+=1
	#if g>175000: exit()

names = np.array(country_data)

fig,ax = plt.subplots()
sc = plt.scatter(gdps_data, devs_data)
ax.set_title("GDP vs Number of Developers")
ax.set_xlabel("GDP")
ax.set_ylabel("Developers")
print (country_data)
to_print_countries = ['United States', 'China', 'India', 'Germany','Canada', 'Brazil', 'Japan'] 

for i, txt in enumerate(country_data):
    if txt not in to_print_countries: continue
    ax.annotate(txt, (gdps_data[i], devs_data[i]))
plt.show()

fig,ax = plt.subplots()
sc = plt.scatter(gdps_data,devs_data)

annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))
annot.set_visible(False)

def update_annot(ind):

    pos = sc.get_offsets()[ind["ind"][0]]
    annot.xy = pos
    text = "{}, {}".format(" ".join(list(map(str,ind["ind"]))), 
                           " ".join([names[n] for n in ind["ind"]]))
    annot.set_text(text)
    annot.get_bbox_patch().set_alpha(0.4)


def hover(event):
    vis = annot.get_visible()
    if event.inaxes == ax:
        cont, ind = sc.contains(event)
        if cont:
            update_annot(ind)
            annot.set_visible(True)
            fig.canvas.draw_idle()
        else:
            if vis:
                annot.set_visible(False)
                fig.canvas.draw_idle()


fig.canvas.mpl_connect("motion_notify_event", hover)
ax.set_title("GDP vs Number of Developers")
ax.set_xlabel("GDP")
ax.set_ylabel("Developers")
plt.show()




