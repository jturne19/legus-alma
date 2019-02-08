"""
"""
import numpy as np
import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord, search_around_sky
import astropy.units as u

def overlap(b4_reg, b7_reg, sep):
	""" 
	function to find ds9 ellipse regions that match or overlap between band 4 and band 7

	"""
	# define some other little functions
	def match_function(c, c_array, sep):
		""" c would be a single band 4 dust region
			c_array would be array of the band 7 regions
		"""
		# find where in the c_array has a separation less the input sep for a given dust region c
		s = c.separation(c_array)
		w = np.where(s < sep)[0]
		if len(w) > 0:
			i = np.argmin(s)
			return c, c_array[i]

	def make_ds9_region(ra, dec, a, b, pa, filename, color):
		f = open(filename, 'w')
		f.write('# Region file format: DS9 version 4.1\n')
		f.write('global color=%s dashlist=8 3 width=1 font="helvetica 10 normal roman" select=1 highlite=1 dash=0 fixed=0 edit=1 move=1 delete=1 include=1 source=1\n'%color)
		f.write('fk5\n')
		for r,d,at,bt,pat in zip(ra, dec, a, b, pa):
			f.write('ellipse(%1.6f,%1.6f,%1.2f",%1.2f",%1.6e)\n'%(r,d,at,bt,pat) )
		f.close()

	# read in ds9 degree region files
	xstr4, ystr4 = np.loadtxt(b4_reg, skiprows=3, usecols=[0,1], dtype='str', delimiter=',', unpack=True)
	xstr7, ystr7 = np.loadtxt(b7_reg, skiprows=3, usecols=[0,1], dtype='str', delimiter=',', unpack=True)

	# get rid of 'ellipse(' and convert to float
	x4 = np.array([ float(s[8:]) for s in xstr4])
	y4 = np.array([ float(s) for s in ystr4])
	x7 = np.array([ float(s[8:]) for s in xstr7])
	y7 = np.array([ float(s) for s in ystr7])

	# take x and y coordinates to make astropy skycoords for them. distance to ngc0628 is 10 Mpc or 1e7 pc
	c4 = SkyCoord(x4*u.deg, y4*u.deg, distance=10*u.Mpc)
	c7 = SkyCoord(x7*u.deg, y7*u.deg, distance=10*u.Mpc)

	# set max separation b/w regions (2 x beam size?)
	# sep = 2.2*u.arcsec
	sep = sep*u.arcsec
	coord_match = np.array([ match_function(c, c7, sep.to(u.degree)) for c in c4 ])

	# get rid of Nones
	coord_match = coord_match[np.not_equal(coord_match, None)]

	# separate out into ra and dec arrays
	ra4 = np.array([c[0].ra.deg for c in coord_match])
	dec4 = np.array([c[0].dec.deg for c in coord_match])
	ra7 = np.array([c[1].ra.deg for c in coord_match])
	dec7 = np.array([c[1].dec.deg for c in coord_match])
	
	# since i did the separation of c4 from c7, unique c4's can share the same c7...
	# so, we do the separation of c7 from c4 to find opposite
	# using only the matched ones found just above
	
	c4 = SkyCoord(ra4*u.deg, dec4*u.deg, distance=10*u.Mpc)
	c7 = SkyCoord(ra7*u.deg, dec7*u.deg, distance=10*u.Mpc)
	
	coord_match = np.array([match_function(c, c4, sep.to(u.degree)) for c in c7])

	# separate out into ra and dec arrays
	ra4 = np.array([c[1].ra.deg for c in coord_match])
	dec4 = np.array([c[1].dec.deg for c in coord_match])
	ra7 = np.array([c[0].ra.deg for c in coord_match])
	dec7 = np.array([c[0].dec.deg for c in coord_match])
	
	# now need to grab the flux from sextractor for these regions!
	
	# read in sextractor business just for band 4 for now
	flux, flux_err, kron, background, x_world, y_world, a_image, b_image, pa = np.loadtxt(b4_reg.replace('.deg.reg', '.cat'), usecols=[3,4,5,6,10,11,18,19,20], unpack=True)
	coords_all = SkyCoord(x_world*u.deg, y_world*u.deg)

	c4 = SkyCoord(ra4*u.deg, dec4*u.deg)

	m0, m1, m2, m3 = coords_all.search_around_sky(c4,0.1*u.arcsec)

	flux = flux[m1]
	flux_err = flux_err[m1]
	kron = kron[m1]
	background = background[m1]
	x_world = x_world[m1]
	y_world = y_world[m1]
	a_image = a_image[m1]
	b_image = b_image[m1]
	pa = pa[m1]

	header = 'flux \t flux_err \t kron \t background \t RA \t DEC \t A_image \t b_image \t PA'
	np.savetxt('band4.overlap.cat', np.transpose([flux, flux_err, kron, background, x_world, y_world, a_image, b_image, pa]), header=header)
	
	# convert a_image and b_image to arcsecs
	pixsize = 0.06	# arcsec/pixel
	a_arcsec = kron*a_image*pixsize
	b_arcsec = kron*b_image*pixsize

	make_ds9_region(x_world, y_world, a_arcsec, b_arcsec, pa, 'band4.overlap.deg.reg', 'magenta')

	# now same for band 7 

	flux, flux_err, kron, background, x_world, y_world, a_image, b_image, pa = np.loadtxt(b7_reg.replace('.deg.reg', '.cat'), skiprows=25, usecols=[3,4,5,6,10,11,18,19,20], unpack=True)
	coords_all = SkyCoord(x_world*u.deg, y_world*u.deg)
	
	c7 = SkyCoord(ra7*u.deg, dec7*u.deg)
	
	# find the indices of the 4 arcsec matched dust clumps in this big list of all the dust clumps
	m0, m1, m2, m3 = coords_all.search_around_sky(c7,0.1*u.arcsec)
	
	flux = flux[m1]
	flux_err = flux_err[m1]
	kron = kron[m1]
	background = background[m1]
	x_world = x_world[m1]
	y_world = y_world[m1]
	a_image = a_image[m1]
	b_image = b_image[m1]
	pa = pa[m1]
	
	header = 'flux \t flux_err \t background \t RA \t DEC \t A_image \t b_image \t PA'
	np.savetxt('band7.overlap.cat', np.transpose([flux, flux_err, kron, background, x_world, y_world, a_image, b_image, pa]), header=header)
	
	# convert a_image and b_image to arcsecs
	a_arcsec = kron*a_image*pixsize
	b_arcsec = kron*b_image*pixsize
	
	make_ds9_region(x_world, y_world, a_arcsec, b_arcsec, pa, 'band7.overlap.deg.reg', 'cyan')
	