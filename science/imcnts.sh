#!/bin/bash

export PATH=/usr/local/Anaconda/bin:$PATH
source activate iraf27
cd /uwpa2/turner/legus-alma/science

pyraf < imcnts.cl

# copy the output over to the science direcotry
yes | cp herschel/tables.asc phot.herschel.asc
