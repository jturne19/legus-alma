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
