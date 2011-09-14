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

from eyenalysis import *
from numpy import *
import os
import os.path

# The number of trials per noise level
N = 100

def cluster(method, sigma, cm):

	"""Cluster a cross-comparison matrix"""
	
	global N

	# Perform clustering
	cl = kmeans(cm, k=2, i=1)

	# Analyze the clustering
	total = 0
	correct = 0
	cl_0 = 0
	cl_1 = 0
	for trialid, cluster in cl.iteritems():
		total += 1
		if cluster == 0:
			cl_0 += 1
		elif cluster == 1:
			cl_1 += 1
		if (int(trialid) < N/2 and cluster == 0) or (int(trialid) >= N/2 and cluster == 1):
			correct += 1
	
	# Process and print the score
	score = 1.0 * correct / total
	if score < 0.5:
		score = 1 - score
	print "%s, %s, %s, %d, %d" % (method, sigma, score, cl_0, cl_1)	

def eyenalysis(path, sigma, whiten):

	"""Analyze a single file using Eyenalysis"""
	
	spd = spd_from_txt(path, keycol=0)
	cm = cross_compare(spd, _whiten=whiten)
	if whiten:
		cluster("enl-wh", sigma, cm)
	else:
		cluster("enl-nw", sigma, cm)
	
if __name__ == "__main__":							
	print "Method, Sigma, Score, CL0, CL1"					
	for path in os.listdir("noiselogs"):
		sigma = os.path.splitext(os.path.basename(path))[0]
		eyenalysis(os.path.join("noiselogs", path), sigma, True)
		eyenalysis(os.path.join("noiselogs", path), sigma, False)

