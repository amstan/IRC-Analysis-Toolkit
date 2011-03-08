#!/usr/bin/env python

from LogReader import *
import sys
import re
import string

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
		
		nick=nick.rstrip("_")
		nicks.add(nick)
		log.append([linetype,date,nick,msg])
		
		#print "Parsing logs @ %s" % (date)
		sys.stdout.flush()
	
	return log, nicks

def main():
	reader=LogReader("logs/*.log")
	
	log, nicks = parseLog(reader)
	
	graph = {}
	for nick in nicks:
		graph[nick] = set()
	
	print "Nicks: %s" % (", ".join(nicks))
	
	nickre = re.compile("\\b(%s)\\b" % ("|".join(re.escape(toLower(nick)) for nick in nicks)))
	
	try:
		for line in log:
			linetype, date, nick, msg = line
			
			print "Searching for edges @ %s" % (date)
			sys.stdout.flush()
			
			if linetype==MSG:
				highlights=set(match.group(1) for match in nickre.finditer(toLower(msg)))
				graph[nick]|=highlights
	except KeyboardInterrupt:
		print graph["amstan"]

if __name__ == "__main__":
	main()