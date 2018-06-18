################################################################################
procedure gettables (tables)
# task gettable=gettables.cl
# gettables @tables.list
# !rm tables.asc tables.tab

string tables   {"@tables_edited.list", prompt="input tables (= tables as in *.tab)"}
string outtable {"tables.tab", prompt="output table for basic data"}
string asctab   {"tables.asc",prompt="output ascii file for basic data"}
bool verbose    {yes, prompt="verbose output?"}

struct *tablelist

begin
	file table, tablefile, outtable1
	int pixels, ntable, len
	real net, bkgd, error_pix, neterr
        string source

	tablefile= mktemp("tmp$tbllst")
        sections(tables, option="fullname", > tablefile)
 	tablelist= tablefile

	cache("tabpar")
	cache("partab")
#
#   create empty output table:
#
	outtable1=mktemp("tmp$out")
	if (verbose) print("...creating empty table:",outtable1)
	tcreate(outtable1, "gettables.col", "",\
		nskip=0, nlines=1, hist=no)
	ntable= 0
#
#       process each table in list:
#
        while (fscan(tablelist,table) != EOF) {
         if (verbose) print("...processing ",table)
         net=0.0     # initialize
         bkgd=0.0     # initialize
         error_pix=0.0     # initialize
         pixels=0    # initialize
         source="none" # initialize
         len=strlen(table)
         if (verbose) print("...name & length ",table," ",len)
	 ntable += 1
         if (len!=1){
         
         keypar(table, "source")
         source=keypar.value
	 tabpar(table, "pixels",1)
         pixels=int(tabpar.value)
	 tabpar(table, "net",1)
         net=real(tabpar.value)
	 tabpar(table, "bkgd",1)
         bkgd=real(tabpar.value)
	 tabpar(table, "neterr",1)
         error_pix=real(tabpar.value)/real(pixels)
         
         print(source," ",net," ",pixels," ",error_pix)
         partab(net,     outtable1, "net",     ntable) 
         partab(bkgd,    outtable1, "bkgd",    ntable) 
         partab(pixels,  outtable1, "pixels",  ntable)       
         partab(source,  outtable1, "source",  ntable)
         partab(error_pix, outtable1, "error_pix", ntable)
         }
        else
         partab(net,     outtable1, "net",     ntable) 
         partab(bkgd,    outtable1, "bkgd",    ntable) 
         partab(pixels,  outtable1, "pixels",  ntable)       
         partab(source,  outtable1, "source",  ntable)
         partab(error_pix, outtable1, "error_pix", ntable)
 	} # done looping through all galaxies
        
        tcopy(outtable1,outtable)
        tdelete(outtable1,verify-)
        tinfo(outtable)
	tprint(outtable,pwidth=120,plength=3000,showrow=no, \
		showhdr=no,align=yes, > asctab)
end
