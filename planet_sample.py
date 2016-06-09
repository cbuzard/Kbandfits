import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from astrodbkit import astrodb
db = astrodb.Database('/Users/cammyfbuzard/Code/Python/BDNYC/BDNYCdev.db')

import montecarlotest_2 as mc


#### Planets

source_id = [1508,1352,1309,1307,241,1378]				### 1507, 2096
spectral_id = [1657,8604,8602,8601,113,1658]				### 2688, 4442

sptype = []
for i in source_id:
	try:
		sptype.append(db.query("SELECT spectral_type FROM spectral_types WHERE regime='OPT' AND source_id={}".format(i),fetch='one')[0])
	except TypeError:
		sptype.append(14)

SNR = []
for i in source_id:
	if i == 1352:
		SNR.append(24)
	elif i == 1378:
		SNR.append(20)
	elif i == 1307 or i == 1309:
		SNR.append(6.6)
	else:
		SNR.append(0)

planet = []
for i,j,k,m in zip(source_id,spectral_id,sptype,SNR):
	planet.append([i,j,k,m])



#### Run K band fits
for i in range(len(planet)):
	mc.linear_fit(planet[i][0],planet[i][1],spectral_type=planet[i][2],SNR=planet[i][3]) 	
					



#### Use textfiles for other planets

textfile = ['/Users/cammyfbuzard/Code/Python/BDNYC/spec_comp_1609_K.txt','/Users/cammyfbuzard/Code/Python/BDNYC/HR8799b_Kband_medres.txt']

sptype = []
for i in textfile:
	sptype.append(14)

### Run

for i in range(len(textfile)):
	mc.linear_fit(textfile=textfile[i],spectral_type=14)	
	

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

df.to_csv('/Users/cammyfbuzard/Desktop/Monte_Carlo/06_09_16/Planets/montecarlo_fits.txt',sep=',',index=False)							