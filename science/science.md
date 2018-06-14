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


### sextractor 

in extract directory, there is config.sex and config.sex
this is the configuration file needed for running sextractor
parameters needed for specific band 4 and band 7 are in the command used to run sextractor

