import ccblc
import numpy as np
import pandas as pd

# set the paths to the input and output files
isli = 'merged-speclib-landsat-8-ies.sli'
icsv = 'merged-speclib-landsat-8-ies.csv'
obase = '../../final/landsat-8-ies'

# set the level to split the data by
split = 'LEVEL_2'

# read the data into memory and get the unique labels
csv = pd.read_csv(icsv)
sli = ccblc.read.spectral_library(isli)
classes = csv[split].unique()
#labels = sli.band_centers

# remove the first band for l8
#labels = labels[1:]
labels = ['B2', 'B3', 'B4', 'B5', 'B6', 'B7']
spec_ind = np.arange(1,7).astype(np.int32)

# loop through each class, get the indices for that class in the spectral library, then write to csv
for c in classes:
    ind = np.array(csv[split] == c)
    
    # old stuff for exporting to a csv
    #arr = sli.spectra[ind, :]
    #arr = sli.spectra[ind, 1:]
    #df = pd.DataFrame(arr, columns=labels)
    #df.to_csv('{}-{}.csv'.format(obase, c), index_label='row_id')
    
    # new stuff for exporting to spectral libraries
    outfile = '{}-{}.sli'.format(obase, c)
    sli.write_sli(outfile, ind, spec_ind)
    
    # side note - the 