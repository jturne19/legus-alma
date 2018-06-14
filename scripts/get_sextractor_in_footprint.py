"""
"""
import numpy as np 
from astropy.io import fits

def in_footprint(cat, pbcoverage):
	"""
	function that takes a sextractor cat file and pulls out the sources that lie within
	the 80% of the given pbcoverage map

	cat:			string; name of the catalog
	pbcoverage: 	string; name of the pbcoverage fits file

	"""

	hdul = fits.open(pbcoverage)
	hdu = hdul[0]
	data = hdu.data[0][0]

	# get rid of nans by changing them to zero
	data[np.isnan(data)] = 0 

	# read in the pixel coordinates of all the sources in the full sextractor catalog
	x, y = np.loadtxt(cat, usecols=[8,9], unpack=True)
	# need to round the coordinates to nearest integer and then convert to ints
	x = np.array([int(round(num, 0)) for num in x ])
	y = np.array([int(round(num, 0)) for num in y ])

	# now read in the entire line of each source for easy output
	sex = np.loadtxt(cat)

	# loop through all the coordinates in x and y to check if that point is greater than .8 in the pbcoverage
	# then save that index position in the array coord_index_footprint
	coord_index_footprint = np.array([ i for i in range(len(x)) if data[y[i]][x[i]] > 0.8 ])

	# save the sextractor results for the regions found to be in the 80% footprint
	header = " #   1 NUMBER                 Running object number                                     \n#   2 FLUX_APER              Flux vector within fixed circular aperture(s)              [count]\n#   3 FLUXERR_APER           RMS error vector for aperture flux(es)                     [count]\n#   4 FLUX_AUTO              Flux within a Kron-like elliptical aperture                [count]\n#   5 FLUXERR_AUTO           RMS error for AUTO flux                                    [count]\n#   6 KRON_RADIUS            Kron apertures in units of A or B                         \n#   7 BACKGROUND             Background at centroid position                            [count]\n#   8 FLUX_MAX               Peak flux above background                                 [count]\n#   9 X_IMAGE                Object position along x                                    [pixel]\n#  10 Y_IMAGE                Object position along y                                    [pixel]\n#  11 X_WORLD                Barycenter position along world x axis                     [deg]\n#  12 Y_WORLD                Barycenter position along world y axis                     [deg]\n#  13 X2_IMAGE               Variance along x                                           [pixel**2]\n#  14 Y2_IMAGE               Variance along y                                           [pixel**2]\n#  15 XY_IMAGE               Covariance between x and y                                 [pixel**2]\n#  16 CXX_IMAGE              Cxx object ellipse parameter                               [pixel**(-2)]\n#  17 CYY_IMAGE              Cyy object ellipse parameter                               [pixel**(-2)]\n#  18 CXY_IMAGE              Cxy object ellipse parameter                               [pixel**(-2)]\n#  19 A_IMAGE                Profile RMS along major axis                               [pixel]\n#  20 B_IMAGE                Profile RMS along minor axis                               [pixel]\n#  21 THETA_IMAGE            Position angle (CCW/x)                                     [deg]\n#  22 ELONGATION             A_IMAGE/B_IMAGE                                           \n#  23 ELLIPTICITY            1 - B_IMAGE/A_IMAGE                                       \n#  24 FWHM_IMAGE             FWHM assuming a gaussian core                              [pixel]\n#  25 FLAGS                  Extraction flags                                          "
	np.savetxt(cat.replace('.cat', '.in_footprint.cat'), sex[coord_index_footprint], header=header, comments='')