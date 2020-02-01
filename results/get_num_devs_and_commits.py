content = open("developers.txt").read().strip().split("\n")
num_devs = {}
for x in content[1:]:
	x_split = x.split("\t")
	num_devs[x_split[1]] = int(x_split[-1])
print ("number of developers:", num_devs)

content = open("commits.txt").read().strip().split("\n")
num_comms = {}
for x in content[1:]:
	x_split = x.split("\t")
	num_comms[x_split[1]] = int(x_split[-1])
print ("number of commits:", num_comms)

devs_data = []
comms_data = []
to_print_countries = ['china', 'india', 'germany','canada', 'brazil', 'japan', 'pakistan', 'bangladesh', 'nigeria', 'france', 'australia']
#for k,d in num_devs.items():
#	if k in to_print_countries:
#		c = num_comms[k]
#		devs_data.append(d)
#		comms_data.append(c)

for k in to_print_countries:
	devs_data.append(num_devs[k])
	comms_data.append(num_comms[k])

import matplotlib.pyplot as plt
fig,ax = plt.subplots()
sc = plt.scatter(devs_data,comms_data)
ax.set_title("Number of Developers vs Number of Commits")
ax.set_xlabel("Developers")
ax.set_ylabel("Commits")

#for i, txt in enumerate(list(num_devs.keys())):
for i, txt in enumerate(to_print_countries):
	#if txt not in to_print_countries: continue
	ax.annotate(txt, (devs_data[i], comms_data[i]))

plt.show()

