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
import os.path

print "Reading data1.csv"
spd = spd_from_txt(os.path.join("example-data", "data1.csv"), keycol=0, skiprows=1)
for key in spd:
	print key, ":", spd[key]
print

print "Cross-comparing"
cm = cross_compare(spd)
for key1 in cm:
	print key1,
	for key2 in cm[key1]:
		print "%.2f" % cm[key1][key2],
	print
print

print "Clustering"
cl = kmeans(cm, k=2,i=10)
for key in cl:
	print key, cl[key]
