"""
big 'ole python script that (hopefully) goes through the entire science procedure for give band 4 and band 7 fits files

notes are given in science.md

"""
import numpy as np
import matplotlib.pyplot as plt
import astropy
from astropy.io import fits
import os, sys, subprocess

# add scripts directory to the path
sys.path.insert(0, '/uwpa2/turner/legus-alma/scripts/')
from ds9_regions_from_sextractor import get_regions
from get_sextractor_in_footprint import in_footprint


# define the band 4 and band 7 fits files to use
b4_fits = 'band4.fits'
b7_fits = 'band7.fits'
# define the other fits files needed
b4_pbcoverage = 'band4.pbcoverage.fits'
b7_pbcoverage = 'band7.pbcoverage.fits'


# read in band 4 header and data 
b4_hdulist = fits.open(b4_fits)
b4_hdu = b4_hdulist[0]
b4_header = b4_hdu.header
b4_data = b4_hdu.data

b4_bmaj = b4_header['bmaj'] * 3600.0 	# restoring beam major axis in arcsec
b4_bmin = b4_header['bmin'] * 3600.0 	# restoring beam minor axis in arcsec


# read in band 7 header and data
b7_hdulist = fits.open(b7_fits)
b7_hdu = b7_hdulist[0]
b7_header = b7_hdu.header
b7_data = b7_hdu.data

b7_bmaj = b7_header['bmaj'] * 3600.0 	# restoring beam major axis in arcsec
b7_bmin = b7_header['bmin'] * 3600.0 	# restoring beam minor axis in arcsec

# use sextractor to extract the dust regions
# need to run sextractor from physics network computer like uwpa
b4_sexcmd = 'sex ../%s -c config.sex -catalog_name band4.cat -detect_thresh 1.5 -analysis_thresh 1.5 -seeing_FWHM %1.2f -pixel_scale 0.06 -back_type manual -back_value 0.0'%(b4_fits, b4_bmaj)
b7_sexcmd = 'sex ../%s -c config.sex -catalog_name band7.cat -detect_thresh 1.0 -analysis_thresh 1.0 -seeing_FWHM %1.2f -pixel_scale 0.06 -back_type manual -back_value 0.0'%(b7_fits, b7_bmaj)

# need to run sextractor from extract directory with the config files and default params things
os.chdir('extract')

# run sextractor commands
try:
	subprocess.call(b4_sexcmd.split())
	subprocess.call(b7_sexcmd.split())
except OSError as e:
	print(e)

# make new .cats that only have regions that lie within the 80% pbcoverage
in_footprint('band4.cat', '../'+b4_pbcoverage)
in_footprint('band7.cat', '../'+b7_pbcoverage)

# next step is to make ds9 regions out of the sextractor .cat
get_regions('band4.in_footprint.cat')
get_regions('band7.in_footprint.cat')
# outputs band4.reg and band7.reg

# need to open band4.in_footprint.reg and band7.in_footprint.reg in ds9 and save as degree region files

