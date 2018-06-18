"""
"""
import numpy as np
from astropy.coordinates import SkyCoord, search_around_sky
import astropy.units as u
import matplotlib.pyplot as plt
from astropy.io import fits
from scipy import stats

def nearest_cluster(dustreg, main_dir='/uwpa2/turner/legus-alma/'):
	"""
	find the nearest clusters to the input alma band4 and band7 dust regions
	
	dustreg:	degree region file of dust regions
	main_dir:	path to the main legus-alma directory in which everything sits

	Outputs:
	c:			SkyCoord object for the dust regions
	ra, dec, age, mass, excess, c_clusters:
		gives the closest 3 star clusters to the input dust regions

	"""
	# read in the ALMA dust regions that lie within the footprint
	xstr, ystr = np.loadtxt(dustreg, skiprows=3, usecols=[0,1], dtype='str', delimiter=',', unpack=True)

	# get rid of 'ellipse(' and convert to float
	x = np.array([ float(s[8:]) for s in xstr])
	y = np.array([ float(s) for s in ystr])


	# read in LEGUS cluster stuff from the catalog with just classes 1, 2, and 3
	ra, dec, age, mass, excess = np.loadtxt(main_dir + 'science/legus/ngc628-c_clusters_class123.cat', usecols=[3,4,16,19,22], unpack=True)

	# take x and y coords to make astropy skycoord objects for band 4
	c = SkyCoord(x*u.deg, y*u.deg, distance=10*u.Mpc) 	# dust regions
	c_clusters = SkyCoord(ra*u.deg, dec*u.deg, distance=10*u.Mpc)

	# match star clusters t0 dust regions
	cluster_match = c.search_around_sky(c_clusters, 10*u.arcsec)
	# cluster_match[0] = indices of clusters in c_clusters
	# cluster_match[1] = indices of dust regions in c
	# cluster_match[2] = the angular separation
	# cluster_match[3] = the physical separation

	# grab 3 closest clusters to each dust region
	idx_min = []
	for i in np.unique(cluster_match[1]):
		w = np.where(cluster_match[1] == i)[0]
		mi = cluster_match[2][w].argsort()[:3]
		idx_min.append(cluster_match[0][w][mi])


	idx_min = np.array(idx_min) #--> indices of clusters in c_clusters that are the 3 closest to each dust region

	ra  = ra[idx_min]
	dec = dec[idx_min]
	age = age[idx_min]
	mass = mass[idx_min]
	excess = excess[idx_min]

	return c, c_clusters[idx_min], age, mass, excess

