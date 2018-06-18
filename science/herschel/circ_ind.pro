FUNCTION circ_ind,image,x_cen,y_cen,r

dims=size(image)
ind=lindgen(dims[1],dims[2])
x_arr=ind MOD dims[1]
y_arr=ind/dims[1]

dist=(x_arr-x_cen)^2.0+(y_arr-y_cen)^2.0

ind=where(dist LT r^2.0)

RETURN,ind

END