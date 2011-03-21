#!/usr/bin/env python

from LogReader import *
from supybotParser import *
import sys
import re
import pygraphviz

def generateGraph(layout,filelist,outputimage):
	reader=LogReader(filelist)
	
	log, nicks = parseLog(reader)
	print "Nicks: %s" % (", ".join(nicks))
	
	#Prepare the graph
	graph = {}
	for nick in nicks:
		graph[nick] = set()
	
	#Scan for highlights, then fill the graph
	nickre = re.compile("\\b(%s)\\b" % ("|".join(re.escape(nick) for nick in nicks)))
	try:
		for line in log:
			linetype, date, nick, msg = line
			
			#show progress
			print "Searching for edges @ %s" % (date)
			sys.stdout.flush()
			
			if linetype==MSG:
				highlights=set(match.group(1) for match in nickre.finditer(msg))
				graph[nick]|=highlights
	except KeyboardInterrupt:
		pass
	
	#Remove nicks that are not referrenced
	activenicks = reduce(set.union,graph.values()) | set(nick for nick in nicks if len(graph[nick])>0)
	nicks, unactivenicks = activenicks, nicks
	
	#Generate the graphwiz
	print "Generating the graph..."
	sys.stdout.flush()
	
	G = pygraphviz.AGraph(strict=False, directed=True)
	G.add_nodes_from(nicks)
	
	for nick, highlights in graph.items():
		for highlight in highlights:
			G.add_edge(nick,highlight)
	
	G.layout(prog=layout)
	G.draw(outputimage)
	print "Done"

if __name__ == "__main__":
	generateGraph(sys.argv[1],sys.argv[2:],"graph.svg")