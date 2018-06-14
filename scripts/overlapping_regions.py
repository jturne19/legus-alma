"""
"""
import numpy as np
import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord, search_around_sky
import astropy.units as u

def overlap(b4):

# def match_function(c, c_array, sep):
# 	""" c would be a single band 4 dust region
# 		c_array would be array of the band 7 regions
# 	"""
# 	# find where in the c_array has a separation less the input sep for a given dust region c
# 	s = c.separation(c_array)
# 	w = np.where(s < sep)[0]
# 	if len(w) > 0:
# 		i = np.argmin(s)
# 		return c, c_array[i]

# def make_ds9_region(ra, dec, a, b, pa, filename, color):
# 	f = open('overlap/%s'%filename, 'w')
# 	f.write('# Region file format: DS9 version 4.1\n')
# 	f.write('global color=%s dashlist=8 3 width=1 font="helvetica 10 normal roman" select=1 highlite=1 dash=0 fixed=0 edit=1 move=1 delete=1 include=1 source=1\n'%color)
# 	f.write('fk5\n')
# 	for r,d,at,bt,pat in zip(ra, dec, a, b, pa):
# 		f.write('ellipse(%1.6f,%1.6f,%1.2f",%1.2f",%1.6e)\n'%(r,d,at,bt,pat) )
# 	f.close()


# # read in the ALMA dust regions that lie within the footprint
# # want the degree region files for these
# xstr4, ystr4 = np.loadtxt('12mband4.footprint.deg.reg', skiprows=3, usecols=[0,1], dtype='str', delimiter=',', unpack=True)
# xstr7, ystr7 = np.loadtxt('12mband7.footprint.deg.reg', skiprows=3, usecols=[0,1], dtype='str', delimiter=',', unpack=True)

# # get rid of 'ellipse(' and convert to float
# x4 = np.array([ float(s[8:]) for s in xstr4])
# y4 = np.array([ float(s) for s in ystr4])
# x7 = np.array([ float(s[8:]) for s in xstr7])
# y7 = np.array([ float(s) for s in ystr7])

# # take x and y coordinates to make astropy skycoords for them. distance to ngc0628 is 10 Mpc or 1e7 pc
# c4 = SkyCoord(x4*u.deg, y4*u.deg, distance=10*u.Mpc)
# c7 = SkyCoord(x7*u.deg, y7*u.deg, distance=10*u.Mpc)

# sep = 2.5*u.arcsec
# coord_match = np.array([ match_function(c, c7, sep.to(u.degree)) for c in c4 ])

# # get rid of Nones
# coord_match = coord_match[np.not_equal(coord_match, None)]

# # separate out into ra and dec arrays
# ra4 = np.array([c[0].ra.deg for c in coord_match])
# dec4 = np.array([c[0].dec.deg for c in coord_match])
# ra7 = np.array([c[1].ra.deg for c in coord_match])
# dec7 = np.array([c[1].dec.deg for c in coord_match])


# # since i did the separation of c4 from c7, unique c4's can share the same c7...
# # so, we do the separation of c7 from c4 to find opposite
# # using only the matched ones found just above

# c4 = SkyCoord(ra4*u.deg, dec4*u.deg, distance=10*u.Mpc)
# c7 = SkyCoord(ra7*u.deg, dec7*u.deg, distance=10*u.Mpc)

# coord_match = np.array([match_function(c, c4, sep.to(u.degree)) for c in c7])

# # separate out into ra and dec arrays
# ra4 = np.array([c[1].ra.deg for c in coord_match])
# dec4 = np.array([c[1].dec.deg for c in coord_match])
# ra7 = np.array([c[0].ra.deg for c in coord_match])
# dec7 = np.array([c[0].dec.deg for c in coord_match])

# # now need to grab the flux from sextractor for these regions!

# # read in sextractor business
# flux, flux_err, kron, background, x_world, y_world, a_image, b_image, pa = np.loadtxt('extract/12mband4.cat', skiprows=25, usecols=[3,4,5,6,10,11,18,19,20], unpack=True)
# coords_all = SkyCoord(x_world*u.deg, y_world*u.deg)

# c4 = SkyCoord(ra4*u.deg, dec4*u.deg)

# # find the indices of the 4 arcsec matched dust clumps in this big list of all the dust clumps
# m0, m1, m2, m3 = coords_all.search_around_sky(c4,0.1*u.arcsec)

# flux = flux[m1]
# flux_err = flux_err[m1]
# kron = kron[m1]
# background = background[m1]
# x_world = x_world[m1]
# y_world = y_world[m1]
# a_image = a_image[m1]
# b_image = b_image[m1]
# pa = pa[m1]

# header = 'flux \t flux_err \t kron \t background \t RA \t DEC \t A_image \t b_image \t PA'
# np.savetxt('overlap/12mband4.overlap.sextractor.cat', np.transpose([flux, flux_err, kron, background, x_world, y_world, a_image, b_image, pa]), header=header)

# # convert a_image and b_image to arcsecs
# pixsize = 0.06	# arcsec/pixel
# a_arcsec = kron*a_image*pixsize
# b_arcsec = kron*b_image*pixsize

# make_ds9_region(x_world, y_world, a_arcsec, b_arcsec, pa, 'overlapping.band4.deg.reg', 'magenta')

# # now same thing with band 7!

# flux, flux_err, kron, background, x_world, y_world, a_image, b_image, pa = np.loadtxt('extract/12mband7.cat', skiprows=25, usecols=[3,4,5,6,10,11,18,19,20], unpack=True)
# coords_all = SkyCoord(x_world*u.deg, y_world*u.deg)

# c7 = SkyCoord(ra7*u.deg, dec7*u.deg)

# # find the indices of the 4 arcsec matched dust clumps in this big list of all the dust clumps
# m0, m1, m2, m3 = coords_all.search_around_sky(c7,0.1*u.arcsec)

# flux = flux[m1]
# flux_err = flux_err[m1]
# kron = kron[m1]
# background = background[m1]
# x_world = x_world[m1]
# y_world = y_world[m1]
# a_image = a_image[m1]
# b_image = b_image[m1]
# pa = pa[m1]

# header = 'flux \t flux_err \t background \t RA \t DEC \t A_image \t b_image \t PA'
# np.savetxt('overlap/12mband7.overlap.sextractor.cat', np.transpose([flux, flux_err, kron, background, x_world, y_world, a_image, b_image, pa]), header=header)

# # convert a_image and b_image to arcsecs
# a_arcsec = kron*a_image*pixsize
# b_arcsec = kron*b_image*pixsize

# make_ds9_region(x_world, y_world, a_arcsec, b_arcsec, pa, 'overlapping.band7.deg.reg', 'cyan')



# """
# this uses the old match function that doesn't exactly work (returns multiple matches instead of just closest one)
# # now run that matching function for 1", 2", 3", and 4" separations
# c4_match1, c7_match1 = match_function_old(c4, c7, 1*u.arcsec)
# c4_match2, c7_match2 = match_function_old(c4, c7, 2*u.arcsec)
# c4_match3, c7_match3 = match_function_old(c4, c7, 3*u.arcsec)
# c4_match4, c7_match4 = match_function_old(c4, c7, 4*u.arcsec)

# # write all coordinates out to a text file so i don't have to rerun the match_function_old everytime
# np.savetxt('overlap/overlapping.1arcsec.txt', np.transpose([c4_match1[:,0],c4_match1[:,1],c7_match1[:,0],c7_match1[:,1]]), header='band4 1"\t\t\t\t\t\t\t\t\t\t\tband7 1"')
# np.savetxt('overlap/overlapping.2arcsec.txt', np.transpose([c4_match2[:,0],c4_match2[:,1],c7_match2[:,0],c7_match2[:,1]]), header='band4 2"\t\t\t\t\t\t\t\t\t\t\tband7 2"')
# np.savetxt('overlap/overlapping.3arcsec.txt', np.transpose([c4_match3[:,0],c4_match3[:,1],c7_match3[:,0],c7_match3[:,1]]), header='band4 3"\t\t\t\t\t\t\t\t\t\t\tband7 3"')
# np.savetxt('overlap/overlapping.4arcsec.txt', np.transpose([c4_match4[:,0],c4_match4[:,1],c7_match4[:,0],c7_match4[:,1]]), header='band4 4"\t\t\t\t\t\t\t\t\t\t\tband7 4"')
# """
# """
# !!! sizes come out to around 2.5 arcsec so i am now commenting out the below size stuff because it's not needed now

# # read in the text files so you don't have to rerun the match_function_old which takes a long time
# band4_ra1, band4_dec1, band7_ra1, band7_dec1 = np.loadtxt('overlap/overlapping.1arcsec.txt', skiprows=1, unpack=True)
# band4_ra2, band4_dec2, band7_ra2, band7_dec2 = np.loadtxt('overlap/overlapping.2arcsec.txt', skiprows=1, unpack=True)
# band4_ra3, band4_dec3, band7_ra3, band7_dec3 = np.loadtxt('overlap/overlapping.3arcsec.txt', skiprows=1, unpack=True)
# band4_ra4, band4_dec4, band7_ra4, band7_dec4 = np.loadtxt('overlap/overlapping.4arcsec.txt', skiprows=1, unpack=True)

# # use the 4 arcsec business to make histogram of the dust clump sizes

# # first, read in the sextractor results (12m band4)
# # want: kron, x_world, y_world, a_image, b_image
# kron, x_world, y_world, a_image, b_image = np.loadtxt('extract/12mband4.cat', skiprows=25, usecols=[5,10,11,18,19], unpack=True)

# # put the full sextractor list of dust clumps into astropy coordinates
# full_coords4 = SkyCoord(x_world*u.deg, y_world*u.deg)
# # put the 4 arcsec matched dust clumps into astropy coordiantes
# c4_match4 = SkyCoord(band4_ra4*u.deg, band4_dec4*u.deg)
# # find the indices of the 4 arcsec matched dust clumps in this big list of all the dust clumps
# m0, m1, m2, m3 = full_coords4.search_around_sky(c4_match4, 0.1*u.arcsec)

# # band 4 sizes
# sizes4 = kron[m1]*a_image[m1] + kron[m1]*b_image[m1]

# # pixel size of 12m band 4 image - CRPIX1 in header
# pixsize = 0.06	#arcsec/pixel
# # put sizes into arcsecs
# sizes4 = sizes4 * pixsize

# # do same thing for 12m band 7
# kron, x_world, y_world, a_image, b_image = np.loadtxt('extract/12mband7.cat', skiprows=25, usecols=[5,10,11,18,19], unpack=True)
# full_coords7 = SkyCoord(x_world*u.deg, y_world*u.deg)
# c7_match4 = SkyCoord(band7_ra4*u.deg, band7_dec4*u.deg)
# m0, m1, m2, m3 = full_coords7.search_around_sky(c7_match4, 0.1*u.arcsec)
# sizes7 = kron[m1]*a_image[m1] + kron[m1]*b_image[m1]
# sizes7 = sizes7 * pixsize

# # smush the two sizes arrays together
# sizes = np.append(sizes4, sizes7)

# # histogram
# n, bins, patches = plt.hist(sizes, bins='auto')
# w = np.argmax(n)
# print 'histogram peaks at size %1.2f'%bins[w]
# w = np.where(sizes > 5)[0]
# print 'there are %i dust clumps with size greater than 5"'%len(w)
# # plt.show()
# """



