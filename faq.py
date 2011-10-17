#!/usr/bin/env python

from LogReader import *
from supybotParser import *
import time

def faq(filelist):
	reader=LogReader(filelist)
	
	log, _ = parseLog(reader)
	
	faqs={}
	def addfaq(question):
		try:
			faqs[line[3]]+=1
		except KeyError:
			faqs[line[3]]=1
	
	for line in log:
		if line[0]==MSG:
			#check if question
			if line[3].find("?")>=0:
				#check if serious question
				if len(line[3].split())>2:
					addfaq(line[3])
	
	for q,count in sorted(faqs.items(),cmp=lambda x,y: cmp(x[1], y[1])):
		if count>1:
			print count, q

if __name__ == "__main__":
	import sys
	faq(sys.argv[1:])
