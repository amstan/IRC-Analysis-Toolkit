#!/usr/bin/env python

import os
import glob

class LogReader:
	def __init__(self, files):
		self.filelist=glob.glob(os.path.expanduser(files))
		self.filelist.sort()
		print "Logs to read: %s" % (self.filelist)
	
	def __iter__(self):
		for filename in self.filelist:
			print "Reading %s..." % filename
			with open(filename) as f:
				for line in f.readlines():
					yield line[:-1]

if __name__="__main__":
	reader=LogReader("logs/*")
	
	for line in reader:
		print line