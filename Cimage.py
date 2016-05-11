import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pylab
import numpy as np

import pdb
import sys
import os
import re

"""
This script is for generating a plots for contours using a .cons file and log file.
Assumes that it is placed in a folder that contains the subject whose plots you are generating. 
Assumes the subject folder contains the files:
		[Subject]_log_cons.txt

Assumes the subject folder contains the folders:
		[Subject]_plots (Where the images will be saved)
		[Subject]_cons (Where the Edgetrak .con files are)
			-> .con files should be named [Subject]_[word]_[rep].con

Run the script with: python Cimage.py [subject]

@Author Lara McConnaughey
"""

basedir = os.path.abspath(".")
subject = sys.argv[1]
log = open(basedir+'/'+subject+'/'+subject+'_log_cons.txt','r') #opens the log file for reading
wre = re.compile('(clip)|(clap)|(slip)|(slap)|(lip)|(lap)',re.I)
k   = re.compile('(k)|(s)',re.I)
l   = re.compile('(l)',re.I)

logs = {} #Dictionary that contains information about a word_repetition 
		  # with keys as [word]_[rep] and values as a list of lists with 
		  # each sublist representing a frame. The sublist will contain 
		  # 'K' and/or 'L' representing the contour of the frame.

line = log.readline()
line = log.readline()

#iterates through the log generating the LOGS dictionary
while line != "":
	line = line.split()
	word = wre.search(line[2]).group()
	sub = line[0] + '_' + word + '_' + line[1]
	frame = []
	if ('K' in line) or ('S' in line) or ('k' in line) or ('s' in line):
		frame.append('K')
	if ('L' in line) or ('l' in line):
		frame.append('L')
	if sub in logs:
		logs[sub].append(frame)
	else: 
		logs[sub] = [frame]
	line = log.readline()

#iterates through the .cons files generating plot images.
for word in logs.keys():

	try:
		fil = pylab.loadtxt(basedir+"/"+subject+"/"+subject+"_cons/"+word+".con")
	except IOError:
		pass

	if len(fil) == 100:
		fil = np.transpose(fil) #trnsposes the file so columns of 2 are xy coordinate pairs
	
	minx = np.min(fil[0])
	maxx = np.max(fil[0])
	miny = np.min(fil[1])
	maxy = np.max(fil[1])

	# number of contours tracked in the .cons file
	cons = len(fil)/2

	for i in range(0,cons):
		minx = min(np.min(fil[i*2]),minx)
		maxx = max(np.max(fil[i*2]),maxx)
		miny = min(np.min(fil[i*2+1]),miny)
		maxy = max(np.max(fil[i*2+1]),maxy)

	frames = logs[word]

	# generates figure window 9x5
	plt.figure(figsize=(9, 5))

	# Number of contours to plot will be based on whether or not all
	# of the frames were Edgetraked. (Some of the frames that were not 
	# tracked to see why check the Edgetrak Notes
	rng = min(cons, len(frames)-1)

	# plots contours on the figure using Gold for 'K', Blue for 'L',
	# Green for 'L' and 'K' and Black Dashed for neither
	for i in range(rng):
		# if len(frames[i]) > 0:  (to only plot 'L' and 'K')
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
	plt.title(word) #Sets the title of the fig to [Subject]_[word]_[rep]
	plt.axis([minx-10, maxx+10, maxy+10, miny-10])

	plt.savefig(basedir+'/'+subject+'/'+subject+'_plots/'+word) #Saves the figure in [Subject]_plots
	plt.close(fig)

