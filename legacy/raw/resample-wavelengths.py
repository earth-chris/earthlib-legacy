# god damn dealing with ENVI is fucking horrible
import os
import aei
import glob
import numpy as np
import pandas as pd
import spectral as spectral

inf = ['bare-santa-barbara.sli', 
          'burn_jfsp.sli', 
          'npv-hyspiri.sli', 
          'npv-santa-barbara.sli', 
          'npv-usgs.sli', 
          'npv_jfsp.sli', 
          'urban-santa-barbara.sli', 
          'veg-prosail.sli']
          
of = ['../cleaned/resampled/bare-santa-barbara-10nm.sli', 
      '../cleaned/resampled/burn-jfsp-10nm.sli', 
      '../cleaned/resampled/npv-hyspiri-10nm.sli', 
      '../cleaned/resampled/npv-santa-barbara-10nm.sli', 
      '../cleaned/resampled/npv-usgs-10nm.sli', 
      '../cleaned/resampled/npv-jfsp-10nm.sli', 
      '../cleaned/resampled/urban-santa-barbara-10nm.sli', 
      '../cleaned/resampled/veg-prosail-10nm.sli']

if len(inf) != len(of): print('input and output file lists do not match')

# set the reference waveltngth file
ref_f = 'soil-icraf-isric.sli'

# get the ref wavelengths
ref = aei.read.spectralLib(ref_f)
ref_wv = ref.band_centers

# loop through each input and set up resampling
for i in range(len(inf)):
    # read the input data
    g = aei.read.spectralLib(inf[i])
    
    # get the wavelengths to resample
    centers = g.band_centers
    
    # deal with micrometers
    if g.band_unit.lower() == 'micrometers':
        centers *= 1000.
        
    # set up the resampler
    rs = spectral.resampling.BandResampler(centers, ref_wv)
    
    # loop through each spectrum and resample
    nl = g.spectra.shape[0]
    nb = len(ref_wv)
    outarr = np.zeros((nl, nb))
    
    for j in range(nl):
        outarr[j] = rs(g.spectra[j])
        
    # save the output data
    with open(of[i], 'w') as f:
        outarr.astype(np.float32).tofile(f)
        
    metadata = {
        'samples' : nb,
        'lines' : nl,
        'bands' : 1,
        'data type' : 4,
        'header offset' : 0,
        'interleave' : 'bsq',
        'byte order' : 0,
        'spectra names' : g.names,
        'wavelength units' : 'nanometers',
        'wavelength' : ref_wv.astype(np.int32)
    }
    spectral.envi.write_envi_header(of[i]+'.hdr', metadata, is_library=True)
        