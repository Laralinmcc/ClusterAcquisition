import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pylab
import numpy as np
from matplotlib.widgets import Button
from matplotlib.widgets import CheckButtons
import pdb
import sys
import os
import re

basedir = os.path.abspath(".")
subject = sys.argv[1]
log = open(basedir+'/'+subject+'/'+subject+'_log_cons.txt','r')
wre = re.compile('(clip)|(clap)|(slip)|(slap)|(lip)|(lap)',re.I)
k   = re.compile('(k)|(s)',re.I)
l   = re.compile('(l)',re.I)

logs = {}

line = log.readline()
line = log.readline()

while line != "":
	line = line.split()
	word = wre.search(line[2]).group()
	sub = line[0] + '_' + word + '_' + line[1]
	frame = []
	print line
	if ('K' in line) or ('S' in line) or ('k' in line) or ('s' in line):
		frame.append('K')
	if ('L' in line) or ('l' in line):
		frame.append('L')
	if sub in logs:
		logs[sub].append(frame)
	else: 
		logs[sub] = [frame]
	line = log.readline()
		

for word in logs.keys():

	try:
		fil = pylab.loadtxt(basedir+"/"+subject+"/"+subject+"_cons/"+word+".con")
	except IOError:
		pass
	if len(fil) == 100:
		fil = np.transpose(fil)
	cons = len(fil)/2
	minx = np.min(fil[0])
	maxx = np.max(fil[0])
	miny = np.min(fil[1])
	maxy = np.max(fil[1])

	for i in range(0,cons):
		minx = min(np.min(fil[i*2]),minx)
		maxx = max(np.max(fil[i*2]),maxx)
		miny = min(np.min(fil[i*2+1]),miny)
		maxy = max(np.max(fil[i*2+1]),maxy)
	frames = logs[word]
	print frames
	plt.figure(figsize=(9, 5))
	rng = min(cons, len(frames)-1)
	for i in range(rng):
		# if len(frames[i]) > 0:
		line = plt.plot(fil[i*2], fil[i*2+1])
	 	if 'L' in frames[i] and 'K' in frames[i]:
			plt.setp(line, color='darkgreen', linewidth=2.0)
		elif 'L' in frames[i] and (not ('K' in frames[i])):
			plt.setp(line, color='darkblue', linewidth=2.0)
		elif 'K' in frames[i]:
			plt.setp(line, color='gold', linewidth=2.0)
		else:
			plt.setp(line, linewidth=1.0, color = 'k', ls = 'dashed')

	print word
	fig = pylab.gcf()
	fig.canvas.set_window_title(word)
	plt.title(word)
	plt.axis([minx-10, maxx+10, maxy+10, miny-10])

	plt.savefig(basedir+'/'+subject+'/'+subject+'_plots/'+word)
	plt.close(fig)

