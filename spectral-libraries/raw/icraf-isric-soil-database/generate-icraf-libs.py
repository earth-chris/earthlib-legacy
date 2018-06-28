# takes the icraf-isric soil spectra and outputs them as a spectral library with metadata for vipertools

import os
import aei
import numpy as np
import pandas as pd
import spectral as spectral

# set the file paths
spec_path = 'spectra.csv'
desc_path = 'site-description.csv'

# set the output file paths
osli = 'bare-icraf-isric.sli'
ohdr = 'bare-icraf-isric.hdr'
ocsv = 'bare-icraf-isric.csv'

# set the order of the final output columns
cols_final = ['NAME', 'LEVEL_1', 'LEVEL_2', 'LEVEL_3', 'LEVEL_4', 'LAT', 'LON', 'SOURCE', 'NOTES']

# first, we'll read in the data
spec = pd.read_csv(spec_path)
desc = pd.read_csv(desc_path)

# then, we need to fill in some data gaps with in the site descriptions
def set_neg_lat(row):
    if row['LATNS'] == 'S':
        return -row['LATD']
    else:
        return row['LATD']
        
def set_neg_lon(row):
    if row['LONEW'] == 'W':
        return -row['LOND']
    else:
        return row['LOND']
        
def calc_dd(row):
    return aei.read.dms_to_dd(row['LATD'], row['LATM'], row['LATS'], row['LOND'], row['LONM'], row['LONS'])

def get_dd_lat(row):
    return row['DD'][0]
    
def get_dd_lon(row):
    return row['DD'][1]

# fill some no-data values
desc['LATD'] = desc['LATD'].fillna(value=0.)
desc['LOND'] = desc['LOND'].fillna(value=0.)
desc['LATM'] = desc['LATM'].fillna(value=0.)
desc['LONM'] = desc['LONM'].fillna(value=0.)
desc['LATS'] = desc['LATS'].fillna(value=0.)
desc['LONS'] = desc['LONS'].fillna(value=0.)

# set negative lat/lons for S/W
desc['LATD'] = desc.apply(set_neg_lat, axis=1)
desc['LOND'] = desc.apply(set_neg_lon, axis=1)

# convert dms to dd
desc['DD'] = desc.apply(calc_dd, axis=1)
desc['LAT'] = desc.apply(get_dd_lat, axis=1)
desc['LON'] = desc.apply(get_dd_lon, axis=1)

# set the country name to match the spectral data
desc['Plotcode'] = desc['ISO'].map(str) + ' ' + desc['ID'].map(str)

# and subset to just the columns we want to merge
cols_keep = ['Plotcode', 'LAT', 'LON']
desc_keep = desc[cols_keep]

# ok, we need to merge the spectral data and the site descriptions to pull metadata
merged = pd.merge(desc_keep, spec, on='Plotcode')

# convert the spectral data to an array and write it as a binary file
wls = merged.columns[6:]
wls_float = [float(i) for i in wls.tolist()]
refl = np.array(merged[wls]).astype(np.float32)

with open(osli, 'w') as f:
    refl.tofile(f)

# set up header info
metadata = {
    'samples' : refl.shape[1],
    'lines' : refl.shape[0],
    'bands' : 1,
    'data type' : 4,
    'header offset' : 0,
    'interleave' : 'bsq',
    'byte order' : 0,
    'sensor type' : 'ASD',
    'spectra names' : merged['Batch_Labid'].tolist(),
    'wavelength units' : 'nanometers',
    'wavelength' : wls_float
}

# write the envi file header
spectral.envi.write_envi_header(ohdr, metadata, is_library=True)

# and write out the final metadata csv file
cols_keep = ['LAT', 'LON', 'Batch_Labid']
md = merged[cols_keep]
md.rename(index=str, columns={'Batch_Labid': 'NAME'}, inplace=True)

# add other metadata for labeling
md['LEVEL_1'] = 'pervious'
md['LEVEL_2'] = 'bare'
md['LEVEL_3'] = 'soil'
md['LEVEL_4'] = 'measured'
md['SOURCE'] = 'asd'
md['NOTES'] = 'icraf-isric-soil-database'

# re-order the labels and write the output
md[cols_final].to_csv(ocsv, index=False)