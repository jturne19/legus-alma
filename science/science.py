"""
big 'ole python script that (hopefully) goes through the entire science procedure for give band 4 and band 7 fits files

notes are given in science.md

"""
import numpy as np
import matplotlib.pyplot as plt
import astropy
from astropy.io import fits
import os, sys, subprocess
from astropy import constants as const

# add scripts directory to the path
sys.path.insert(0, '/uwpa2/turner/legus-alma/scripts/')
from ds9_regions_from_sextractor import get_regions
from get_sextractor_in_footprint import in_footprint
from overlapping_regions import overlap
from mcmc_error_bars import mcmc_error
from nearest_cluster import nearest_cluster

"""
if starting with new band 4 and band 7 fits files, you need to:
	1. make sure to have pbcoverage files
	2. take global.deg.reg and make new pixel files for band 4 and band 7 

"""
# decide what you want:

global_phot               = False		# perform global photometry?
regions                   = False		# use sextractor to get dust regions and whatnot?
fluxes                    = False		# calculate flux in dust regions and get slopes?
create_legus_region_files = False		# create ds9 region files from legus cluster catalog? (probably not necessary since those files are already on the github repo)
closest_clusters          = True		# find closest stellar clusters to dust regions?
plot                      = False		# do some plotting?

main_dir = '/uwpa2/turner/legus-alma/'

os.chdir(main_dir + 'science')

# define the band 4 and band 7 fits files to use
b4_fits = 'band4.fits'
b7_fits = 'band7.feather.fits'
# define the other fits files needed
b4_pbcoverage = 'band4.pbcoverage.fits'
b7_pbcoverage = 'band7.pbcoverage.fits'


# defining some functions
def slope(x,y):
	"""simple function to return the slope of a log line connecting two points
	"""
	return (np.log10(y[1]) - np.log10(y[0])) / (np.log10(x[1]) - np.log10(x[0]))

def mbb_func_freq(freq, beta, T, sr_in_images):

	C3 = 2 * const.h.value / const.c.value**2
	C4 = const.h.value / const.k_B.value

	bb = C3 * (freq**(3 + beta)) / (np.exp(C4*freq/T) - 1)
	return bb * freq * sr_in_images
	

# global photometry modified blackbody fit
if global_phot:
	from modBBfit import fit

	print('\ndoing global photometry bidness \n')

	os.chdir(main_dir + 'science/herschel/')
	# first need pixel scale of the PACS and SPIRE images. units are MJy*pix/sr. we want Jy
	head = fits.open('NGC0628_S500_110_SSS_111_PACSS_70.fits')[0].header
	cd11 = head['CD1_1']	# deg/pix
	cd22 = head['CD2_2']	# deg/pix
	pix_scale_sr = (-cd11 * 3600)*(cd22*3600) / 4.255e10	# sr/pix

	# read in phot data from tables.asc
	net, num_of_pix = np.loadtxt('tables.asc', usecols=[1,2], unpack=True)
	# total number of sr in the images
	sr_in_images = pix_scale_sr * num_of_pix[0]
	# wavelengths of the hershcel images
	wavel = np.array([71.8, 103.0, 157.0, 252.0, 353.0, 511.0])*1.0e-6 	# meters
	# convert to frequencies
	freq = const.c.value/wavel 	# Hz
	# now convert flux from MJy*pix/sr to Jy
	net = net * pix_scale_sr * 1e6
	flux = net * freq 	# nu*F_nu

	# calculate error in fluxes
	sky_sigma, n_sky = np.loadtxt('sky.sigma.temp.dat', usecols=[2,3], unpack=True)
	flux_err = sky_sigma * np.sqrt(num_of_pix + num_of_pix**2/n_sky)
	cal_err = np.array([.05, .05, .05, .07, .07, .07])*flux
	flux_err = flux_err * pix_scale_sr * freq * 1e6
	flux_err = np.sqrt(flux_err**2 + cal_err**2)*1e-26

	beta, T = fit(freq, flux, flux_err, sr_in_images)

	# array of wavelengths for fitting
	wfit = np.arange(50, 1e4, 10)
	# free-free and synchrotron
	ff_flux0 = 12.319e-19
	sync_flux0 = 4.567e-19
	# alma freq
	alma_freq = np.array([1.45E+11, 3.43E+11])
	alma_wavel = const.c.value/alma_freq[0] * 1e6

	bb = mbb_func_freq(const.c.value/(wfit*1e-6), beta[0], T[0], sr_in_images)*1e-26
	ff = ff_flux0 * (alma_wavel/wfit)**.9
	sync = sync_flux0 * (alma_wavel/wfit)**.2

	flux_sum = bb + ff + sync

	# alma global phot
	anet, anum_of_pix = np.loadtxt(main_dir+'/science/global/tables.asc', usecols=[1,2], unpack=True)
	# net is in units Jy*pix/beam
	b4_hdulist = fits.open(main_dir+ 'science/'+b4_fits)
	b4_hdu = b4_hdulist[0]
	b4_header = b4_hdu.header
	b4_bmaj = b4_header['bmaj'] * 3600.0
	b4_bmin = b4_header['bmin'] * 3600.0

	b7_hdulist = fits.open(main_dir+'science/'+b7_fits)
	b7_hdu = b7_hdulist[0]
	b7_header = b7_hdu.header
	b7_bmaj = b7_header['bmaj'] * 3600.0 
	b7_bmin = b7_header['bmin'] * 3600.0 


	beams = np.array([ np.pi/4.0 *b4_bmaj * b4_bmin, np.pi/4.0 * b7_bmaj*b7_bmin])
	pixel_size = 0.06**2
	pix_per_beam = beams/pixel_size	

	alma_flux = anet * alma_freq / pix_per_beam	# Jy


	# save alma data
	np.savetxt(main_dir+'science/global/alma_global_flux.dat',np.transpose([const.c.value/alma_freq * 1e6, alma_flux*1e-26]), header='wavelength (micron) \t flux (W/m2)' )
	# save herschel data
	np.savetxt('herschel_flux.dat', np.transpose([const.c.value/freq * 1e6, flux*1e-26, flux_err]), header='wavelength (micron) \t flux (W/m2) \t 1 sigma error')
	# save bb, ff, and sync data
	np.savetxt('radiation.dat', np.transpose([wfit, bb, ff, sync, flux_sum]), header='wavelength (micron) \t BB (W/m2) \t F-F flux (W/m2) \t Synchrotron (W/m2) \t BB+FF+Sync (W/m2)')
	np.savetxt('bb_params.dat', [beta, T], header='best fit parameters for the modified blackbody fit \nbeta, +error, -error \ntemperature, +error, -error')

	# for testing how things look:
	# read in data from the things above
	wavel, bb, ff, sync, total = np.loadtxt(main_dir+'science/herschel/radiation.dat', unpack=True)
	hwavel, hflux, herr = np.loadtxt(main_dir+'science/herschel/herschel_flux.dat', unpack=True)
	awavel, aflux = np.loadtxt(main_dir + 'science/global/alma_global_flux.dat', unpack=True)

	plt.figure()
	plt.loglog(hwavel, hflux, 'ko')
	plt.loglog(awavel, aflux, 'ro')
	plt.loglog(wavel, total, 'k-')
	plt.xlabel('Wavelength (micron)')
	plt.ylabel(r'Flux (W/m$^2$)')
	plt.show()


if regions:

	print('\ndoing dust region bidness \n')

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
	b4_sexcmd = 'sex ../%s -c config.sex -catalog_name band4.cat -detect_thresh 1.0 -analysis_thresh 1.0 -seeing_FWHM %1.2f -pixel_scale 0.06 -back_type manual -back_value 0.0'%(b4_fits, b4_bmaj)
	b7_sexcmd = 'sex ../%s -c config.sex -catalog_name band7.cat -detect_thresh 1.0 -analysis_thresh 1.0 -seeing_FWHM %1.2f -pixel_scale 0.06 -back_type manual -back_value 0.0'%(b7_fits, b7_bmaj)
	
	# need to run sextractor from extract directory with the config files and default params things
	os.chdir(main_dir+'science/extract')
	
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
	# outputs band4.in_footprint.reg and band7.in_footprint.reg
	done = False
	while not done:
		check = raw_input('Did you open the in_footprint.reg files and then save them as degree region files? [y/n] ')
		if check == 'y'or check == 'yes' or check == 'Y' or check == 'Yes' or check == 'YES':
			# need to open band4.in_footprint.reg and band7.in_footprint.reg in ds9 and save as degree region files
			overlap('band4.in_footprint.deg.reg', 'band7.in_footprint.deg.reg')
			# outputs band4.overlap.deg.reg and band7.overlap.deg.reg
			done = True
		else:
			print('\nwell do it\n')

if fluxes:

	print('\ndoing flux continuum slope bidness \n')

	os.chdir(main_dir + 'science/extract')

	# grab fluxes in regions
	# need the band frequencies
	#				   band 4, band 7
	freq = np.array([1.45E+11, 3.43E+11])
	wavel = const.c.value/freq
	
	
	b4_flux, b4_fluxerr, b4_bg = np.loadtxt('band4.overlap.cat', usecols=[0,1,3], unpack=True)
	b7_flux, b7_fluxerr, b7_bg = np.loadtxt('band7.overlap.cat', usecols=[0,1,3], unpack=True)
	
	os.chdir(main_dir + 'science/')
	
	# subtract out background
	b4_flux = b4_flux - b4_bg
	b7_flux = b7_flux - b7_bg
	
	# flux from sextractor is in Jy pix/beam so need to get rid of beam business
	beams = np.array([ np.pi/4.0 *b4_bmaj * b4_bmin, np.pi/4.0 * b7_bmaj*b7_bmin])
	pixel_size = 0.06**2
	pix_per_beam = beams/pixel_size
	
	# Jy
	flux = np.array([ b4_flux*freq[0]/pix_per_beam[0], b7_flux*freq[1]/pix_per_beam[1] ])
	flux_err = np.array([ b4_fluxerr*freq[0]/pix_per_beam[0], b7_fluxerr*freq[1]/pix_per_beam[1] ])
	
	# simple calculation of slopes
	slopes = slope(freq, flux)
	
	# mcmc calculation of slopes and the standard deviations on those slopes
	err_params = np.zeros([len(flux[0]), 3])
	
	for i in range(len(flux[0])):
		y = np.array([flux[0][i], flux[1][i]])*1e-26
		err = np.array([flux_err[0][i], flux_err[1][i]])*1e-26
	
		err_params[i] = mcmc_error(slope, wavel, y, err)
	
	np.savetxt('slopes+errs.dat', err_params, header='mean slope \t std dev \t median slope')

if create_legus_region_files:

	print('\nturning legus clusters into ds9 region files \n')

	os.chdir(main_dir + 'science/legus')

	ra, dec, cl = np.loadtxt('hlsp_legus_hst_acs-wfc3_ngc628-c_multiband_v1_padagb-mwext-avgapcor.tab', usecols=[3,4,33], unpack=True)
	all_clusters = np.loadtxt('hlsp_legus_hst_acs-wfc3_ngc628-c_multiband_v1_padagb-mwext-avgapcor.tab')

	# first get rid of classes 0 and 4
	w = np.where((cl != 0) & (cl != 4))[0]
	ra = ra[w]
	dec = dec[w]

	all_clusters = all_clusters[w]

	# output these star clusters as a ds9 degree region file
	f = open('ngc628-c_clusters_class123.deg.reg', 'w')
	f.write('fk5\n')

	for i in range(len(ra)):
		f.write('point(%1.6f,%1.6f) # point=X\n'%(ra[i], dec[i]))

	f.close()

	# write out new cluster catalog file with just classes 1,2,3
	np.savetxt('ngc628-c_clusters_class123.cat', all_clusters, delimiter='\t')


if closest_clusters:

	print('\nfinding the closest stellar clusters to the dust blobs \n')

	os.chdir(main_dir + 'science')
	dustcoords, starcoords, age, mass, excess = nearest_cluster('extract/band4.overlap.deg.reg')

	# calculate angular separations
	ang_sep = np.array([ dustcoords[i].separation(starcoords[i]).arcsec for i in range(len(dustcoords))])
	# calculate physical separations in pc
 	phys_sep = np.array([ ang*10e6 / 206265 for ang in ang_sep ])

 	age_avg = np.array([ np.mean(a) for a in age ])
 	mass_avg = np.array([ np.mean(m) for m in mass ])
 	excess_avg = np.array([ np.mean(e) for e in excess])
 	phys_sep_avg = np.array([ np.mean(p) for p in phys_sep ])
 	ang_sep_avg = np.array([ np.mean(a) for a in ang_sep])

 	age_min = np.array([ np.min(a) for a in age ])
 	mass_min = np.array([ np.min(m) for m in mass ])
 	excess_min = np.array([ np.min(e) for e in excess ])
 	phys_sep_min = np.array([ np.min(p) for p in phys_sep])
 	ang_sep_min = np.array([ np.min(a) for a in ang_sep])

 	np.savetxt('closest_clusters_props.average.dat', np.transpose([ang_sep_avg, phys_sep_avg, age_avg, mass_avg, excess_avg]), header='ang sep (arsec) \t physical sep (pc) \t age (yr) \t mass (solar mass) \t E(B-V)')
	np.savetxt('closest_clusters_props.minimum.dat', np.transpose([ang_sep_min, phys_sep_min, age_min, mass_min, excess_min]), header='ang sep (arsec) \t physical sep (pc) \t age (yr) \t mass (solar mass) \t E(B-V)')

if plot:

	print('\ndoing some plotting bidness \n')

	ang_sep_avg, phys_sep_avg, age_avg, mass_avg, excess_avg = np.loadtxt('closest_clusters_props.average.dat', unpack=True)
	ang_sep_min, phys_sep_min, age_min, mass_min, excess_min = np.loadtxt('closest_clusters_props.minimum.dat', unpack=True)
	slopes = np.loadtxt('slopes+errs.dat', usecols=[0])

	plt.figure()
	plt.semilogx(age_avg, slopes, 'ro')
	# plt.loglog(age_avg, np.abs(slopes), 'ro')
	plt.xlabel('Age (years)')
	plt.ylabel('Dust Continuum Slope')
	plt.title('3 closest clusters averaged')
	plt.savefig('figs/age_avg.png')
	# plt.show()

	plt.figure()
	plt.semilogx(age_min, slopes, 'ro')
	plt.xlabel('Age (years)')
	plt.ylabel('Dust Continuum Slope')
	plt.title('closest cluster')
	plt.savefig('figs/age_min.png')
	# plt.show()

	plt.figure()
	plt.semilogx(mass_avg, slopes, 'ro')
	# plt.loglog(mass_avg, -slopes, 'ro')	
	plt.xlabel('Mass (solar masses)')
	plt.ylabel('Dust Continuum Slope')
	plt.title('3 closest clusters averaged')
	plt.savefig('figs/mass_avg.png')
	# plt.show()

	plt.figure()
	plt.semilogx(mass_min, slopes, 'ro')
	plt.xlabel('Mass (solar masses)')
	plt.ylabel('Dust Continuum Slope')
	plt.title('closest cluster')
	plt.savefig('figs/mass_min.png')
	# plt.show()

	plt.figure()
	plt.semilogx(excess_avg, slopes, 'ro')
	# plt.loglog(excess_avg, -slopes, 'ro')
	plt.xlabel('E(B-V)')
	plt.ylabel('Dust Continuum Slope')
	plt.title('3 closest clusters averaged')
	plt.savefig('figs/excess_avg.png')
	# plt.show()

	plt.figure()
	plt.semilogx(excess_min, slopes, 'ro')
	plt.xlabel('E(B-V)')
	plt.ylabel('Dust Continuum Slope')
	plt.title('closest cluster')
	plt.savefig('figs/excess_min.png')
	# plt.show()

	plt.figure()
	plt.semilogy(phys_sep_avg, age_avg, 'bo')
	plt.xlabel('Physical Separation (pc)')
	plt.ylabel('Age (yr)')
	plt.title('3 closest clusters averaged')
	plt.savefig('figs/age_sep_avg.png')

	plt.figure()
	plt.semilogy(phys_sep_min, age_min, 'bo')
	plt.xlabel('Physical Separation (pc)')
	plt.ylabel('Age (yr)')
	plt.title('closest cluster')
	plt.savefig('figs/age_sep_min.png')
