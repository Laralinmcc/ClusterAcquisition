import os.path
import sys

""" This script prints useful information for edgetraking.
	Assumes the subject folder contains the files:
		[Subject]_log_cons.txt

	Assumes the subject folder contains the folders:
		[Subject]_contours (Where the ultrasound frames are stored)
		
	Run the script with: python Filepath.py [Subject]

	@author Lara McConnaughey
"""

sub = sys.argv[1]
path = os.path.abspath(sub)
abspath = "/home/oski/Desktop/Shared/sf_Clutster_Acquisition/" + sub + "/" + sub + "_contours/"

cons_folder = path + "/" + sub + "_contours"
print(cons_folder)

files = os.listdir(cons_folder)
files.pop(0)
curfile = ""
subject = ""

log = path + "/" + sub + "_log_cons.txt"
log = open(log, 'r')

line = log.readline()
curword = ""
start = True
frames = []
while (line != ""):
	line = line.split()
	word = line[2]
	if curword != word:
		if (not start):
			print("start:" + str(min(frames)))
			print("end:" + str(max(frames)))
			frames = []
			start = False
		curword = word
		print("----------------------------------------------------")
		rep = line[1]
		print(abspath + sub + "_" + rep + "_#.bmp")
		print("word:" + line[2])
		start = False
	frames.append(int(line[len(line)-1]))
	line = log.readline()
print("start:" + str(min(frames)))
print("end:" + str(max(frames)))

	
