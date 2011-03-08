#!/usr/bin/env python

from LogReader import *
import sys
import re
import string
import pygraphviz

ACTION, MISC, MSG = range(3)

#From supybot
_rfc1459trans = string.maketrans(string.ascii_uppercase + r'\[]~',
                                 string.ascii_lowercase + r'|{}^')
def toLower(s, casemapping=None):
	"""s => s
	Returns the string s lowered according to IRC case rules."""
	if casemapping is None or casemapping == 'rfc1459':
		return s.translate(_rfc1459trans)
	elif casemapping == 'ascii': # freenode
		return s.lower()
	else:
		raise ValueError, 'Invalid casemapping: %r' % casemapping

def parseLog(reader):
	log = []
	nicks = set()

	for line in reader:
		date, _, nick, msg = line.split(' ',3)
		
		if nick=="*":
			linetype = ACTION
			nick, msg = msg.split(' ',1)
		elif nick=="***":
			linetype = MISC
			nick, msg = msg.split(' ',1)
		else:
			linetype = MSG
			nick = nick[1:-1]
		
		nick=toLower(nick.rstrip("_"))
		msg=toLower(msg)
		nicks.add(nick)
		log.append([linetype,date,nick,msg])
		
		#show progress
		print "Parsing logs @ %s" % (date)
		sys.stdout.flush()
	
	return log, nicks

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