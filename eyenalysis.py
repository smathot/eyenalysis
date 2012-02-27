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

DATA FORMATS
============

A dataset consists of a dictionary where each dictionary entry is a single named
scanpath. A scanpath consists of a list of points. A point consists of a list of
coordinates.

# Create a point
pt1 = [0,0]
pt2 = [1,1]

# Create a scanpath
sp1 = [pt1, pt2]

# Create some more points
pt2 = [0.5,0.5]
pt3 = [1.5,1.5]

# Create a scanpath
sp2 = [pt2, pt3]

# Create a dataset
spd = {"sp1" : sp1, "sp2" : sp2}

USAGE
=====

from eyenalysis import *

print "Distance between sp1 and sp2:", sp_dist(sp1, sp2)
cm = cross_compare(spd)
print "Cross-compare matrix:"
for sp1 in cm:
	print sp1,
	for sp2 in cm[sp1]:
		print "%.4f" % cm[sp1][sp2],
	print
"""

from numpy import loadtxt, delete, array, mean, std
from scipy.spatial.distance import euclidean, cdist
from scipy.cluster.vq import whiten
		
def sp_dist(sp1, sp2, norm=True):

	"""
	Determines the distance between two scanpaths.
	
	Arguments:
	sp1 -- the first scanpath
	sp2 -- the second scanpath
	
	Keyword arguments:
	norm -- indicates if the distance should be normalized (default=True)
	
	Returns:
	A distance
	"""
		
	c = cdist(sp1, sp2)
	d = c.min(axis=0).sum() + c.min(axis=1).sum()
	if norm:
		d /= max(len(sp1), len(sp2))
	return d
	
def cross_compare(spd, norm=True, _whiten=True, check_identical=False):

	"""
	Cross-compare all scanpaths
	
	Arguments:
	spd -- a dictionary of scanpaths
	
	Keyword arguments:
	norm -- indicates if the distances should be normalized (default=True)	
	_whiten -- indicates if the dataset should be whitened (see whiten())
			   (default=True)
	check_identical -- indicates if an exception should occur when the distance
					   between two (non-identical) scanpaths is zero. Lots of
					   zeros in the cross-comparison matrix may result in buggy
					   clusering. (default=False)
	
	Returns:
	A matrix of pair-wise distances
	"""
	
	if _whiten:
		spd = whiten(spd)	
	cm = {}
	for sp1 in spd:
		cm[sp1] = {}
		for sp2 in spd:
			if sp1 == sp2:
				d = 0
			elif sp2 in cm and sp1 in cm[sp2]:
				d = cm[sp2][sp1]
			else:
				d = sp_dist(spd[sp1], spd[sp2], norm=norm)
				if check_identical and d == 0:
					raise Exception("Scanpaths %s and %s appear to be identical" % (sp1, sp2))
			cm[sp1][sp2] = d
	return cm
	
def whiten(spd):

	"""
	Transforms all coordinates into standard deviations from the mean. So, for
	example, a value of -0.5 would mean that this value is 0.5*std below the
	mean.
	
	Arguments:
	spd -- a dataset (dictionary of scanpaths)
	
	Returns:
	A "whitenend" dataset (dictionary of scanpaths)
	"""

	# Create a list of all points
	l = []
	for sp in spd:			
		for pt in spd[sp]:
			l.append(pt)
			
	# Compute the mean and standard deviation	
	a = array(l)
	m = mean(a, axis=0)
	s = std(a, axis=0)
	
	# Whiten the data
	_spd = {}
	for sp in spd:
		l = []
		for pt in spd[sp]:			
			l.append(list((array(pt)-m)/s))
		_spd[sp] = l
	return _spd
	
def scale(spd, scaling):

	"""
	Multiplies all coordinates by a certain scaling factor.
	
	Arguments:
	spd -- a dataset (dictionary of scanpaths)
	scaling -- a single scaling factor (for all coordinates) or a list of
			   scaling factors. If a list is passed, the length of the list
			   should match the number of coordinates.
			   
	Returns:
	A "scaled" dataset (dictionary of scanpaths)
	"""

	# Convert the scaling parameter into a numpy array
	if type(scaling) == int or type(scaling) == float:
		scaling = array([scaling])
	else:
		scaling = array(scaling)
		
	_spd = {}
	for sp in spd:
		l = []
		for pt in spd[sp]:
			if len(pt) != len(scaling) and len(scaling) != 1:
				raise Exception("The scaling list should be a single value or match the number of coordinates")
			l.append(list(array(pt)*scaling))
		_spd[sp] = l
	return _spd
	
def sp_from_txt(path, delimiter=",", skiprows=0):

	"""
	Reads a single scanpath from a file. This function expects a value-separated
	text file containing only numeric values, where each row corresponds to a
	single point.
	
	Arguments:
	path -- the file path
	
	Keyword arguments:
	delimiter -- delimiter character (default=",")
	skiprows -- the number of rows to skip. Useful for skipping non-numeric
				column headers (default=0)
				
	Returns:
	A scanpath (note: a 2-dimensional numpy array is returned, but this can be
	used interchangeably with a regular Python list for Eyenalysis)
	"""

	return loadtxt(open(path), dtype=float, delimiter=delimiter, skiprows=skiprows)
	
def spd_from_txt(path, keycol=0, delimiter=",", skiprows=0):

	"""
	Reads a dataset (a dictionary of scanpaths) from a file. This function
	expects a value-separated text file containing only numeric values, except
	for the key column, which uniquely defines each scanpaths from the dataset.
	
	Arguments:
	path -- the file path
	
	Keyword arguments:
	keycol -- the column that should be used as a key
	delimiter -- delimiter character (default=",")
	skiprows -- the number of rows to skip. Useful for skipping non-numeric
				column headers (default=0)
				
	Returns:
	A dataset (dictionary of scanpaths)
	"""	

	d = loadtxt(open(path), dtype=str, delimiter=delimiter, skiprows=skiprows)
	spd = {}
	for row in d:
		key = row[keycol]
		if key not in spd:
			spd[key] = []
		spd[key].append( [float(val) for val in delete(row, keycol)] )
	return spd
	
def kmeans(cm, k=2, i=10):

	"""
	Perform K-means clustering on a	cross-comparison matrix as returned by
	cross_compare(). Note that clustering of two perfectly segregated groups
	(i.e., groups consisting of identical items) sometimes fails, so that all
	items are clustered into the same group. Not sure why, but this appears to
	affect many implementations of K-Means clustering, not just Pycluster.
	
	This function uses Pycluster. Alternative implementations can be found in
	scipy and python-cluster:
	
	<http://bonsai.hgc.jp/~mdehoon/software/cluster/software.htm#pycluster>
	<http://docs.scipy.org/doc/scipy/reference/cluster.vq.html>
	<http://python-cluster.sourceforge.net/>
	
	Arguments:
	cm -- the cross-comparison matrix
	
	Keyword arguments:
	k -- the number of clusters (default=2)
	i -- the number of iterations (default=10)
	
	Returns:
	A key-cluster dictionary
	"""
	
	from Pycluster import kcluster
	
	# First convert the dictionary into a list of tuples so it can be handled
	# by python-cluster
	data = []
	for row in cm:
		data.append(tuple(cm[row].values()))									
			
	# Perform the clustering
	clusterid, error, nfound = kcluster(data, nclusters=k, npass=i)
	
	# Parse the results into a dictionary and return
	d = {}
	for j in range(len(clusterid)):
		d[cm.keys()[j]] = clusterid[j]	
	return d
	


