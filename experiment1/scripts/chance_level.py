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
from random import random, seed

if __name__ == "__main__":

	print "Method, Sigma, Score, CL0, CL1"	
	for n in range(10000):
		seed()
		cm = {}
		for i in range(100):
			cm[i] = {}
			for j in range(100):
				cm[i][j] = random()
		cluster("rnd", "NA", cm)
