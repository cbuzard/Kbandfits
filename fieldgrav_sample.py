import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from astrodbkit import astrodb
db = astrodb.Database('/Users/cammyfbuzard/Code/Python/BDNYC/BDNYCdev.db')

import montecarlotest_2 as mc

sources = pd.DataFrame(db.list("select source_id from spectral_types where gravity is null and regime='OPT'").fetchall())
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


#### no T dwarfs (those will use IR spectral types)

tdwarfs = []
for i in sources[0]:
	tdwarfs.append(db.list("SELECT spectral_type FROM spectral_types WHERE regime='OPT' AND source_id={}".format(i)).fetchone()[0])
noTs = []
for i in tdwarfs:
	if i >= 7.0 and i <= 19.5:
		noTs.append(i)
	else:
		noTs.append(None)
sources[1] = noTs
sources = sources.dropna()


#### any betas?? Not anymore!

grav = []
for i in sources[0]:
	grav.append(db.list("SELECT gravity FROM spectral_types WHERE regime='OPT' AND source_id={}".format(i)).fetchone()[0])
for num,i in enumerate(grav):
	if i == None or i == '':
		grav[num] = 1
	else:
		grav[num] = None
sources[1] = grav
sources = sources.dropna()			


#### spectral ids

spectral_ids = []
for i in sources[0]:
	try:
		spectral_ids.append(db.list("SELECT id FROM spectra WHERE source_id={} AND regime='NIR' AND instrument_id=6 AND mode_id=1".format(i)).fetchone()[0])
	except TypeError:
		spectral_ids.append(None)		
sources[1] = spectral_ids					
sources = sources.dropna()


fieldgrav = []			
for i,j in zip(sources[0],sources[1]):
	fieldgrav.append([i,j])


### Run

for i in range(len(fieldgrav)):
	mc.linear_fit(fieldgrav[i][0],fieldgrav[i][1])
	
	
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

df.to_csv('/Users/cammyfbuzard/Desktop/Monte_Carlo/06_09_16/Field_gravities/montecarlo_fits.txt',sep=',',index=False)										
		