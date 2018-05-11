# script / workflow

re-downloaded raw data from ALMA science archive

extracted all tar files

simplified the file structure since the default ALMA directories are numerous and not descriptive

file structure for band 4 12m data:

```bash
legus-alma
└──	raw
	├── band4
	│	└── 12m
	│	    ├── calibration
	│	    │   ├── antennapos.csv
	│	    │   ├── flux.csv
	│	    │   ├── uid___A001_X87c_X69.cont.dat
	│	    │   ├── uid___A001_X87c_X69.session_1.caltables.tgz
	│	    │   ├── uid___A001_X87c_X69.session_2.caltables.tgz
	│	    │   ├── uid___A002_Xba0af7_X6409_flagtargetstemplate.txt
	│	    │   ├── uid___A002_Xba0af7_X6409_flagtemplate.txt
	│	    │   ├── uid___A002_Xba0af7_X6409.ms.calapply.txt
	│	    │   ├── uid___A002_Xba0af7_X6409.ms.flagversions.tgz
	│	    │   ├── uid___A002_Xba0af7_X6ac1_flagtargetstemplate.txt
	│	    │   ├── uid___A002_Xba0af7_X6ac1_flagtemplate.txt
	│	    │   ├── uid___A002_Xba0af7_X6ac1.ms.calapply.txt
	│	    │   └── uid___A002_Xba0af7_X6ac1.ms.flagversions.tgz
	│	    ├── log
	│	    │   ├── casa-20170117-233444.log
	│	    │   ├── casa-20170118-003949.log
	│	    │   ├── casa-20170118-004134.log
	│	    │   ├── casa-20170119-202224.log
	│	    │   ├── casa-20170124-142630.log
	│	    │   └── uid___A001_X87c_X69.casa_commands.log
	│	    ├── product
	│	    │   ├── uid___A001_X87c_X69.J0006-0623_bp.spw17.mfs.I.pbcor.fits
	│	    │   ├── uid___A001_X87c_X69.J0006-0623_bp.spw17.mfs.I.pb.fits
	│	    │   ├── uid___A001_X87c_X69.J0006-0623_bp.spw19.mfs.I.pbcor.fits
	│	    │   ├── uid___A001_X87c_X69.J0006-0623_bp.spw19.mfs.I.pb.fits
	│	    │   ├── uid___A001_X87c_X69.J0006-0623_bp.spw21.mfs.I.pbcor.fits
	│	    │   ├── uid___A001_X87c_X69.J0006-0623_bp.spw21.mfs.I.pb.fits
	│	    │   ├── uid___A001_X87c_X69.J0006-0623_bp.spw23.mfs.I.pbcor.fits
	│	    │   ├── uid___A001_X87c_X69.J0006-0623_bp.spw23.mfs.I.pb.fits
	│	    │   ├── uid___A001_X87c_X69.J0139+1753_ph.spw17.mfs.I.pbcor.fits
	│	    │   ├── uid___A001_X87c_X69.J0139+1753_ph.spw17.mfs.I.pb.fits
	│	    │   ├── uid___A001_X87c_X69.J0139+1753_ph.spw19.mfs.I.pbcor.fits
	│	    │   ├── uid___A001_X87c_X69.J0139+1753_ph.spw19.mfs.I.pb.fits
	│	    │   ├── uid___A001_X87c_X69.J0139+1753_ph.spw21.mfs.I.pbcor.fits
	│	    │   ├── uid___A001_X87c_X69.J0139+1753_ph.spw21.mfs.I.pb.fits
	│	    │   ├── uid___A001_X87c_X69.J0139+1753_ph.spw23.mfs.I.pbcor.fits
	│	    │   ├── uid___A001_X87c_X69.J0139+1753_ph.spw23.mfs.I.pb.fits
	│	    │   ├── uid___A001_X87c_X69.J0238+1636_bp.spw17.mfs.I.pbcor.fits
	│	    │   ├── uid___A001_X87c_X69.J0238+1636_bp.spw17.mfs.I.pb.fits
	│	    │   ├── uid___A001_X87c_X69.J0238+1636_bp.spw19.mfs.I.pbcor.fits
	│	    │   ├── uid___A001_X87c_X69.J0238+1636_bp.spw19.mfs.I.pb.fits
	│	    │   ├── uid___A001_X87c_X69.J0238+1636_bp.spw21.mfs.I.pbcor.fits
	│	    │   ├── uid___A001_X87c_X69.J0238+1636_bp.spw21.mfs.I.pb.fits
	│	    │   ├── uid___A001_X87c_X69.J0238+1636_bp.spw23.mfs.I.pbcor.fits
	│	    │   ├── uid___A001_X87c_X69.J0238+1636_bp.spw23.mfs.I.pb.fits
	│	    │   ├── uid___A001_X87c_X69.NGC_628_sci.spw17_19_21_23.cont.I.alpha.error.fits
	│	    │   ├── uid___A001_X87c_X69.NGC_628_sci.spw17_19_21_23.cont.I.alpha.fits
	│	    │   ├── uid___A001_X87c_X69.NGC_628_sci.spw17_19_21_23.cont.I.pb.tt0.fits
	│	    │   ├── uid___A001_X87c_X69.NGC_628_sci.spw17_19_21_23.cont.I.tt0.pbcor.fits
	│	    │   ├── uid___A001_X87c_X69.NGC_628_sci.spw17_19_21_23.cont.I.tt1.pbcor.fits
	│	    │   ├── uid___A001_X87c_X69.NGC_628_sci.spw17.cube.I.pbcor.fits
	│	    │   ├── uid___A001_X87c_X69.NGC_628_sci.spw17.cube.I.pb.fits
	│	    │   ├── uid___A001_X87c_X69.NGC_628_sci.spw17.mfs.I.pbcor.fits
	│	    │   ├── uid___A001_X87c_X69.NGC_628_sci.spw17.mfs.I.pb.fits
	│	    │   ├── uid___A001_X87c_X69.NGC_628_sci.spw19.cube.I.pbcor.fits
	│	    │   ├── uid___A001_X87c_X69.NGC_628_sci.spw19.cube.I.pb.fits
	│	    │   ├── uid___A001_X87c_X69.NGC_628_sci.spw19.mfs.I.pbcor.fits
	│	    │   ├── uid___A001_X87c_X69.NGC_628_sci.spw19.mfs.I.pb.fits
	│	    │   ├── uid___A001_X87c_X69.NGC_628_sci.spw21.cube.I.pbcor.fits
	│	    │   ├── uid___A001_X87c_X69.NGC_628_sci.spw21.cube.I.pb.fits
	│	    │   ├── uid___A001_X87c_X69.NGC_628_sci.spw21.mfs.I.pbcor.fits
	│	    │   ├── uid___A001_X87c_X69.NGC_628_sci.spw21.mfs.I.pb.fits
	│	    │   ├── uid___A001_X87c_X69.NGC_628_sci.spw23.cube.I.pbcor.fits
	│	    │   ├── uid___A001_X87c_X69.NGC_628_sci.spw23.cube.I.pb.fits
	│	    │   ├── uid___A001_X87c_X69.NGC_628_sci.spw23.mfs.I.pbcor.fits
	│	    │   └── uid___A001_X87c_X69.NGC_628_sci.spw23.mfs.I.pb.fits
	│	    ├── qa
	│	    │   └── uid___A001_X87c_X69.weblog.tgz
	│	    ├── raw
	│	    │   ├── uid___A002_Xba0af7_X6409.asdm.sdm
	│	    │   └── uid___A002_Xba0af7_X6ac1.asdm.sdm
	│	    ├── README
	│	    ├── script
	│	    │   ├── casa_piperestorescript.py
	│	    │   ├── casa_pipescript.py
	│	    │   ├── PPR_uid___A001_X87c_X6a.xml
	│	    │   ├── scriptForImaging.py
	│	    │   └── scriptForPI.py
	│	    └── tar
	│	        ├── 2016.1.01435.S_uid___A001_X87c_X69_001_of_001.tar
	│	        ├── 2016.1.01435.S_uid___A002_Xba0af7_X6409.asdm.sdm.tar
	│	        └── 2016.1.01435.S_uid___A002_Xba0af7_X6ac1.asdm.sdm.tar
	└── band7
	 	├── 7m
	    │	├── calibration
	    │	│   ├── antennapos.csv
	    │	│   ├── flux.csv
	    │	│   ├── uid___A001_X87c_X6f.cont.dat
	    │	│   ├── uid___A001_X87c_X6f.session_1.caltables.tgz
	    │	│   ├── uid___A001_X87c_X6f.session_2.caltables.tgz
	    │	│   ├── uid___A001_X87c_X6f.session_3.caltables.tgz
	    │	│   ├── uid___A001_X87c_X6f.session_4.caltables.tgz
	    │	│   ├── uid___A001_X87c_X6f.session_5.caltables.tgz
	    │	│   ├── uid___A001_X87c_X6f.session_6.caltables.tgz
	    │	│   ├── uid___A001_X87c_X6f.session_7.caltables.tgz
	    │	│   ├── uid___A001_X87c_X6f.session_8.caltables.tgz
	    │	│   ├── uid___A002_Xb8e115_X1f93_flagtargetstemplate.txt
	    │	│   ├── uid___A002_Xb8e115_X1f93_flagtemplate.txt
	    │	│   ├── uid___A002_Xb8e115_X1f93.ms.calapply.txt
	    │	│   ├── uid___A002_Xb8e115_X1f93.ms.flagversions.tgz
	    │	│   ├── uid___A002_Xb8e115_X2cb0_flagtargetstemplate.txt
	    │	│   ├── uid___A002_Xb8e115_X2cb0_flagtemplate.txt
	    │	│   ├── uid___A002_Xb8e115_X2cb0.ms.calapply.txt
	    │	│   ├── uid___A002_Xb8e115_X2cb0.ms.flagversions.tgz
	    │	│   ├── uid___A002_Xb8f857_X1a7f_flagtargetstemplate.txt
	    │	│   ├── uid___A002_Xb8f857_X1a7f_flagtemplate.txt
	    │	│   ├── uid___A002_Xb8f857_X1a7f.ms.calapply.txt
	    │	│   ├── uid___A002_Xb8f857_X1a7f.ms.flagversions.tgz
	    │	│   ├── uid___A002_Xb903d6_X69f8_flagtargetstemplate.txt
	    │	│   ├── uid___A002_Xb903d6_X69f8_flagtemplate.txt
	    │	│   ├── uid___A002_Xb903d6_X69f8.ms.calapply.txt
	    │	│   ├── uid___A002_Xb903d6_X69f8.ms.flagversions.tgz
	    │	│   ├── uid___A002_Xb91513_X225e_flagtargetstemplate.txt
	    │	│   ├── uid___A002_Xb91513_X225e_flagtemplate.txt
	    │	│   ├── uid___A002_Xb91513_X225e.ms.calapply.txt
	    │	│   ├── uid___A002_Xb91513_X225e.ms.flagversions.tgz
	    │	│   ├── uid___A002_Xb91513_X34ce_flagtargetstemplate.txt
	    │	│   ├── uid___A002_Xb91513_X34ce_flagtemplate.txt
	    │	│   ├── uid___A002_Xb91513_X34ce.ms.calapply.txt
	    │	│   ├── uid___A002_Xb91513_X34ce.ms.flagversions.tgz
	    │	│   ├── uid___A002_Xb92da3_X25af_flagtargetstemplate.txt
	    │	│   ├── uid___A002_Xb92da3_X25af_flagtemplate.txt
	    │	│   ├── uid___A002_Xb92da3_X25af.ms.calapply.txt
	    │	│   ├── uid___A002_Xb92da3_X25af.ms.flagversions.tgz
	    │	│   ├── uid___A002_Xb92da3_X3341_flagtargetstemplate.txt
	    │	│   ├── uid___A002_Xb92da3_X3341_flagtemplate.txt
	    │	│   ├── uid___A002_Xb92da3_X3341.ms.calapply.txt
	    │	│   ├── uid___A002_Xb92da3_X3341.ms.flagversions.tgz
	    │	│   ├── uid___A002_Xb9356a_X221c_flagtargetstemplate.txt
	    │	│   ├── uid___A002_Xb9356a_X221c_flagtemplate.txt
	    │	│   ├── uid___A002_Xb9356a_X221c.ms.calapply.txt
	    │	│   └── uid___A002_Xb9356a_X221c.ms.flagversions.tgz
	    │	├── log
	    │	│   ├── casa-20161123-150354.log
	    │	│   ├── casa-20161123-173729.log
	    │	│   ├── casa-20161123-174549.log
	    │	│   ├── casa-20161206-184411.log
	    │	│   ├── casa-20161206-193932.log
	    │	│   ├── casa-20161213-160049.log
	    │	│   └── uid___A001_X87c_X6f.casa_commands.log
	    │	├── product
	    │	│   ├── uid___A001_X87c_X6f.J0006-0623_bp.spw16.mfs.I.pbcor.fits
	    │	│   ├── uid___A001_X87c_X6f.J0006-0623_bp.spw16.mfs.I.pb.fits
	    │	│   ├── uid___A001_X87c_X6f.J0006-0623_bp.spw18.mfs.I.pbcor.fits
	    │	│   ├── uid___A001_X87c_X6f.J0006-0623_bp.spw18.mfs.I.pb.fits
	    │	│   ├── uid___A001_X87c_X6f.J0006-0623_bp.spw20.mfs.I.pbcor.fits
	    │	│   ├── uid___A001_X87c_X6f.J0006-0623_bp.spw20.mfs.I.pb.fits
	    │	│   ├── uid___A001_X87c_X6f.J0006-0623_bp.spw22.mfs.I.pbcor.fits
	    │	│   ├── uid___A001_X87c_X6f.J0006-0623_bp.spw22.mfs.I.pb.fits
	    │	│   ├── uid___A001_X87c_X6f.J0152+2207_ph.spw16.mfs.I.pbcor.fits
	    │	│   ├── uid___A001_X87c_X6f.J0152+2207_ph.spw16.mfs.I.pb.fits
	    │	│   ├── uid___A001_X87c_X6f.J0152+2207_ph.spw18.mfs.I.pbcor.fits
	    │	│   ├── uid___A001_X87c_X6f.J0152+2207_ph.spw18.mfs.I.pb.fits
	    │	│   ├── uid___A001_X87c_X6f.J0152+2207_ph.spw20.mfs.I.pbcor.fits
	    │	│   ├── uid___A001_X87c_X6f.J0152+2207_ph.spw20.mfs.I.pb.fits
	    │	│   ├── uid___A001_X87c_X6f.J0152+2207_ph.spw22.mfs.I.pbcor.fits
	    │	│   ├── uid___A001_X87c_X6f.J0152+2207_ph.spw22.mfs.I.pb.fits
	    │	│   ├── uid___A001_X87c_X6f.J0510+1800_bp.spw16.mfs.I.pbcor.fits
	    │	│   ├── uid___A001_X87c_X6f.J0510+1800_bp.spw16.mfs.I.pb.fits
	    │	│   ├── uid___A001_X87c_X6f.J0510+1800_bp.spw18.mfs.I.pbcor.fits
	    │	│   ├── uid___A001_X87c_X6f.J0510+1800_bp.spw18.mfs.I.pb.fits
	    │	│   ├── uid___A001_X87c_X6f.J0510+1800_bp.spw20.mfs.I.pbcor.fits
	    │	│   ├── uid___A001_X87c_X6f.J0510+1800_bp.spw20.mfs.I.pb.fits
	    │	│   ├── uid___A001_X87c_X6f.J0510+1800_bp.spw22.mfs.I.pbcor.fits
	    │	│   ├── uid___A001_X87c_X6f.J0510+1800_bp.spw22.mfs.I.pb.fits
	    │	│   ├── uid___A001_X87c_X6f.J0522-3627_bp.spw16.mfs.I.pbcor.fits
	    │	│   ├── uid___A001_X87c_X6f.J0522-3627_bp.spw16.mfs.I.pb.fits
	    │	│   ├── uid___A001_X87c_X6f.J0522-3627_bp.spw18.mfs.I.pbcor.fits
	    │	│   ├── uid___A001_X87c_X6f.J0522-3627_bp.spw18.mfs.I.pb.fits
	    │	│   ├── uid___A001_X87c_X6f.J0522-3627_bp.spw20.mfs.I.pbcor.fits
	    │	│   ├── uid___A001_X87c_X6f.J0522-3627_bp.spw20.mfs.I.pb.fits
	    │	│   ├── uid___A001_X87c_X6f.J0522-3627_bp.spw22.mfs.I.pbcor.fits
	    │	│   ├── uid___A001_X87c_X6f.J0522-3627_bp.spw22.mfs.I.pb.fits
	    │	│   ├── uid___A001_X87c_X6f.J2253+1608_bp.spw16.mfs.I.pbcor.fits
	    │	│   ├── uid___A001_X87c_X6f.J2253+1608_bp.spw16.mfs.I.pb.fits
	    │	│   ├── uid___A001_X87c_X6f.J2253+1608_bp.spw18.mfs.I.pbcor.fits
	    │	│   ├── uid___A001_X87c_X6f.J2253+1608_bp.spw18.mfs.I.pb.fits
	    │	│   ├── uid___A001_X87c_X6f.J2253+1608_bp.spw20.mfs.I.pbcor.fits
	    │	│   ├── uid___A001_X87c_X6f.J2253+1608_bp.spw20.mfs.I.pb.fits
	    │	│   ├── uid___A001_X87c_X6f.J2253+1608_bp.spw22.mfs.I.pbcor.fits
	    │	│   ├── uid___A001_X87c_X6f.J2253+1608_bp.spw22.mfs.I.pb.fits
	    │	│   ├── uid___A001_X87c_X6f.NGC_628_sci.spw16_18_20_22.cont.I.pbcor.fits
	    │	│   ├── uid___A001_X87c_X6f.NGC_628_sci.spw16_18_20_22.cont.I.pb.fits
	    │	│   ├── uid___A001_X87c_X6f.NGC_628_sci.spw16.cube.I.pbcor.fits
	    │	│   ├── uid___A001_X87c_X6f.NGC_628_sci.spw16.cube.I.pb.fits
	    │	│   ├── uid___A001_X87c_X6f.NGC_628_sci.spw16.mfs.I.pbcor.fits
	    │	│   ├── uid___A001_X87c_X6f.NGC_628_sci.spw16.mfs.I.pb.fits
	    │	│   ├── uid___A001_X87c_X6f.NGC_628_sci.spw18.cube.I.pbcor.fits
	    │	│   ├── uid___A001_X87c_X6f.NGC_628_sci.spw18.cube.I.pb.fits
	    │	│   ├── uid___A001_X87c_X6f.NGC_628_sci.spw18.mfs.I.pbcor.fits
	    │	│   ├── uid___A001_X87c_X6f.NGC_628_sci.spw18.mfs.I.pb.fits
	    │	│   ├── uid___A001_X87c_X6f.NGC_628_sci.spw20.cube.I.pbcor.fits
	    │	│   ├── uid___A001_X87c_X6f.NGC_628_sci.spw20.cube.I.pb.fits
	    │	│   ├── uid___A001_X87c_X6f.NGC_628_sci.spw20.mfs.I.pbcor.fits
	    │	│   ├── uid___A001_X87c_X6f.NGC_628_sci.spw20.mfs.I.pb.fits
	    │	│   ├── uid___A001_X87c_X6f.NGC_628_sci.spw22.cube.I.pbcor.fits
	    │	│   ├── uid___A001_X87c_X6f.NGC_628_sci.spw22.cube.I.pb.fits
	    │	│   ├── uid___A001_X87c_X6f.NGC_628_sci.spw22.mfs.I.pbcor.fits
	    │	│   └── uid___A001_X87c_X6f.NGC_628_sci.spw22.mfs.I.pb.fits
	    │	├── qa
	    │	│   └── uid___A001_X87c_X6f.weblog.tgz
	    │	├── raw
	    │	│   ├── uid___A002_Xb8e115_X1f93.asdm.sdm
	    │	│   ├── uid___A002_Xb8e115_X2cb0.asdm.sdm
	    │	│   ├── uid___A002_Xb8f857_X1a7f.asdm.sdm
	    │	│   ├── uid___A002_Xb903d6_X69f8.asdm.sdm
	    │	│   ├── uid___A002_Xb91513_X225e.asdm.sdm
	    │	│   ├── uid___A002_Xb91513_X34ce.asdm.sdm
	    │	│   ├── uid___A002_Xb92da3_X25af.asdm.sdm
	    │	│   ├── uid___A002_Xb92da3_X3341.asdm.sdm
	    │	│   └── uid___A002_Xb9356a_X221c.asdm.sdm
	    │	├── README
	    │	├── script
	    │	│   ├── casa_piperestorescript.py
	    │	│   ├── casa_pipescript.py
	    │	│   ├── PPR_uid___A001_X87c_X70.xml
	    │	│   ├── scriptForImaging.py
	    │	│   └── scriptForPI.py
	    │	└── tar
	    │	    ├── 2016.1.01435.S_uid___A001_X87c_X6f_001_of_001.tar
	    │	    ├── 2016.1.01435.S_uid___A002_Xb8e115_X1f93.asdm.sdm.tar
	    │	    ├── 2016.1.01435.S_uid___A002_Xb8e115_X2cb0.asdm.sdm.tar
	    │	    ├── 2016.1.01435.S_uid___A002_Xb8f857_X1a7f.asdm.sdm.tar
	    │	    ├── 2016.1.01435.S_uid___A002_Xb903d6_X69f8.asdm.sdm.tar
	    │	    ├── 2016.1.01435.S_uid___A002_Xb91513_X225e.asdm.sdm.tar
	    │	    ├── 2016.1.01435.S_uid___A002_Xb91513_X34ce.asdm.sdm.tar
	    │	    ├── 2016.1.01435.S_uid___A002_Xb92da3_X25af.asdm.sdm.tar
	    │	    ├── 2016.1.01435.S_uid___A002_Xb92da3_X3341.asdm.sdm.tar
	    │	    └── 2016.1.01435.S_uid___A002_Xb9356a_X221c.asdm.sdm.tar
		└── 12m

```


## prep for imaging

reproduce the pipeline calibrated.ms --> this will create the 'calibrated' directory which will be needed for imaging

need to use casa version 4.7.0-1 (r38335) because that's what was orginally used

```bash
cd script
casa-release-4.7.0-1-el7/bin/casa --pipeline
```
```python
execfile('scriptForPI.py')

```
