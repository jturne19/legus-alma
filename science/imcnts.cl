cd /uwpa2/turner/legus-alma/science/herschel
xray
xspatial
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

.exit