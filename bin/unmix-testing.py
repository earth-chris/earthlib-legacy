# shebang
"""This is for testing and developing the scripts to run ccb-lc unmixing on earth engine
"""
import ee
import ccblc
import numpy as np
import pandas as pd

# set the paths for the input files
slibp = '/home/cba/src/ccb-lc/spectral-libraries/final'
lib1f = slibp + '/landsat-8-ies-bare.sli'
lib2f = slibp + '/landsat-8-ies-vegetation.sli'
lib3f = slibp + '/landsat-8-ies-urban.sli'

# set the collection to use
coll = ee.ImageCollection('LANDSAT/LC08/C01/T2_SR')

# set the seed
np.random.seed(1985)

# read the spectral libraries into memory
lib1 = ccblc.read.spectral_library(lib1f)
lib2 = ccblc.read.spectral_library(lib2f)
lib3 = ccblc.read.spectral_library(lib3f)

# perform uniform random sampling for which spectra to select
n_spec = 10
ind1 = np.random.randint(0, lib1.spectra.shape[0], n_spec)
ind2 = np.random.randint(0, lib2.spectra.shape[0], n_spec)
ind3 = np.random.randint(0, lib3.spectra.shape[0], n_spec)

# loop through and print out the data so i can plug them in to the ee javascript editor
for i in range(n_spec):
    l1str = ', '.join((lib1.spectra[ind1[i]] * 10000).astype(np.int32).astype(np.string_))
    l2str = ', '.join((lib2.spectra[ind2[i]] * 10000).astype(np.int32).astype(np.string_))
    l3str = ', '.join((lib3.spectra[ind3[i]] * 10000).astype(np.int32).astype(np.string_))
    nmstr = "{:02d}".format(i)
    print("var bare_{} = ee.List([{}]);".format(nmstr, l1str))
    print("var vege_{} = ee.List([{}]);".format(nmstr, l2str))
    print("var urbn_{} = ee.List([{}]);".format(nmstr, l3str))
    print("var cmbo_{n} = ee.List([bare_{n}, vege_{n}, urbn_{n}]);".format(n=nmstr))