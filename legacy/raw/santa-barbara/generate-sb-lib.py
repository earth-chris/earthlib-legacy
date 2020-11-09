# takes the santa barbara urband spectra and outputs them as a spectral library with metadata for vipertools

import aei
import random
import pyprosail
import numpy as np
import pandas as pd
import spectral as spectral

# set input paths
spec_path = 'urban-reflectance-spectra-from-santa-barbara--ca.csv'

# set the output file paths
osli_bare = 'bare-santa-barbara.sli'
ohdr_bare = 'bare-santa-barbara.hdr'
ocsv_bare = 'bare-santa-barbara.csv'

osli_npv = 'npv-santa-barbara.sli'
ohdr_npv = 'npv-santa-barbara.hdr'
ocsv_npv = 'npv-santa-barbara.csv'

osli_urban = 'urban-santa-barbara.sli'
ohdr_urban = 'urban-santa-barbara.hdr'
ocsv_urban = 'urban-santa-barbara.csv'

# set the order of the final output columns
cols_final = ['NAME', 'LEVEL_1', 'LEVEL_2', 'LEVEL_3', 'LEVEL_4', 'LAT', 'LON', 'SOURCE', 'NOTES']

# read the data
raw = pd.read_csv(spec_path)

# split the data into bare, urban, and npv tables
bare = raw[raw['Level_2'] == 'SOIL']
npv = raw[raw['Level_2'] == 'NPV']
urban = raw[raw['Level_2'].isin(['roof', 'paved', 'coating'])]

# pull the spectral data from each table, 
# convert to 0-1 refl and micrometers, and output to each spectral library
wls = raw.columns[17:]
wls_float = [float(i) / 1000 for i in wls.tolist()]
refl_bare = np.array(bare[wls]).astype(np.float32) / 10000.
refl_npv = np.array(npv[wls]).astype(np.float32) / 10000.
refl_urban = np.array(urban[wls]).astype(np.float32) / 10000.

with open(osli_bare, 'w') as f:
    refl_bare.tofile(f)
with open(osli_npv, 'w') as f:
    refl_npv.tofile(f)
with open(osli_urban, 'w') as f:
    refl_urban.tofile(f)

# set up header info for each
metadata_bare = {
    'samples' : refl_bare.shape[1],
    'lines' : refl_bare.shape[0],
    'bands' : 1,
    'data type' : 4,
    'header offset' : 0,
    'interleave' : 'bsq',
    'byte order' : 0,
    'sensor type' : 'ASD',
    'spectra names' : bare['Name'].tolist(),
    'wavelength units' : 'micrometers',
    'wavelength' : wls_float
}
spectral.envi.write_envi_header(ohdr_bare, metadata_bare, is_library=True)

metadata_npv = {
    'samples' : refl_npv.shape[1],
    'lines' : refl_npv.shape[0],
    'bands' : 1,
    'data type' : 4,
    'header offset' : 0,
    'interleave' : 'bsq',
    'byte order' : 0,
    'sensor type' : 'ASD',
    'spectra names' : npv['Name'].tolist(),
    'wavelength units' : 'micrometers',
    'wavelength' : wls_float
}
spectral.envi.write_envi_header(ohdr_npv, metadata_npv, is_library=True)

metadata_urban = {
    'samples' : refl_urban.shape[1],
    'lines' : refl_urban.shape[0],
    'bands' : 1,
    'data type' : 4,
    'header offset' : 0,
    'interleave' : 'bsq',
    'byte order' : 0,
    'sensor type' : 'ASD',
    'spectra names' : urban['Name'].tolist(),
    'wavelength units' : 'micrometers',
    'wavelength' : wls_float
}
spectral.envi.write_envi_header(ohdr_urban, metadata_urban, is_library=True)

# finally, set up the viper style output csvs for each group
obare = pd.DataFrame(columns=cols_final, index=range(len(bare)))
obare['NAME'] = bare['Name'].tolist()
obare['LEVEL_1'] = 'pervious'
obare['LEVEL_2'] = 'bare'
obare['LEVEL_3'] = bare['Level_3'].tolist()
obare['LEVEL_4'] = 'measured'
obare['LAT'] = bare['Latitude'].tolist()
obare['LON'] = bare['Longitude'].tolist()
obare['SOURCE'] = bare['source'].tolist()
obare['NOTES'] = 'urban reflectance spectra from santa barbara'
obare.to_csv(ocsv_bare, index=False)

onpv = pd.DataFrame(columns=cols_final, index=range(len(npv)))
onpv['NAME'] = npv['Name'].tolist()
onpv['LEVEL_1'] = 'pervious'
onpv['LEVEL_2'] = 'npv'
onpv['LEVEL_3'] = npv['Level_3'].tolist()
onpv['LEVEL_4'] = 'measured'
onpv['LAT'] = npv['Latitude'].tolist()
onpv['LON'] = npv['Longitude'].tolist()
onpv['SOURCE'] = npv['source'].tolist()
onpv['NOTES'] = 'urban reflectance spectra from santa barbara'
onpv.to_csv(ocsv_npv, index=False)

ourban = pd.DataFrame(columns=cols_final, index=range(len(urban)))
ourban['NAME'] = urban['Name'].tolist()
ourban['LEVEL_1'] = 'impervious'
ourban['LEVEL_2'] = 'urban'
ourban['LEVEL_3'] = urban['Level_3'].tolist()
ourban['LEVEL_4'] = 'measured'
ourban['LAT'] = urban['Latitude'].tolist()
ourban['LON'] = urban['Longitude'].tolist()
ourban['SOURCE'] = urban['source'].tolist()
ourban['NOTES'] = 'urban reflectance spectra from santa barbara'
ourban.to_csv(ocsv_urban, index=False)