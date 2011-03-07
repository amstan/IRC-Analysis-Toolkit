#!/usr/bin/env python

from LogReader import *
import re

msgSplitPattern = re.compile(r"<([^>]+)>")

reader=LogReader("logs/*.log")

lines = []
for line in reader:
	print line
	line = re.split(msgSplitPattern, line, maxsplit=2)
	#lines.append(line)
	print "%s %s" % (len(line), line)