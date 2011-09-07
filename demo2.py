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

print "Reading data2A.csv"
sp1 = sp_from_txt(os.path.join("example-data", "data2A.csv"))
print "Reading data2B.csv"
sp2 = sp_from_txt(os.path.join("example-data", "data2B.csv"))
print "Reading data2C.csv"
sp3 = sp_from_txt(os.path.join("example-data", "data2C.csv"))
print "Reading data2D.csv"
sp4 = sp_from_txt(os.path.join("example-data", "data2D.csv"))

spd = {"sp1" : sp1, "sp2" : sp2, "sp3" : sp3, "sp4" : sp4}

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
cl = kmeans_cluster(cm, k=2,i=10)
for key in cl:
	print key, cl[key]
