#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
Copyright 2012 Sebastiaan Mathot
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

ABOUT
=====
This script generates a plot of the average similarity, as determined by
eyenalysis, as a function of the number of dimensions and the scanpath length.
"""

from eyenalysis import *
import numpy as np
from matplotlib import pyplot

if __name__ == "__main__":

	n = 1000
	aLen = range(1,33)
	aNDim = [1,2,4,8,16]
	colors = ["#73d216", "#3465a5", "#f57900", "#cc0000", "#729fcf", "#75507b"]
	pyplot.figure(figsize=(5, 4))
	pyplot.rcParams['font.size'] = 10
	pyplot.rcParams['font.family'] = "Ubuntu"
	pyplot.xlim( (0,33) )	

	for nDim in aNDim:
		yData = []
		yErr = []
		for l in aLen:
			lDist = []		
			for i in range(n):		
				sp1 = np.random.random( (l,nDim) )
				sp2 = np.random.random( (l,nDim) )
				lDist.append( sp_dist(sp1, sp2))
			aDist = np.array(lDist)			
			yData.append(aDist.mean())
			yErr.append(aDist.std())
		pyplot.plot(aLen, yData, label='%d' % nDim, color=colors.pop(), \
			linewidth=2)
		
	pyplot.legend(title='Nr. of dimensions', ncol=3, fancybox=True)
	pyplot.xlabel('Sequence length') 
	pyplot.ylabel('Mean similarity') 	
	pyplot.savefig('plots/randomDataSim.svg')
	pyplot.show()
