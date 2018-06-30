# takes the hyspiri spectra and outputs them as a spectral library with metadata for vipertools

import aei
import random
import pyprosail
import numpy as np
import pandas as pd
import spectral as spectral

# set input paths
spec_path = 'nasa-hyspiri-airborne-campaign-leaf-and-canopy-spectra-and-leaf-traits.csv'

# set the output file paths
osli_npv = 'npv-hyspiri.sli'
ohdr_npv = 'npv-hyspiri.hdr'
ocsv_npv = 'npv-hyspiri.csv'

# set the order of the final output columns
cols_final = ['NAME', 'LEVEL_1', 'LEVEL_2', 'LEVEL_3', 'LEVEL_4', 'LAT', 'LON', 'SOURCE', 'NOTES']

# read the data
raw = pd.read_csv(spec_path)

# subsett these data by type
npv = raw[raw['Target Type'].isin(['NPV / litter', 'NPV', 'NPV / soil'])]

# erm, once again this is mostly veg. spectra. Who needs that shit, anyway?
# just pull the npv and gtfo
wls = raw.columns[20:]
wls_float = [float(i) / 1000 for i in wls.tolist()]
refl_npv = np.array(npv[wls]).astype(np.float32)

with open(osli_npv, 'w') as f:
    refl_npv.tofile(f)

# set up header info for each
metadata_npv = {
    'samples' : refl_npv.shape[1],
    'lines' : refl_npv.shape[0],
    'bands' : 1,
    'data type' : 4,
    'header offset' : 0,
    'interleave' : 'bsq',
    'byte order' : 0,
    'sensor type' : 'SpecEvo/ASD',
    'spectra names' : npv['Sample_Name'].tolist(),
    'wavelength units' : 'micrometers',
    'wavelength' : wls_float
}
spectral.envi.write_envi_header(ohdr_npv, metadata_npv, is_library=True)

# then output the csv file
onpv = pd.DataFrame(columns=cols_final, index=range(len(npv)))
onpv['NAME'] = npv['Sample_Name'].tolist()
onpv['LEVEL_1'] = 'pervious'
onpv['LEVEL_2'] = 'npv'
onpv['LEVEL_3'] = ['litter', 'npv', 'npv', 'npv', 'npv', 'npv', 'npv', 'npv', 'npv', 'npv']
onpv['LEVEL_4'] = 'measured'
onpv['LAT'] = npv['Latitude'].tolist()
onpv['LON'] = npv['Longitude'].tolist()
onpv['SOURCE'] = ['specevo', 'specevo', 'specevo', 'specevo', 'specevo', 'specevo', 'specevo', 'specevo', 'asd', 'asd']
onpv['NOTES'] = 'hyspiri simulation spectra'
onpv.to_csv(ocsv_npv, index=False)
