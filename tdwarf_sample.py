##### this tests T dwarfs which have IR spectral types. remember to change sptype regime in montecarlotest_2 to 'IR'

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from astrodbkit import astrodb
db = astrodb.Database('/Users/cammyfbuzard/Dropbox/BDNYCdb/BDNYCdev.db')

import montecarlotest_2 as mc

sources = pd.DataFrame(db.list("select source_id from spectral_types where regime='IR'").fetchall())
sources = sources.drop_duplicates(0)


### No unresolved binaries

comp = []
for i in sources[0]:
	try:
		comp.append(db.list("SELECT components FROM sources WHERE id={}".format(i)).fetchone()[0])
	except TypeError:
		comp.append(1)	
for index,item in enumerate(comp):
	if item == None:
		comp[index] = 1
	else:
		comp[index] = None	
sources[1] = comp				
sources = sources.dropna()		


### No companions

comp = []
for i in sources[0]:
	try:
		comp.append(db.list("SELECT companions FROM sources WHERE id={}".format(i)).fetchone()[0])
	except TypeError:
		comp.append(1)	
for index,item in enumerate(comp):
	if item == None:
		comp[index] = 1
	else:
		comp[index] = None	
sources[1] = comp				
sources = sources.dropna()	


#### no objects that appear elsewhere

elsewhere = []
for i in sources[0]:
	if i == 241 or i == 183 or i == 700 or i == 739 or i == 54 or i == 1309 or i == 1721 or i == 1352 or i == 1307 or i == 1508 or i == 1378 or i == 443 or i == 791 or i == 757 or i == 854 or i == 366 or i == 118 or i == 1468:		
		## 118 had really large unc, 1468 is subdwarf 2M1626 
		elsewhere.append(None)
	else:
		elsewhere.append(i)
sources[1] = elsewhere
sources = sources.dropna()

#### Source ids of the non-T dwarf sample

original_sample = [ 743,  550,  196,   96,  175,  246,  237,  502,  216,  710,   82,
        137,  686,  623,  452,  376,  512,  723,  353,  587,    7,  336,
        220,  738,  441,  825,  464,  614,  856,  126,  575,  725,  691,
        392,  364,  697,  320,  214,   63,  775,  567,  287,  379,   86,
        785,  576,  650,  107,  698,  755,  455,  874,  824,  778,   10,
         19,   53,   55,   69,   99,  100,  134,  143,  145,  166,  174,
        187,  193,  223,  239,  245,  266,  286,  288,  301,  322,  324,
        333,  335,  349,  387,  421,  422,  432,  445,  458,  484,  488,
        526,  578,  583,  617,  619,  628,  681,  724,  736,  773,  818,
        820,  829,  833,  844,  848, 1371,  479, 1292,    4, 2030, 1452,
         20,  594, 1928,  415,   98,  700,  720,  443,  577,  579,   83,
        420,  183,  757,  854,   15,  751,  273,   91,  413,  275,  601,
         84,  140,  366,  449,  872, 1516, 1721, 1508, 1352, 1309, 1307,
        241, 1378, 1507, 2096]

canstay = []
for i in sources[0]:
	if i not in set(original_sample):
		canstay.append(i)
	else:
		canstay.append(None)
sources[1] = canstay
sources = sources.dropna()
		

#### only T dwarfs (those will use IR spectral types)

tdwarfs = []
for i in sources[0]:
	tdwarfs.append(db.list("SELECT spectral_type FROM spectral_types WHERE regime='IR' AND source_id={}".format(i)).fetchone()[0])
noTs = []
for i in tdwarfs:
	if i >= 20 and i <= 22.5:
		noTs.append(i)
	else:
		noTs.append(None)
sources[1] = noTs
sources = sources.dropna()


#### spectral ids

spectral_ids = []
for i in sources[0]:
	if i == 360:
		spectral_ids.append(2732)
	elif i == 437 or i == 538 or i == 2123:
		spectral_ids.append(None)	
	else:
		try:
			spectral_ids.append(db.list("SELECT id FROM spectra WHERE source_id={} AND regime='NIR'".format(i)).fetchone()[0])
		except TypeError:
			spectral_ids.append(None)		
sources[1] = spectral_ids					
sources = sources.dropna()



tdwarfs = []			
for i,j in zip(sources[0],sources[1]):
	tdwarfs.append([i,j])
	

### Run

for i in range(len(tdwarfs)):
	mc.linear_fit(tdwarfs[i][0],tdwarfs[i][1])
	
	
### Gather info

source_id = []
for i in range(len(mc.slopesvals)):
	source_id.append(mc.slopesvals[i][0])	
spectral_id = []
for i in range(len(mc.slopesvals)):
	spectral_id.append(mc.slopesvals[i][1])	
blue_slope = []
for i in range(len(mc.slopesvals)):
	blue_slope.append(mc.slopesvals[i][2])	
blue_std = []
for i in range(len(mc.slopesvals)):
	blue_std.append(mc.slopesvals[i][3])
red_slope = []
for i in range(len(mc.slopesvals)):
	red_slope.append(mc.slopesvals[i][4])
red_std = []
for i in range(len(mc.slopesvals)):
	red_std.append(mc.slopesvals[i][5])	
sptype = []
for i in range(len(mc.slopesvals)):
	sptype.append(mc.slopesvals[i][6])	
filename = []
for i in range(len(mc.slopesvals)):
	filename.append(mc.slopesvals[i][7])

df = pd.DataFrame(source_id)
df[1] = spectral_id
df[2] = blue_slope
df[3] = blue_std
df[4] = red_slope
df[5] = red_std
df[6] = sptype
df[7] = filename

df.columns = ['source_id','spectral_id','blue_slope','blue_std','red_slope','red_std','sp_type','filename']		

df.to_csv('/Users/cammyfbuzard/Desktop/Monte_Carlo/06_09_16/Overlap/Tdwarfs_montecarlo_fits.txt',sep=',',index=False)										
		

	
