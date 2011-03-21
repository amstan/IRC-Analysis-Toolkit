#!/usr/bin/env python
#Parses supybot's logfiles. Format Example:
#2010-09-10T01:13:23  <amstan> heheh
#2010-09-10T01:51:20  *** lava <lava!~lava-699.233.432.400.austin.res.rr.com> has quit IRC (Quit: Konversation Terminated)

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
		
		nick=toLower(nick.rstrip("_"))
		msg=toLower(msg)
		nicks.add(nick)
		log.append([linetype,date,nick,msg])
		
		#show progress
		print "Parsing logs @ %s" % (date)
		sys.stdout.flush()
	
	return log, nicks

if __name__ == "__main__":
	import sys, LogReader
	
	reader=LogReader.LogReader(sys.argv[1:])
	
	print parseLog(reader)