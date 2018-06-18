; .r /cherokee1/turner/alma/fitsky_ds9.pro
; fitsky_ds9
;;;;;;;;;;;;;;;;; Version 2 ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Computes both small-scale and large-scale sky flucutations (see Eqns 2 & 3 of
; Boselli+03 406,867).
; Requires read_circ.pro, circ_ind.pro
; The sky region files should not have any header info in them
PRO fitsky_ds9
	
openw,1,'sky.sigma.temp.dat'
readcol,'skyaps.list',f='(a,a)',imgfile,ds9file
nim=n_elements(imgfile)

for i=0, nim-1 do begin

 img=readfits(imgfile[i],hdr)
 foo=read_circ(ds9file[i],x,y,r)

 all_ind=0
 individual_sky_medians=fltarr(n_elements(x))
 ;individual_sky_stddevs=fltarr(n_elements(x))

 FOR n=0,n_elements(x)-1 DO BEGIN
  ind=circ_ind(img,x[n],y[n],r[n])
  ;print,x[n],y[n],r[n],median(img[ind]),stddev(img[ind],/nan)
  individual_sky_medians[n]=median(img[ind]) ; for the majority of images
  ;individual_sky_medians[n]=mean(img[ind]) ; for few special low-integration cases where median is zero ...
  ;individual_sky_stddevs[n]=stddev(img[ind],/nan) ; not used
  all_ind=[all_ind,ind]
 ENDFOR
 
 all_ind=all_ind[1:*]
 sky_median=median(img[all_ind])
 sky_sigma=stddev(img[all_ind],/nan)
 sigma_individual_sky_medians=stddev(individual_sky_medians,/nan)
 print,'The median and sigma for all sky aps combined:',i,sky_median,sky_sigma
 print,'The standard deviation of the median of the individual sky aps:',sigma_individual_sky_medians
 printf,1,f='(a46,1x,f12.6,1x,f10.6,1x,i7,1x,f9.6,1x,i3)',imgfile[i],sky_median,sky_sigma,n_elements(all_ind),sigma_individual_sky_medians,n_elements(individual_sky_medians) ; file, median, sig, Nskypix

endfor
close,1
END

FUNCTION circ_ind,image,x_cen,y_cen,r

dims=size(image)
ind=lindgen(dims[1],dims[2])
x_arr=ind MOD dims[1]
y_arr=ind/dims[1]

dist=(x_arr-x_cen)^2.0+(y_arr-y_cen)^2.0

ind=where(dist LT r^2.0)

RETURN,ind

END

FUNCTION read_circ,file,x,y,r

; PURPOSE:
;     Reads a ds9 region file with circles

OPENR, lun, file, /GET_LUN

array = ''
line = ''
WHILE NOT EOF(lun) DO BEGIN & $
  READF, lun, line & $
  array = [array, line] & $
ENDWHILE
;close,lun
FREE_LUN,lun ; DAD

;num=n_elements(array)-5
num=n_elements(array)-1 ; DAD
x=fltarr(num)
y=fltarr(num)
r=fltarr(num)

FOR n=0,num-1 DO BEGIN

;   text_split=strsplit(array[n+5],'(),',/extract)
   text_split=strsplit(array[n+1],'(),',/extract) ; DAD
   x[n]=text_split[1]-1.0
   y[n]=text_split[2]-1.0
   r[n]=text_split[3]

ENDFOR

RETURN,0

END

;Staudaher gave me this:
;To run put all three in your path, then type:
;fitsky_ds9,imgfile,ds9file
;imgfile and ds9file are strings of the fits file and ds9 region file respectively.

;Cook gave me this:
;nsky=n_elements(x_sky)
;for m=0, nsky-1 do begin
;  ;use sigma clipping to get correct sky values
;  APER,im,x_sky[m],y_sky[m],flux_junk,flux_junkerr,flux_sky_temp,$
;       flux_skyerr_temp,1.,rad_sky[m],[0.,rad_sky[m]],[min(im)-10,max(im)+10],/flux,/meanback,/silent
;  flux_sky[m]=flux_sky_temp ;sky values per pix; double checked with interactive phot=right on the money
;  ;note: IMCNT sky values and std are way off....
;  ;below: do not sigma clip to get correct sky sigma for errors. (aka get rid of /meanback)
;  APER,im,x_sky[m],y_sky[m],flux_junk,flux_junkerr,flux_sky_temp,$
;       flux_skyerr_temp,1.,rad_sky[m],[0.,rad_sky[m]],[min(im)-10,max(im)+10],/flux,/silent
;  flux_sky_std[m]=flux_skyerr_temp 
;  ;standard deviation in sky values per pix within each sky aperture; double checked with interactive phot
;  ;also, these are slightly higher than sigma clipped sky std values
;endfor 
