import os.path
import sys


folder = os.path.abspath(sys.argv[1])
print(folder)
files = os.listdir(folder)
files.pop(0)
curfile = ""
subject = ""
log = open(sys.argv[2], 'r')
filepath = {}
for fil in files:
	if (subject != fil[:6]):
		subject = fil[:6]
		if (subject[-1] == '_'):
			index = subject[-2]
		else:
			index = subject[-2:]
		filepath[index] = "/home/oski/Desktop/Shared/"+folder[7:]+"/"+subject+"#.bmp"
	curfile = fil[0][:6]

line = log.readline()
curword = ""
start = True
frames = []
n = "0"
while (line != ""):
	line = line.split()
	word = line[2]
	if ((curword != word) or (n != line[-2][0])):
		if (not start):
			print("start:" + min(frames))
			print("end:" + max(frames))
			frames = []
			start = False
		curword = word
		n = line[-2][0]
		print("----------------------------------------------------")
		print(filepath[line[1]])
		print("word:" + line[2])
		start = False
	frames.append(line[len(line)-1])
	line = log.readline()
print("start:" + min(frames))
print("end:" + max(frames))

	
