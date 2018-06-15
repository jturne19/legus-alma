# script / workflow for the 'science' 

## procedure outline:

1. create 'global' region common to both band 4 and band 7 images
2. use this region to perform global photometery on band 4, band 7, and herschel images
	- submm excess?

3. use sextractor to find dust regions of >5 contiguous pixels with >3 sigma over RMS
4. pick out regions that lie within the 80% pbcoverage area
5. match dust regions across multiple bands (3,4,6,7) 
	- can also use Halpha contours?

6. measure continuum slope for these 'verified' regions
7. match dust regions with their nearest neighbor stellar clusters
8. any correlation between continuum slope and stellar cluster properties?


### global photometry
first made a circular region that fit in both band 4 and band 7 images without getting any primary beam edge effects. saved this region in degrees as global.deg.reg
next opened that region in band 4, band 7, PACS, and SPIRE images and saved the region as 'image' for each of them.
need to delete the extra stuff that ds9 puts in the region files
now to do photometry:
```bash
export PATH=/usr/local/Anaconda/bin:$PATH
source activate iraf27
cd /uwpa2/turner/legus-alma/science
pyraf

cd
xray
xspatial

cd herschel
imcnts 'NGC0628_S500_110_SSS_111_PACSS_70'  'global.070.pix' "" 'NGC0628.pix070.0.sky' 'ngc0628.070.0.tab'
imcnts 'NGC0628_S500_110_SSS_111_PACSS_100' 'global.100.pix' "" 'NGC0628.pix100.0.sky' 'ngc0628.100.0.tab'
imcnts 'NGC0628_S500_110_SSS_111_PACSS_160' 'global.160.pix' "" 'NGC0628.pix160.0.sky' 'ngc0628.160.0.tab'
imcnts 'NGC0628_S500_110_SSS_111_SPIRE_250' 'global.250.pix' "" 'NGC0628.pix250.0.sky' 'ngc0628.250.0.tab'
imcnts 'NGC0628_S500_110_SSS_111_SPIRE_350' 'global.350.pix' "" 'NGC0628.pix350.0.sky' 'ngc0628.350.0.tab'
imcnts 'NGC0628_S500_110_SSS_111_SPIRE_500' 'global.500.pix' "" 'NGC0628.pix500.0.sky' 'ngc0628.500.0.tab'

# put all tabs into a list
ls ngc0628*tab > tables.list

# convert tabs to ascii
task gettables = gettables.cl
gettables @tables.list
# copy the output over to the science direcotry
cp tables.asc ../phot.herschel.asc

cd ..
# requires the 2 diminsional fits files...
from astropy.io import fits
hdul = fits.open('band4.fits')
hdu = hdul[0]
hdu.data = hdu.data[0][0]
hdu.writeto('band4.2D.fits')

hdul = fits.open('band7.fits')
hdu = hdul[0]
hdu.data = hdu.data[0][0]
hdu.writeto('band7.2D.fits')



```




### sextractor 

in extract directory, there is config.sex and config.sex
this is the configuration file needed for running sextractor
parameters needed for specific band 4 and band 7 are in the command used to run sextractor

