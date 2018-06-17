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
cd /uwpa2/turner/legus-alma/science/
./imcnts.sh
```
this will do the global photometery on the herschel images
for the alma images, iraf was being stupid so i had to copy over and do them on another computer
```bash
ssh turner@zulu
cp -r /d/uwpa2/turner/legus-alma/science/global ~/tmp/

xgterm -sb &
cd ~/iraf/
cl 
cd /d/users/turner/tmp/global/
xray
xspatial
imcnts band4.2D global.band4.pix 0. "" band4.tab
imcnts band7.2D global.band7.pix 0. "" band7.tab
cp *tab /d/uwpa2/turner/legus-alma/science/global

cd /d/uwpa2/turner/legus-alma/science/global/
cp ../herschel/gettables.c* ./

ls *tab > tables.list

# for some reasion this is not working for band4.tab and band7.tab
task gettables = gettables.cl
gettables @tables.list


```
### modified blackbody fit to the global photometry






### sextractor 

in extract directory, there is config.sex and config.sex
this is the configuration file needed for running sextractor
parameters needed for specific band 4 and band 7 are in the command used to run sextractor

