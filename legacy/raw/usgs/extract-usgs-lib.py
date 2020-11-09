#!/usr/bin/python

# import dependencies
import os
import aei
import glob
import numpy as np
import pandas as pd
import spectral as spectral

# set up output files
osli_npv = 'npv-usgs.sli'
ohdr_npv = 'npv-usgs.hdr'
ocsv_npv = 'npv-usgs.csv'

# set the final columns for the output csv
cols_final = ['NAME', 'LEVEL_1', 'LEVEL_2', 'LEVEL_3', 'LEVEL_4', 'LAT', 'LON', 'SOURCE', 'NOTES']

# define file paths
npv_files = ['vegetation/s07_ASD_D.spicata_DWV6-0511_dryNPV.a_ASDFRa_AREF.txt', 
             'vegetation/s07_ASD_Grass_dry.8+.2green_AMX31_BECKa_AREF.txt', 
             'vegetation/s07_ASD_Grass_dry.83+.17NaMont_AMX35_BECKb_AREF.txt', 
             'vegetation/s07_ASD_Grass_dry.9+.1green_AMX32_BECKa_AREF.txt', 
             'vegetation/s07_ASD_Marsh_sediment_DWV3-0511_dry_ASDFRa_AREF.txt', 
             'vegetation/s07_ASD_Marsh_wrack_DWV3-0511_dryNPV_ASDFRa_AREF.txt', 
             'vegetation/s07_ASD_P.aus._DWO-3-DEL-2d_dryNPV.a_ASDFRa_AREF.txt', 
             'vegetation/s07_ASD_P.australis_CRMS-0153_dryNPV_ASDFRa_AREF.txt', 
             'vegetation/s07_ASD_Sagebrush_Sage-Leaves-1_dry_ASDFRa_AREF.txt', 
             'vegetation/s07_ASD_Willow_Willow-Leaves-1_dry_ASDFRa_AREF.txt']

# set up output arrays
nb = 2151
npvnl = len(npv_files)

npvout = np.zeros((npvnl, nb), dtype = np.float32)

# create lists for the file names to use as spectra names
npvnames = []

# loop through each lib and read info
for i in range(npvnl):
    g = aei.read.ascii(npv_files[i])
    npvout[i,:] = np.array(g[1:]).astype(np.float32)
    npvnames.append((g[0]).split(' ')[2])
    
# mask some weird no-data values
npvout[npvout < 0] = 0.

# write the data out to the sli files
with open(osli_npv, 'w') as f:
    npvout.tofile(f)

# set up header info
wls = np.array(aei.read.ascii('s07_ASD_Wavelengths_ASD_0.35-2.5_microns_2151_ch.txt')[1:]).astype(np.float32)
metadata = {
    'samples' : 2151,
    'lines' : npvnl,
    'bands' : 1,
    'data type' : 4,
    'header offset' : 0,
    'interleave' : 'bsq',
    'byte order' : 0,
    'sensor type' : 'ASD',
    'spectra names' : npvnames,
    'wavelength units' : 'micrometers',
    'wavelength' : wls
    }

# write npv header
spectral.envi.write_envi_header(ohdr_npv, metadata, is_library=True)

# then create the viper-format csv files
onpv = pd.DataFrame(columns=cols_final, index=range(npvnl))
onpv['NAME'] = npvnames
onpv['LEVEL_1'] = 'pervious'
onpv['LEVEL_2'] = 'npv'
onpv['LEVEL_3'] = 'litter'
onpv['LEVEL_4'] = 'measured'
onpv['LAT'] = 0.
onpv['LON'] = 0.
onpv['SOURCE'] = 'asd'
onpv['NOTES'] = 'usgs'
onpv.to_csv(ocsv_npv, index=False)