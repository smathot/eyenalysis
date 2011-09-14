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

import pytools
import random

random.seed()

# Generate 100 scanpaths per noise level. The first 50 trials are based on
# picture 1, the rest on picture 2.
N = 100
min_sigma = 0
max_sigma = 2000
step_sigma = 10

print "Creating noisy scanpaths"
print "%d per noise level" % N

# Walk through each noise level
for sigma in range(min_sigma, max_sigma, step_sigma):

	print "Sigma = %d" % sigma
	path = "noiselogs/%d.csv" % sigma
	print "Saving as %s" % path

	f_out = open(path, "w")
	i = 0
	
	# Walk through each trial
	for trialid in range(N):					
		
		# Open the correct logfile, depending on which picture we're using	
		if trialid < N / 2:
			pic = 1
		else:
			pic = 2
		pic_path = "log/log%s.txt" % pic
		f_in = open(pic_path, "r")		
		
		#print "Using %s" % pic_path
		
		for l in f_in:

			# Look for something like:
			# 0000091.60ms CovertShift          (329,624) 5.085mV	
			a = l.split()
			if "CovertShift" in a:
				t = float(a[0][:-2])
				x = float(a[2][1:-1].split(",")[0])
				y = float(a[2][1:-1].split(",")[1])
				
				t += random.normalvariate(0, sigma)
				x += random.normalvariate(0, sigma)
				y += random.normalvariate(0, sigma)
				
				x = max(0, min(1280, x))
				y = max(0, min(960, y))
				t = max(0, min(5000, t))
									
				# At max(sigma) half the times, remove or add a saccade
				c = 1 - 0.5 * float(sigma) / 2000
				if random.random() > c:				
					i += 1										
					if random.randint(0, 1) == 0:					
						f_out.write("%d, %f, %d, %d\n" % (trialid, t, x, y))													
						t += random.normalvariate(0, sigma)
						x += random.normalvariate(0, sigma)
						y += random.normalvariate(0, sigma)						
						x = max(0, min(1280, x))
						y = max(0, min(960, y))
						t = max(0, min(5000, t))													
						f_out.write("%d, %f, %d, %d\n" % (trialid, t, x, y))						
				else:					
					f_out.write("%d, %f, %d, %d\n" % (trialid, t, x, y))

		f_in.close()			

	print "Average nr of changes = %.2f" % (float(i) / N)			
	f_out.close()
