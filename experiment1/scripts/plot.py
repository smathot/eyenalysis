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

import numpy as np
import matplotlib.pyplot as plt
from plotting import smooth
	
if __name__ == "__main__":

	d = np.loadtxt("summary.csv", dtype=str, delimiter=" , ")
	xdata = np.array(d[:,0], dtype=float)
	labels = ["Levenshtein", "Eyenalysis (raw data)", "Eyenalysis (whitened data)", "Scanmatch"]
	colors = ["#73d216", "#3465a5", "#f57900", "#cc0000"]
	colors2 = ["#8ae234", "#729fcf", "#fcaf3e", "#ef2929"]

	lw = 2
	wlen = 7
	wtype = "hanning"

	plt.figure(figsize=(12, 4))
	plt.plot(xdata, [54]*len(xdata), "-", label="Chance level", color="#555753", linewidth=lw)
	plt.rcParams['font.size'] = 10
	plt.rcParams['font.family'] = "Ubuntu"
	
	plt.suptitle("Results")	

	for col in [2, 5, 8, 11]:

		ydata = np.array(d[:,col], dtype=float)
		yerr = np.array(d[:,col+1], dtype=float)	
		_smooth = smooth(ydata, window_len=2*wlen+1, window=wtype)[wlen:-wlen]
		color = colors.pop()
		color2 = colors2.pop()	
		plt.errorbar(xdata, ydata*100, yerr=yerr*100, fmt=",", color=color2, capsize=0, elinewidth=0.5)
		plt.plot(xdata, _smooth*100, "-", label=labels.pop(), color=color, linewidth=lw)	
	
	plt.ylim(50, 104) 			
	plt.legend(fancybox=True, borderpad=1)
	plt.xlabel('Noise (sigma)') 
	plt.ylabel('Clustering accuracy (%)') 
	plt.grid(True, color=(0,0,0))
	plt.savefig("plot.svg")
	plt.show()

