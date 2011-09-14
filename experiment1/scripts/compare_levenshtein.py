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

from compare_eyenalysis import cluster
import os
import os.path
from numpy import *

def chop(s):

	"""Chop a string into a list of two-character items"""

	r = []
	for i in range(0, len(s), 2):	
		r.append(s[i:i+2])		
	return r

def levenshtein2(a,b):

	"""Modified levenshtein distance to work on lists of strings"""

	a = chop(a)
	b = chop(b)

	n, m = len(a), len(b)
	if n > m:
		# Make sure n <= m, to use O(min(n,m)) space
		a,b = b,a
		n,m = m,n
		
	current = range(n+1)
	for i in range(1,m+1):
		previous, current = current, [i]+[0]*n
		for j in range(1,n+1):
			add, delete = previous[j]+1, current[j-1]+1
			change = previous[j-1]
			if a[j-1] != b[i-1]:
				change = change + 1
			current[j] = min(add, delete, change)
		    
	return current[n]
	
def levenshtein(path, sigma):

	"""Analyze a single file using Levenshtein"""
	
	trials = {}
	for trial in loadtxt(path, dtype=str, delimiter=", "):
		trials[trial[0]] = trial[1]
	
	cm = {}
	for key1, s1 in trials.iteritems():
		cm[key1] = {}
		for key2, s2 in trials.iteritems():
			if key1 == key2:
				d = 0
			elif key2 in cm and key1 in cm[key2]:
				d = cm[key2][key1]				
			else:
				d = float(levenshtein2(s1,s2)) / max(len(s1), len(s2))
			cm[key1][key2] = d
		
	cluster("lev", sigma, cm)

if __name__ == "__main__":							

	print "Method, Sigma, Score, CL0, CL1"					
	for path in os.listdir("noiselogs"):
		sigma = os.path.splitext(os.path.basename(path))[0]
		levenshtein(os.path.join("strings", path), sigma)	
