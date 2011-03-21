#!/usr/bin/env python

from LogReader import *
from supybotParser import *
import re
import time
#import matplotlib.pyplot

enter = re.compile("(<.*>) (has joined #\w*)")
quit = re.compile("(<.*>) (has quit (IRC|irc)|has left #\w*) (\(.*\))")

def populationGraph(filelist,outputimage):
	reader=LogReader(filelist)
	
	log, _ = parseLog(reader)
	
	population = 0
	plot = ([],[])
	
	for line in log:
		if line[0]==MISC:
			matches = (enter.match(line[3]),quit.match(line[3]))
			
			if matches[0] is not None:
				population += 1
				print "ENTER",
			elif matches[1] is not None:
				population -= 1
				print "QUIT",
			else:
				continue
			
			timestamp=time.strptime(line[1],"%Y-%m-%dT%H:%M:%S")
			
			print "%s population: %s, reason: %s" % (line[1],population,line[3])
			
			plot[0].append(timestamp)
			plot[1].append(population)
	
	print plot


if __name__ == "__main__":
	import sys
	populationGraph(sys.argv[1:],"graph.svg")
	