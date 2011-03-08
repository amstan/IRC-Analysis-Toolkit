#!/usr/bin/env python

from LogReader import *
import sys
import re

ACTION, MISC, MSG = range(3)

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
			nick = nick[1:-1].rstrip("_")
		
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
	
	nickre = re.compile("\\b(%s)*\\b" % ("|".join(re.escape(nick.lower()) for nick in nicks)))
	
	#Do some tests for the match
	print nickre.match("xenon: amstan: test").groups()
	print nickre.match("gfdsgsjhsdfrwagh").groups()
	
	#for line in log[:0]:
		#print line
		#linetype, date, nick, msg = line
		#if linetype == MSG:
			#line=line.lower()
			#if msg.find(possiblenick)!=-1:
				#print possiblenick
		
		#print "Searching for edges @ %s" % (date)
		#sys.stdout.flush()

if __name__ == "__main__":
	main()