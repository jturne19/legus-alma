#>>> ======================================================================================#
#>>>                        TEMPLATE IMAGING PREP SCRIPT                                   #
#>>> ======================================================================================#
#>>>
#>>> Updated: Mon Apr  3 11:36:08 EDT 2017

#>>>
#>>> Lines beginning with '#>>>' are instructions to the data imager
#>>> and will be removed from the script delivered to the PI. If you
#>>> would like to include a comment that will be passed to the PI, begin
#>>> the line with a single '#', i.e., standard python comment syntax.
#>>>
#>>> Helpful tip: Use the commands %cpaste or %paste to copy and paste
#>>> indented sections of code into the casa command line.
#>>>
#>>>--------------------------------------------------------------------------------------#
#>>>                     Data Preparation                                                 #
#>>> -------------------------------------------------------------------------------------#
#>>>
#>>> Below are some example commands for combining your data. All of
#>>> these commands will not be relevant for all datasets, so think about
#>>> what would be best for your data before running any commands. For
#>>> more information, see the NA Imaging Guide
#>>> (https://staff.nrao.edu/wiki/bin/view/NAASC/NAImagingScripts).
#>>>
#>>> These commands should be run prior to undertaking any imaging.
#>>>>
#>>> The NA Imaging team is working on generating best
#>>> practices for this step. Suggestions are welcome!  Please send to
#>>> akepley@nrao.edu and she'll forward them on to the NA Imaging team.
#>>>
#>>>

########################################
# Getting a list of ms files to image

import glob

vislist=glob.glob('*.ms.split.cal')

##################################################
# Flag Bad Data [OPTIONAL]

#>>> If you have obviously bad antennas, channels, etc leftover from
#>>> the calibration, flag them here.

#>>> The policy for Cycle 3 is to flag baselines longer than 10km when imaging.

# Save original flags
for vis in vislist:
    flagmanager(vis=vis,
                mode='save',
                versionname='original_flags')

###############################################################
# Combining Measurement Sets from Multiple Executions 

#>>> DO NOT DO THIS IF YOU HAVE EQUALIZED THE FLUX BETWEEN THE
#>>> DIFFERENT EXECUTIONS OF A SCHEDULING BLOCK. The flux
#>>> equalization procedure already produces a single measurement set.

# If you have multiple executions, you will want to combine the
# scheduling blocks into a single ms using concat for ease of imaging
# and self-calibration. Each execution of the scheduling block will
# generate multiple spectral windows with different sky frequencies,
# but the same rest frequency, due to the motion of the Earth. Thus,
# the resulting concatentated file will contain n spws, where n is
# (#original science spws) x (number executions).  In other words, the
# multiple spws associated with a single rest frequency will not be
# regridded to a single spectral window in the ms.

concatvis='calibrated.ms'

rmtables(concatvis)
os.system('rm -rf ' + concatvis + '.flagversions')
concat(vis=vislist,
       concatvis=concatvis)

###################################
# Splitting off science target data

#>>> Uncomment following line for single executions
# concatvis = vislist[0]

#>>> Uncomment following line for multiple executions
concatvis='calibrated.ms'

#>>> Doing the split.  If multiple data sets were rescaled using
#>>> scriptForFluxCalibration.py, need to get datacolumn='corrected'

sourcevis='calibrated_source.ms'
rmtables(sourcevis)
os.system('rm -rf ' + sourcevis + '.flagversions')
split(vis=concatvis,
      intent='*TARGET*', # split off the target sources
      outputvis=sourcevis,
      datacolumn='data')



############################################
# Rename and backup data set

#>>> If you haven't regridded:
os.system('mv -i ' + sourcevis + ' ' + 'calibrated_final.ms')

#>>> If you have regridded:
# os.system('mv -i ' + regridvis + ' ' + 'calibrated_final.ms') 

# At this point you should create a backup of your final data set in
# case the ms you are working with gets corrupted by clean. 

os.system('cp -ir calibrated_final.ms calibrated_final.ms.backup')

#>>> Please do not modify the final name of the file
#>>> ('calibrated_final.ms'). The packaging process requires a file with
#>>> this name.

############################################
# Output a listobs file

listobs(vis='calibrated_final.ms',listfile='calibrated_final.ms.listobs.txt') 

