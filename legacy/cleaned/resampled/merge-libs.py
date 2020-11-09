# import dependencies
import os
import aei
import glob
import numpy as np
import pandas as pd
import spectral as spectral

# set the output files
osli = '../merged-speclibs.sli'
ohdr = '../merged-speclibs.sli.hdr'
ocsv = '../merged-speclibs.csv'

# list the spectral library and csv files to read
sli_files = ['bare-icraf-isric-10nm.sli', 
             'bare-santa-barbara-10nm.sli', 
             'burn-jfsp-10nm.sli', 
             'npv-hyspiri-10nm.sli', 
             'npv-jfsp-10nm.sli', 
             'npv-santa-barbara-10nm.sli', 
             'npv-usgs-10nm.sli', 
             'urban-santa-barbara-10nm.sli', 
             'veg-prosail-10nm.sli']

csv_files = ['bare-icraf-isric-10nm.csv', 
             'bare-santa-barbara-10nm.csv', 
             'burn-jfsp-10nm.csv', 
             'npv-hyspiri-10nm.csv', 
             'npv-jfsp-10nm.csv', 
             'npv-santa-barbara-10nm.csv', 
             'npv-usgs-10nm.csv', 
             'urban-santa-barbara-10nm.csv', 
             'veg-prosail-10nm.csv']
             
# ok, i'm going to be lazy about writing this
# loop through each list and load the data into memory
sli = []
csv = []
n_spec = 0
n_libs = len(sli_files)

for i in range(n_libs):
    s = aei.read.spectralLib(sli_files[i])
    sli.append(s)
    n_spec += s.spectra.shape[0]
    c = pd.read_csv(csv_files[i])
    csv.append(c)
    
# subset to the good bands to use
wv = s.band_centers
lo = wv < 400
hi = wv > 2450 
s1g = wv > 1350
s1l = wv < 1460
s2g = wv > 1790
s2l = wv < 1960

s1 = s1g & s1l
s2 = s2g & s2l
bb = s1 + s2 + hi + lo
gb = np.invert(bb)

# create the output array for the spectral data
n_bands = gb.sum()
outarr = np.zeros((n_spec, n_bands))

# set the first csv as the output dataframe, then concatenate all other frames to it
df = csv[0]

# then loop through and smoosh all the csvs and spectral libraries together
inl = 0
for i in range(n_libs):
    s = sli[i]
    nl = s.spectra.shape[0]
    outarr[inl:inl+nl, :] = s.spectra[:, gb]
    inl += nl
    
    if i > 0:
        df = df.append(csv[i])
        
# then write the output files
df.to_csv(ocsv, index=False)

with open(osli, 'w') as f:
    outarr.astype(np.float32).tofile(f)
    
metadata = {
    'samples' : n_bands,
    'lines' : n_spec,
    'bands' : 1,
    'data type' : 4,
    'header offset' : 0,
    'interleave' : 'bsq',
    'byte order' : 0,
    'spectra names' : df['NAME'].tolist(),
    'wavelength units' : 'nanometers',
    'wavelength' : wv[gb]
}
spectral.envi.write_envi_header(ohdr, metadata, is_library=True)
