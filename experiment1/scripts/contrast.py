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
import numpy as np
from bayes import uniform_bf as ubf
from bayes import slider
import matplotlib.pyplot as plt
from matplotlib import cm
from plotting import smooth, heatcurve

wlen = 7

d = np.loadtxt("summary.csv", dtype=str, skiprows=1, delimiter=", ")

for col in [38, 41, 47]:

	xdata = np.array(d[:,0], dtype=float) 
	ydata = np.array(d[:,col], dtype=float)*100
	yerr = np.array(d[:,col+1], dtype=float)*100
	a = np.swapaxes([ydata, yerr], 0, 1)

	_smooth = smooth(ydata, window_len=2*wlen+1)[wlen:-wlen]

	bfl = slider(a, wlen=wlen, lower=0, upper=46)
		
	fig = heatcurve(xdata, ydata, cdata=_smooth, yerr=yerr, yheat=np.log10(bfl),
		heatrange=(-3,3), threshold=2, size=(12,4), heatlabel="Log10(Bf)",
		ticks=range(-3,4))
	plt.xlabel('Noise (sigma)', figure=fig) 
	plt.ylabel('Difference in clustering accuracy (%)', figure=fig) 
	if col == 47:
		plt.ylim(-5, 50, figure=fig) 	
	else:
		plt.ylim(-5, 25, figure=fig) 	
	
	plt.rcParams['font.size'] = 10
	plt.rcParams['font.family'] = "Ubuntu"	
	fig.savefig("contrast-%.2d.svg" % col)
	
			
	
