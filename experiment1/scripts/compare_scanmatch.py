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
import os.path

if __name__ == "__main__":

	p_sigma = None
	print "Method, Sigma, Score, CL0, CL1"
	
	for l in open("scanmatch/scanmatch_output.txt"):
	
		path, sp1, sp2, score = l.split()
		sigma = int(os.path.splitext(os.path.basename(path))[0])	
	
		# Remove the commas which have been accidentally added to the trialids
		sp1 = sp1[:-1]
		sp2 = sp2[:-1]
	
		# Determine the start of a new trial	
		if sigma != p_sigma:
		
			# Cluster the previous trial
			if p_sigma != None:
				cluster("scm", p_sigma, cm)
				
			p_sigma = sigma
			cm = {}

		if sp1 not in cm:
			cm[sp1] = {}
		cm[sp1][sp2] = float(score)
	
	cluster("scm", p_sigma, cm)
		
