"""
iostat graphs

requires scipy

Wrote this script a loooong time ago to practice python.
Please forgive the uglyness of this script, I wrote this
when I barely knew how to program.

Parses the output of iotop and charts
a graph showing the programs using the most I/O on a linux system.

"""
import re
import matplotlib.pyplot as plt
import sys


file = open(sys.argv[1],'r')
file.readline()
line = file.readline()
proc = {}
i = 0
while line != "":
	print "line is",line
	if re.match(r"^\s*\d+", line):
		parts = re.split(r"\s+",line.strip())
		print "parts is",parts
		pname = " ".join(parts[10:])

		if pname not in proc:
			proc[pname] = [[], []]
			for x in range(i):
				proc[pname][0].append(0)
				proc[pname][1].append(0)

		proc[pname][0].append(float(parts[2]))
		proc[pname][1].append(float(parts[4]))

	elif re.match(r"^Total", line):
		i += 1

	for key in proc.keys():
		if len(proc[key][0]) < i:
			proc[key][0].append(0)
		if len(proc[key][1]) < i:
			proc[key][1].append(0)
	
	print proc
	line = file.readline()

file.close()

for key in proc:
	plt.plot(proc[key][0],label=key+" (in)")
	plt.plot(proc[key][1],label=key+" (out)")
plt.legend()
plt.show()
