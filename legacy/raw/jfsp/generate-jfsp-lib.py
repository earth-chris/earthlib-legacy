#!/usr/bin/python

# import dependencies
import pandas as pd
import spectral as spectral
import numpy as np
import aei
import os

# set up output files
osli_npv = 'npv-jfsp.sli'
ohdr_npv = 'npv-jfsp.hdr'
ocsv_npv = 'npv-jfsp.csv'
osli_bare = 'bare-jfsp.sli'
ohdr_bare = 'bare-jfsp.hdr'
ocsv_bare = 'bare-jfsp.csv'
osli_burn = 'burn-jfsp.sli'
ohdr_burn = 'burn--jfsp.hdr'
ocsv_burn = 'burn-jfsp.csv'

# set the final columns for the output csv
cols_final = ['NAME', 'LEVEL_1', 'LEVEL_2', 'LEVEL_3', 'LEVEL_4', 'LAT', 'LON', 'SOURCE', 'NOTES']

# define file paths
npv_files = ['southern_california/npv/deadneed.txt',
               'southern_california/npv/deadlitt.txt',
               'southern_california/npv/deadmanz.txt',
               'southern_california/npv/kellbark.txt',
               'southern_california/npv/deaddumo.txt',
               'southern_california/npv/crosscut.txt',
               'southern_california/npv/deadgras.txt',
               'southern_california/npv/goldgras.txt',
               'southern_california/npv/deadceon.txt',
               'southern_california/npv/bleachwd.txt',
               'southern_california/npv/coulbark.txt',
               'western_montana/npv/yewdead.txt',
               'western_montana/npv/deadcott.txt',
               'western_montana/npv/deadpond.txt',
               'western_montana/npv/deadbark.txt',
               'western_montana/npv/deadfern.txt',
               'western_montana/npv/deadneed.txt',
               'western_montana/npv/deadlitt.txt',
               'western_montana/npv/wdslash.txt',
               'western_montana/npv/stmpwood.txt',
               'western_montana/npv/deadtwig.txt',
               'western_montana/npv/deadlodg.txt',
               'western_montana/npv/innrbark.txt',
               'western_montana/npv/deadsfir.txt',
               'western_montana/npv/oldwood.txt',
               'western_montana/npv/deaddoug.txt',
               'western_montana/npv/needbrow.txt',
               'interior_alaska/npv/dedbirch.txt',
               'interior_alaska/npv/deadwood.txt',
               'interior_alaska/npv/dedaspen.txt',
               'interior_alaska/npv/dedspruc.txt',
               'eastern_washington/brte_br.txt',
               'eastern_washington/difubr.txt',
               'eastern_washington/woodstrw.txt']

burn_files = ['interior_alaska/char/ash.txt',
              'interior_alaska/char/charduff.txt',
              'interior_alaska/char/chartree.txt',
              'southern_california/char/burncham.txt',
              'southern_california/char/charbark.txt',
              'southern_california/char/charlogs.txt',
              'southern_california/char/charrock.txt',
              'southern_california/char/charsoil.txt',
              'southern_california/char/graysoil.txt',
              'western_montana/char/ash_litter.txt',
              'western_montana/char/ash.txt',
              'western_montana/char/barkchar.txt',
              'western_montana/char/black_charwood.txt',
              'western_montana/char/charbark.txt',
              'western_montana/char/charrock.txt',
              'western_montana/char/charsoil.txt',
              'western_montana/char/charwood.txt',
              'western_montana/char/cooney_charwood.txt',
              'western_montana/char/light_charsoil.txt',
              'eastern_washington/difubr.txt',
              'eastern_washington/scorch_psme.txt']

# set up output arrays
npvnl = len(npv_files)
burnnl = len(burn_files)

npvout = np.zeros((npvnl, 2151), dtype = np.float32)
burnout = np.zeros((burnnl, 2151), dtype = np.float32)

# create lists for the file names to use as spectra names
npvnames = []
burnnames = []

# loop through each lib and read info
for i in range(npvnl):
    g = aei.read.jfsc(npv_files[i])
    npvout[i,:] = g.spectra[0,:].astype(np.float32)
    npvnames.append(os.path.basename(npv_files[i])[:-4])

for i in range(burnnl):
    g = aei.read.jfsc(burn_files[i])
    burnout[i,:] = g.spectra[0,:].astype(np.float32)
    burnnames.append(os.path.basename(burn_files[i])[:-4])

# write the data out to the sli files
with open(osli_npv, 'w') as f:
    npvout.tofile(f)

with open(osli_burn, 'w') as f:
    burnout.tofile(f)

# set up header info
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
    'wavelength' : g.band_centers
    }

# write npv header
spectral.envi.write_envi_header(ohdr_npv, metadata, is_library=True)

# edit and write for burn
metadata['lines'] = burnnl
metadata['spectra names'] = burnnames
spectral.envi.write_envi_header(ohdr_burn, metadata, is_library = True)

# set up level 3 labels for npv
npv_l3 = ['litter', 
    'litter', 
    'litter', 
    'bark', 
    'litter', 
    'wood', 
    'litter', 
    'litter', 
    'wood', 
    'wood', 
    'bark', 
    'wood', 
    'litter', 
    'litter', 
    'bark', 
    'litter', 
    'litter', 
    'litter', 
    'wood', 
    'wood', 
    'bark', 
    'litter', 
    'bark', 
    'litter', 
    'wood', 
    'litter', 
    'litter', 
    'bark', 
    'wood', 
    'bark', 
    'bark',
    'litter',
    'litter',
    'litter']

# then create the viper-format csv files
onpv = pd.DataFrame(columns=cols_final, index=range(npvnl))
onpv['NAME'] = npvnames
onpv['LEVEL_1'] = 'pervious'
onpv['LEVEL_2'] = 'npv'
onpv['LEVEL_3'] = npv_l3
onpv['LEVEL_4'] = 'measured'
onpv['LAT'] = 0.
onpv['LON'] = 0.
onpv['SOURCE'] = 'asd'
onpv['NOTES'] = 'joint fire science program'
onpv.to_csv(ocsv_npv, index=False)

oburn = pd.DataFrame(columns=cols_final, index=range(burnnl))
oburn['NAME'] = burnnames
oburn['LEVEL_1'] = 'pervious'
oburn['LEVEL_2'] = 'burn'
oburn['LEVEL_3'] = 'char'
oburn['LEVEL_4'] = 'measured'
oburn['LAT'] = 0.
oburn['LON'] = 0.
oburn['SOURCE'] = 'asd'
oburn['NOTES'] = 'joint fire science program'
oburn.to_csv(ocsv_burn, index=False)
