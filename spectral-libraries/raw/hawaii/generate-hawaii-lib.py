# takes the hyspiri spectra and outputs them as a spectral library with metadata for vipertools

import aei
import random
import pyprosail
import numpy as np
import pandas as pd
import spectral as spectral

# set input paths
spec_path = 'hawaii-2000-vegetation-species-spectra.csv'

# set the output file paths
osli_npv = 'npv-hyspiri.sli'
ohdr_npv = 'npv-hyspiri.hdr'
ocsv_npv = 'npv-hyspiri.csv'

# set the order of the final output columns
cols_final = ['NAME', 'LEVEL_1', 'LEVEL_2', 'LEVEL_3', 'LEVEL_4', 'LAT', 'LON', 'SOURCE', 'NOTES']

# read the data
raw = pd.read_csv(spec_path)

# nevermind this'n, also nothin' but veg, really