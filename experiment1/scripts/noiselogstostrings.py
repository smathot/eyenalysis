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

import numpy
import math
import os.path

dl = []

def xy_to_s(x, y, fix_list):

	"""Convert coordinates to a string of 'aA' form"""
	
	x = max(0, min(1280, x))
	y = max(0, min(960, y))	
	_x = int(x) / (1280 / 25)
	_y = int(y) / (960 / 25)
	a = chr(ord("a") + _x)
	b = chr(ord("A") + _y)		
	fix_list.append( (_x, _y) )	
	return a + b
	
def determine_sacc_size(fix_list):

	"""Determine the saccade size from a list of fixations"""

	global dl

	for i in range(1, len(fix_list)):	
		x1, y1 = fix_list[i-1]
		x2, y2 = fix_list[i]
		d = math.sqrt( (x1-x2)**2 + (y1-y2)**2 )
		dl.append(d)

def convert(path):

	"""Convert a single noiselog to a string"""
	
	print "Converting", path

	f_in = open(path, "r")
	f_out = open("strings/%s" % os.path.basename(path), "w")
	
	# Walk through all lines in the input file
	fix_list = []
	p_trialid = -1
	for l in f_in:
	
		# Extract the trialid and the x,y,t coordinates
		trialid, t, x, y = l.split(",")
		t = float(t)
		x = float(x)
		y = float(y)
		
		# If we encounter a new trial, output the previous trial
		if trialid != p_trialid:			
			if p_trialid >= 0:
				f_out.write("%s, %s\n" % (p_trialid, s))
			s = ""
			c = ""
			p_t = 0
			p_trialid = trialid
			determine_sacc_size(fix_list)
			fix_list = []
					
		# Determine the fixation duration of the previous fixation
		# and print the previous fixation again for each 100ms
		fix_dur = t - p_t		
		for i in range(int(fix_dur / 100)):
			s += c
		
		c = xy_to_s(x, y, fix_list)
		s += c
		
	f_out.write("%s, %s\n" % (p_trialid, s))		
	f_out.close()
	f_in.close()

for path in os.listdir("noiselogs"):
	path = os.path.join("noiselogs", path)
	convert(path)

print "Standard deviation of saccade sizes:", numpy.std(dl)
