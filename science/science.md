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


### feather band 7 12m + 7m images
to test flux recovery, going to feather the 7m ACA low resolution image with the 12m INT high resolution images

in casa 5.3.0:
```python
# first need to convert FITS files to CASA images using importfits
importfits('12m.pbcor.fits','12m.pbcor.image')
importfits('7m.pbcor.fits', '7m.pbcor.image')

# now feathering
feather('band7.feather.image', '12m.pbcor.image', '7m.pbcor.image')
# check
viewer('band7.feather.image')
# export to FITS
exportfits('band7.feather.image', 'band7.feather.fits')

```



### global photometry
first made a circular region that fit in both band 4 and band 7 images without getting any primary beam edge effects. saved this region in degrees as global.deg.reg
next opened that region in band 4, band 7, PACS, and SPIRE images and saved the region as 'image' for each of them.
need to delete the extra stuff that ds9 puts in the region files
now to do photometry:
```bash
cd /uwpa2/turner/legus-alma/science/
./imcnts.sh

# need to get errors
idl
.r fitsky_ds9.pro 
fitsky_ds9

```
this will do the global photometery on the herschel images
for the alma images, first need to take the fits files and make then 2 dimensional otherwise imcnts doesn't know what to do
```python
from astropy.io import fits
hdul = fits.open('band7.feather.fits')
hdu = hdul[0]
hdu.data = hdu.data[0][0]
hdu.writeto('global/band7.feather.2D.fits')

```

iraf was being stupid so i had to copy over and do them on another computer
```bash
ssh turner@zulu
cp -r /d/uwpa2/turner/legus-alma/science/global ~/tmp/

xgterm -sb &
cd ~/iraf/
cl 
cd /d/users/turner/tmp/global/
xray
xspatial
imcnts band4.2D global.band4.pix "" global.band4.sky.pix band4.tab
imcnts band7.2D global.band7.pix "" global.band7.sky.pix band7.tab
cp *tab /d/uwpa2/turner/legus-alma/science/global

ls *tab > tables.list

task gettables = gettables.cl
gettables @tables.list

cp b*tab /d/uwpa2/turner/legus-alma/science/global/
cp tables* /d/uwpa2/turner/legus-alma/science/global/

```
### modified blackbody fit to the global photometry

want to take our so-called 'global' photometry in the herschel images and fit a modified blackbody to them. uses modBBfit.py

### sextractor 

in extract directory, there is config.sex and config.sex
this is the configuration file needed for running sextractor
parameters needed for specific band 4 and band 7 are in the command used to run sextractor

