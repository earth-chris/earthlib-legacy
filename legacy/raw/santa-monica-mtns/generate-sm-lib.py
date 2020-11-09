# takes the santa monica mountains spectra and outputs them as a spectral library with metadata for vipertools

import aei
import random
import pyprosail
import numpy as np
import pandas as pd
import spectral as spectral

# set input paths
spec_path = 'santa-monica-mountains-vegetation-species-spectra.csv'

# set the output file paths
osli_bare = 'bare-santa-barbara.sli'
ohdr_bare = 'bare-santa-barbara.hdr'
ocsv_bare = 'bare-santa-barbara.csv'

osli_npv = 'npv-santa-barbara.sli'
ohdr_npv = 'npv-santa-barbara.hdr'
ocsv_npv = 'npv-santa-barbara.csv'

# set the order of the final output columns
cols_final = ['NAME', 'LEVEL_1', 'LEVEL_2', 'LEVEL_3', 'LEVEL_4', 'LAT', 'LON', 'SOURCE', 'NOTES']

# read the data
raw = pd.read_csv(spec_path)

# eh, its mostly veg/soil, which we have enough of atm