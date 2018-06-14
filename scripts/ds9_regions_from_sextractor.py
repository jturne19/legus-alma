"""

"""
import numpy as np 

def get_regions(cat):
	""" function that takes the catalog output from sextractor and turns it into ds9 readable region files

	cat:	string; name of the sextractor catalog

	"""
	# read in pertinent information from the cat file
	kron, x, y, A, B, pa = np.loadtxt(cat, usecols=[5,8,9,18,19,20], unpack=True)

	f = open(cat.replace('.cat', '.reg'), 'w')
	f.write('image\n')

	for i in range(len(kron)):
		f.write('ellipse(%f, %f, %f, %f, %f)\n'%(x[i], y[i], kron[i]*A[i], kron[i]*B[i], pa[i]))

	f.close()
