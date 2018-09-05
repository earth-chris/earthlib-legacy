# shebang
"""This is for testing and developing the scripts to run ccb-lc unmixing on earth engine
"""
import ee
import ccblc
import numpy as np
import pandas as pd
ee.Initialize()

# set the paths for the input files
slibp = '/home/cba/src/ccb-lc/spectral-libraries/final'
#lib1f = slibp + '/landsat-8-ies-bare.sli'
lib1f = '/home/cba/src/ccb-lc/spectral-libraries/raw/bare-santa-barbara-landsat-8-full.sli'
lib2f = slibp + '/landsat-8-ies-vegetation.sli'
#lib3f = slibp + '/landsat-8-ies-npv.sli'
lib3f = slibp + '/landsat-8-ies-urban.sli'

# set the collection to use
coll = ee.ImageCollection('LANDSAT/LC08/C01/T2_SR')

# set the seed
np.random.seed(1985)

# read the spectral libraries into memory
n_libs = 3
lib1r = ccblc.read.spectral_library(lib1f)
lib2r = ccblc.read.spectral_library(lib2f)
lib3r = ccblc.read.spectral_library(lib3f)

# do this in a loop later
libs_raw = [lib1r, lib2r, lib3r]

# to deal with cludging the santa barbara bare soil data
lib1r.spectra = lib1r.spectra[:, 1:]
lib1r.band_centers = lib1r.band_centers[1:]

# perform uniform random sampling for which spectra to select
n_spec = 30
ind1 = np.random.randint(0, lib1r.spectra.shape[0], n_spec)
ind2 = np.random.randint(0, lib2r.spectra.shape[0], n_spec)
ind3 = np.random.randint(0, lib3r.spectra.shape[0], n_spec)
inds = [ind1, ind2, ind3]

# loop through and print out the data so i can plug them in to the ee javascript editor
combo_list_py = []
combo_list_ee = []
for i in range(n_spec):
    l1str = ', '.join((lib1r.spectra[ind1[i]] * 10000).astype(np.int32).astype(np.string_))
    l2str = ', '.join((lib2r.spectra[ind2[i]] * 10000).astype(np.int32).astype(np.string_))
    l3str = ', '.join((lib3r.spectra[ind3[i]] * 10000).astype(np.int32).astype(np.string_))
    nmstr = "{:02d}".format(i)
    print("var bare_{} = ee.List([{}]);".format(nmstr, l1str))
    print("var vege_{} = ee.List([{}]);".format(nmstr, l2str))
    print("var urbn_{} = ee.List([{}]);".format(nmstr, l3str))
    print("var cmbo_{n} = ee.List([bare_{n}, vege_{n}, urbn_{n}]);".format(n=nmstr))
    combo_list_py.append('cmbo_{}'.format(nmstr))
    
    # the ee stuff
    combo_iter_py = []
    combo_iter_ee = []
    for j in range(n_libs):
        spec = (libs_raw[j].spectra[inds[j][i]] * 10000).astype(np.int32).tolist()
        spec_ee = ee.List(spec)
        combo_iter_ee.append(spec_ee)
        combo_iter_py.append(spec)
    
    combo_list_ee.append(ee.List(combo_iter_ee))
    
combo_list = ee.List(combo_list_ee)
combo_prnt = ', '.join(combo_list_py)
print('var combo = ee.List([{}]);'.format(combo_prnt))
    
    
    
    
    
    
    
    
    