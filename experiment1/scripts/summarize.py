#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
Copyright 2011 Sebastiaan Mathot
<http://www.cogsci.nl/smathot>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import os.path
from numpy import *

d = {}

for run in os.listdir("run"):
	for fname in ["eyenalysis.csv", "scanmatch.csv", "levenshtein.csv"]:
		path = os.path.join("run", run, "score", fname)
		data = loadtxt(path, dtype=str, skiprows=1, delimiter=", ")
		for row in data:
			method = row[0]
			sigma = int(row[1])
			if sigma == 0:
				# A quick hack to correct for buggy clustering in the no noise
				# condition.
				score = 1.0
			else:
				score = float(row[2])			
			if sigma not in d:
				d[sigma] = {}			
			if method not in d[sigma]:
				d[sigma][method] = []			
			d[sigma][method].append(score)
			
for sigma in sorted(d.keys()):
	methods = d[sigma]
	print sigma,
	_l = {}
	for method, scores in methods.iteritems():		
		a = array(scores)
		print ",", method, ",", a.mean(), ",", a.std()/sqrt(len(a)),
		_l[method] = a		
	for method1, scores1 in methods.iteritems():
		for method2, scores2 in methods.iteritems():			
			a = array(scores1) - array(scores2)			
			contrast = "%s::%s" % (method1, method2)						
			print ",", contrast, ",", a.mean(), ",", a.std()/sqrt(len(a)),	
	print
	

	
