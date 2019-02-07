# script / workflow

re-downloaded raw data from ALMA science archive

extracted all tar files

simplified the file structure since the default ALMA directories are numerous and not descriptive

## prep for imaging

reproduce the pipeline calibrated.ms --> this will create the 'calibrated' directory which will be needed for imaging

need to use casa version 4.7.0-1 (r38335) because that's what was orginally used

```bash
cd script
casa-release-4.7.0-1-el7/bin/casa --pipeline

# to run in parallel using mpi
casa-release-4.7.0-1-el7/bin/mpicasa -n N casa-release-4.7.0-1-el7/bin/casa  --pipeline
# where N is the number of cores you want to use on the machine

```
```python
execfile('scriptForPI.py')
# takes a few hours
```

copy or move over the newly created calibrated/uid*split.cal over to imaging directory and start casa there

```python
execfile('../../../image_prep.py')

# selected parts from image.py
finalvis='calibrated_final.ms'
contspws = '0,1,2,3'	# check output calibrated_final.ms.listobs.txt!

flagmanager(vis=finalvis,mode='save',
			versionname='before_cont_flags')
initweights(vis=finalvis,wtmode='weight',dowtsp=True)

contvis='calibrated_final_cont.ms'
rmtables(contvis)
os.system('rm -rf ' + contvis + '.flagversions')

# band 4 width=[8,8,8,8]
# band 7 width=[16,16,16,16]

width=[16,16,16,16]

split2(vis=finalvis,
	   spw=contspws,      
	   outputvis=contvis,
	   width=width, 
	   datacolumn='data')

# check the weights

# get antenna from weblog -> click any *target.ms -> antenna setup -> polar plot -> antenna in middle
# get field from weblog ---> click any *target.ms -> spatial setup -> plot under mosiac pointings -> field in middle 
# 12m band 4 -- antenna='DA49', field='15'
# 7m band 7 --- antenna='CM05', field='26'
# 12m band 7 -- antenna='DA59', field='71'

antenna = 'DA49'
field = '15'
plotms(vis=contvis, yaxis='wtsp',xaxis='freq',spw='',antenna=antenna,field=field ) 

# inspect continuum for any problems
plotms(vis=contvis,xaxis='uvdist',yaxis='amp',coloraxis='spw')
```
## imaging for band 4 12m

```python
"""
tclean parameters:

field: 			mosiac so set to 'NGC_628' to use all fields in the mosiac
imagermode:		'mosiac' because this is a mosiac
phasecenter:	field in the center of the image
cell: 			cell size - essentially pixels across the beam
imsize:			final image size in pixels
outframe:		velocity frame to output. barycentric is fine
veltype: 		velocity type - documentation recommends to keep as 'radio'
weighting: 		weighting for combining interferometric data
robust: 		changes resolution/sensitivity: smaller number (negative) - higher ang resolution, lower sensitivity. bigger number - lower ang resolution, greater sensitiviy (for more extended things)
interactive: 	interactive masking or not
niter: 			max number of iterations for cleaning
threshold: 		threshold for stopping the cleaning cycles
scales: 		scales for the multiscale cleaning
mask:			apply a previously saved mask or not
imagename: 		the final image name 

for getting phasecenter, cell size, and image size, we can use analysisUtils
to get analysisUtils:
download tar from website: https://casaguides.nrao.edu/index.php/Analysis_Utilities
extract and put wherever
in casa:
import sys
sys.path.append('path/to/analysis_scripts')
import analysisUtils as au

au.pickCellSize(contvis, imsize=True)

this will output something like (0.8, [180,180], 27) where
0.8 --> recommended cell size in arcsec (does not take into account projected baselines so may want to use slightly lower cell size)
[180,180] --> image size in pixels. for mosiacs, want to go bigger to pad the sides to make sure you get extended emissions
27 --> field closest to center of the image

can also get cell size by first getting longest baseline in wavelengths:
plotms(vis=contvis, xaxis='uvwave', yaxis='amp')
# estimate beam size --> 206265.0/(longest baseline in wavelengths)
# divide beam size by 5-8 --> better to have slightly too many cells per beam than too few
"""
# don't necessarily need pipeline version of casa for imaging
contvis = 'calibrated_final_cont.ms'
clearcal(vis=contvis)
delmod(vis=contvis)

field = 'NGC_628'
imagermode = 'mosaic'
phasecenter = 15
cell = '0.06arcsec'
imsize = [2500,2500]
outframe = 'bary'
veltype = 'radio'
weighting = 'briggs'

robust = 2.0
interactive = True
niter = 1000
threshold = '0.0mJy'

uvtaper = True
outertaper = '1arcsec'

contimagename = '12mband4_robust+2_uvtaper1arcsec_multiscale_hogbom'

tclean(vis=contvis,
     imagename=contimagename,
     field=field,
     phasecenter=phasecenter,
     mode='mfs',
     psfmode='clark',
     imsize = imsize, 
     cell= cell, 
     weighting = weighting, 
     robust = robust,
     niter = niter, 
     threshold = threshold, 
     interactive = interactive,
     imagermode = imagermode,
     uvtaper = uvtaper,
     outertaper = outertaper)

# interactive cleaning
# drew regions around areas with 3 sigma above background
# background rms ~ 1e-5 
# picked out regions with peaks > 3e-5 

# once done with that, can save the masked used interactively with
contmaskname = 'cont.mask'
rmtables(contmaskname) # if you want to delete the old mask
os.system('cp -ir ' + contimagename + '.mask ' + contmaskname)
# then when running tclean again, you can call
mask = contmaskname
# and probably want to do
interactive = False

```

## imaging for band 7 7m

```python

contvis = 'calibrated_final_cont.ms'
clearcal(vis=contvis)
delmod(vis=contvis)

field = 'NGC_628'
imagermode = 'mosaic'
phasecenter = 27

cell = '0.5arcsec'
imsize = [300,300]

outframe = 'bary'
veltype = 'radio'
weighting = 'briggs'

robust = -0.5
interactive = True
niter = 1000
threshold = '0.0mJy'

contimagename = '7mband7_robust-0.5_multiscale_hogbom'

clean(vis=contvis,
     imagename=contimagename,
     field=field,
     phasecenter=phasecenter,
     mode='mfs',
     psfmode='clark',
     imsize = imsize, 
     cell= cell, 
     weighting = weighting, 
     robust = robust,
     niter = niter, 
     threshold = threshold, 
     interactive = interactive,
     imagermode = imagermode)

```

## imaging for band 7 12m

```python
contvis = 'calibrated_final_cont.ms'
clearcal(vis=contvis)
delmod(vis=contvis)

field = 'NGC_628'
imagermode = 'mosaic'
phasecenter = 71
cell = '0.06arcsec'
imsize = [2500,2500]
outframe = 'bary'
veltype = 'radio'
weighting = 'briggs'

robust = 2.0
interactive = True
niter = 1000
threshold = '0.0mJy'

uvtaper = True
outertaper = '1.2arcsec'

contimagename = '12m_band7_robust+2_uvtaper1.2_masked'

clean(vis=contvis,
     imagename=contimagename,
     field=field,
     phasecenter=phasecenter,
     mode='mfs',
     psfmode='clark',
     imsize = imsize, 
     cell= cell, 
     weighting = weighting, 
     robust = robust,
     niter = niter, 
     threshold = threshold, 
     interactive = interactive,
     imagermode = imagermode,
     uvtaper = uvtaper,
     outertaper = outertaper)

# interactive cleaning
# drew regions around areas with 3 sigma above background
# background rms ~ 1e-5 
# picked out regions with peaks > 3e-5 

# once done with that, can save the masked used interactively with
contmaskname = 'cont.mask'
rmtables(contmaskname) # if you want to delete the old mask
os.system('cp -ir ' + contimagename + '.mask ' + contmaskname)
# then when running tclean again, you can call
mask = contmaskname
# and probably want to do
interactive = False

```

### export to fits


# Observations:

| Band | Freq (GHz) | Wavelength (mm) | Dish | #Execs | FOV     | Beam Size (arcsec) | RMS (Jy/beam) |
|------|------------|-----------------|------|--------|---------|--------------------|---------------|
| 4    | 145        | 2.1             | 12M  | 2/2    | 2' x 2' | 1.12 x 1.08        | 1e-5          |
| 7    | 343        | 0.87            | 12m  | 7/7    | 2' x 2' | 0.94 x 0.88        | 2e-5          |
| 7    | 343        | 0.87            | 7m   | 9/9    | 2' x 2' | 4.73 x 2.70        | 2e-4          |
| 7    | 343        | 0.87            | 7m+12m (feather)        | 1.11 x 1.04        | |



# Rerun imaging using Ilsang's tclean parameters

## band 4 12m 

```python
# CASA 5.4.0-68

contvis = 'calibrated_final_cont.ms'
clearcal(vis=contvis)
delmod(vis=contvis)

field = 'NGC_628'
imagermode = 'mosaic'
phasecenter = 15
cell = '0.06arcsec'
imsize = [2500,2500]
outframe = 'bary'
veltype = 'radio'
weighting = 'briggs'

robust = 2.0
interactive = True
niter = 1000
threshold = '0.0mJy'

uvtaper = ['1arcsec']

contimagename = '12mband4.ilsang'

tclean(vis=contvis,
     imagename=contimagename,
     field=field,
     phasecenter=phasecenter,
     specmode='mfs',
     deconvolver='mtmfs',
     nterms=2,
     gridder='mosaic',
     imsize = imsize, 
     cell= cell, 
     weighting = weighting, 
     robust = robust,
     niter = niter, 
     threshold = threshold, 
     interactive = interactive,
     uvtaper = uvtaper)

# save mask
contmaskname = 'cont.mask'
rmtables(contmaskname) # if you want to delete the old mask
os.system('cp -ir ' + contimagename + '.mask ' + contmaskname)

# create primary beam corrected image 
impbcor(imagename=contimagename+'.image.tt0',
     pbimage=contimagename+'.pb.tt0',
     outfile=contimagename+'.image.pbcor.tt0')

# export image, pbcor, and pb to fits files
exportfits(imagename=contimagename+'.image.tt0',
     fitsimage=contimagename+'.fits',
     dropdeg=True)

exportfits(imagename=contimagename+'.image.pbcor.tt0',
     fitsimage=contimagename+'.pbcor.fits',
     dropdeg=True)

exportfits(imagename=contimagename+'.pb.tt0',
     fitsimage=contimagename+'.pb.fits',
     dropdeg=True)

```
## band 7 7m

```python
# CASA 5.4.0-68

# this observation is from Cycle 4 so it is affected by the flux calibration issues reported by the ALMA and CASA people
# important to do this in the newest version of CASA 

contvis = 'calibrated_final_cont.ms'
clearcal(vis=contvis)
delmod(vis=contvis)

field = 'NGC_628'
imagermode = 'mosaic'
phasecenter = 27

cell = '0.5arcsec'
imsize = [300,300]

outframe = 'bary'
veltype = 'radio'
weighting = 'briggs'

robust = -0.5
interactive = True
niter = 1000
threshold = '0.0mJy'

contimagename = '7mband7.ilsang'

tclean(vis=contvis,
     imagename=contimagename,
     field=field,
     phasecenter=phasecenter,
     specmode='mfs',
     deconvolver='mtmfs',
     nterms=2,
     gridder='mosaic',
     imsize = imsize, 
     cell= cell, 
     weighting = weighting, 
     robust = robust,
     niter = niter, 
     threshold = threshold, 
     interactive = interactive)

# save mask
contmaskname = 'cont.mask'
rmtables(contmaskname) # if you want to delete the old mask
os.system('cp -ir ' + contimagename + '.mask ' + contmaskname)

# create primary beam corrected image
impbcor(imagename=contimagename+'.image.tt0',
     pbimage=contimagename+'.pb.tt0',
     outfile=contimagename+'.image.pbcor.tt0')

# export image, pbcor, and pb to fits files
exportfits(imagename=contimagename+'.image.tt0',
     fitsimage=contimagename+'.fits',
     dropdeg=True)

exportfits(imagename=contimagename+'.image.pbcor.tt0',
     fitsimage=contimagename+'.pbcor.fits',
     dropdeg=True)

exportfits(imagename=contimagename+'.pb.tt0',
     fitsimage=contimagename+'.pb.fits',
     dropdeg=True)

```

## band 7 12m 

```python
# CASA 5.4.0-68

contvis = 'calibrated_final_cont.ms'
clearcal(vis=contvis)
delmod(vis=contvis)

field = 'NGC_628'
imagermode = 'mosaic'
phasecenter = 71
cell = '0.06arcsec'
imsize = [2500,2500]
outframe = 'bary'
veltype = 'radio'
weighting = 'briggs'

robust = 2.0
interactive = True
niter = 1000
threshold = '0.0mJy'

uvtaper = ['1.2arcsec']

contimagename = '12mband7.ilsang'

tclean(vis=contvis,
     imagename=contimagename,
     field=field,
     phasecenter=phasecenter,
     specmode='mfs',
     deconvolver='mtmfs',
     nterms=2,
     gridder='mosaic',
     imsize = imsize, 
     cell= cell, 
     weighting = weighting, 
     robust = robust,
     niter = niter, 
     threshold = threshold, 
     interactive = interactive,
     uvtaper = uvtaper)

# save mask
contmaskname = 'cont.mask'
rmtables(contmaskname) # if you want to delete the old mask
os.system('cp -ir ' + contimagename + '.mask ' + contmaskname)

# create primary beam corrected image
impbcor(imagename=contimagename+'.image.tt0',
     pbimage=contimagename+'.pb.tt0',
     outfile=contimagename+'.image.pbcor.tt0')

# export image, pbcor, and pb to fits files
exportfits(imagename=contimagename+'.image.tt0',
     fitsimage=contimagename+'.fits',
     dropdeg=True)

exportfits(imagename=contimagename+'.image.pbcor.tt0',
     fitsimage=contimagename+'.pbcor.fits',
     dropdeg=True)

exportfits(imagename=contimagename+'.pb.tt0',
     fitsimage=contimagename+'.pb.fits',
     dropdeg=True)

# output the 'dirty' image by calling tclean with 0 iterations
interactive = False
niter = 0
contimagename = '12mband7.ilsang.dirty'

tclean(vis=contvis,
     imagename=contimagename,
     field=field,
     phasecenter=phasecenter,
     specmode='mfs',
     deconvolver='mtmfs',
     nterms=2,
     gridder='mosaic',
     imsize = imsize, 
     cell= cell, 
     weighting = weighting, 
     robust = robust,
     niter = niter, 
     threshold = threshold, 
     interactive = interactive,
     uvtaper = uvtaper)

```

## feather band 7 images

copied over the image, pbcor, and pb images to the ilsang directory

played around with the low resolution scaling using casafeather (called from bash shell)

scaling factors to try:
     - 1.0
     - 1.5
     - 2.5
     - 5.0

also try feather using dirty 12m image 

```python
scalefactors = [1.0, 1.5, 2.5, 5.0]

for scale in scalefactors:

     feather(imagename = 'band7.ilsang.%1.1f.feather'%scale,
          highres = '12mband7.ilsang.image.tt0',
          lowres = '7mband7.ilsang.image.tt0',
          sdfactor = scale)
     
# export fits

for scale in scalefactors:
     exportfits(imagename = 'band7.ilsang.%1.1f.feather'%scale,
          fitsimage = 'band7.ilsang.%1.1f.feather.fits'%scale,
          dropdeg = True)
```

# Observations:

| Band | Freq (GHz) | Wavelength (mm) | Dish | Image Name                | FOV     | Beam Size (arcsec) | RMS (Jy/beam) |
|------|------------|-----------------|------|---------------------------|---------|--------------------|---------------|
| 4    | 145        | 2.1             | 12m  | 12mband4.ilsang.image.tt0 | 2' x 2' | 1.12 x 1.08        | 3.2e-5        |
| 7    | 343        | 0.87            | 12m  | 12mband7.ilsang.image.tt0 | 2' x 2' | 1.12 x 1.04        | 2.3e-4        |
| 7    | 343        | 0.87            | 7m   |  7mband7.ilsang.image.tt0 | 2' x 2' | 4.78 x 2.73        | 8.8e-4        |

## Primary Beam Corrected Images

| Band | Freq (GHz) | Wavelength (mm) | Dish | Image Name                      | RMS (Jy/beam) |
|------|------------|-----------------|------|---------------------------------|---------------|
| 4    | 145        | 2.1             | 12m  | 12mband4.ilsang.image.pbcor.tt0 | 6.76e-5       |
| 7    | 343        | 0.87            | 12m  | 12mband7.ilsang.image.pbcor.tt0 | 3.77e-4       |
| 7    | 343        | 0.87            | 7m   |  7mband7.ilsang.image.pbcor.tt0 | 1.75e-3       |
