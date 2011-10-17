#!/usr/bin/env python

from LogReader import *
from supybotParser import *
import time

def faq(filelist):
	reader=LogReader(filelist)
	
	log, _ = parseLog(reader)
	
	faqs={}
	
	for line in log:
		if line[0]==MSG:
			if line[3].find("?")>=0:
				try:
					faqs[line[3]]+=1
				except KeyError:
					faqs[line[3]]=1
	
	for q,count in faqs.items():
		if count>1:
			print count, q

if __name__ == "__main__":
	import sys
	faq(sys.argv[1:])
	