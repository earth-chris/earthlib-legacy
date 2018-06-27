#!/usr/bin/python

# import dependencies
import spectral as spectral
import numpy as np
import aei
import os

# set up output files
npvf = 'jfsp_npv_spectral_lib.sli'
npvh = 'jfsp_npv_spectral_lib.hdr'
baref = 'jfsp_bare_spectral_lib.sli'
bareh = 'jfsp_bare_spectral_lib.hdr'
charf = 'jfsp_char_spectral_lib.sli'
charh = 'jfsp_char_spectral_lib.hdr'

# define file paths
soil_files = ['/home/cba/cba/global/spectra/joint_fire_science_program/southern_california/soil/privcali.txt',
              '/home/cba/cba/global/spectra/joint_fire_science_program/southern_california/soil/bigrocks.txt',
              '/home/cba/cba/global/spectra/joint_fire_science_program/southern_california/soil/parksand.txt',
              '/home/cba/cba/global/spectra/joint_fire_science_program/southern_california/soil/hillcali.txt',
              '/home/cba/cba/global/spectra/joint_fire_science_program/southern_california/soil/deepcali.txt',
              '/home/cba/cba/global/spectra/joint_fire_science_program/southern_california/soil/sand.txt',
              '/home/cba/cba/global/spectra/joint_fire_science_program/southern_california/soil/bridge.txt',
              '/home/cba/cba/global/spectra/joint_fire_science_program/southern_california/soil/sandston.txt',
              '/home/cba/cba/global/spectra/joint_fire_science_program/western_montana/soil/calib5rd.txt',
              '/home/cba/cba/global/spectra/joint_fire_science_program/western_montana/soil/grayrock.txt',
              '/home/cba/cba/global/spectra/joint_fire_science_program/western_montana/soil/baresoil.txt',
              '/home/cba/cba/global/spectra/joint_fire_science_program/western_montana/soil/redrock.txt',
              '/home/cba/cba/global/spectra/joint_fire_science_program/western_montana/soil/site4cal.txt',
              '/home/cba/cba/global/spectra/joint_fire_science_program/western_montana/soil/grayrock_hillslope.txt',
              '/home/cba/cba/global/spectra/joint_fire_science_program/western_montana/soil/rockycal.txt',
              '/home/cba/cba/global/spectra/joint_fire_science_program/western_montana/soil/calibrd.txt',
              '/home/cba/cba/global/spectra/joint_fire_science_program/western_montana/soil/whalecal.txt',
              '/home/cba/cba/global/spectra/joint_fire_science_program/western_montana/soil/rocksig.txt',
              '/home/cba/cba/global/spectra/joint_fire_science_program/western_montana/soil/oldrocky.txt',
              '/home/cba/cba/global/spectra/joint_fire_science_program/western_montana/soil/bluesadl.txt',
              '/home/cba/cba/global/spectra/joint_fire_science_program/western_montana/soil/roadsoil.txt',
              '/home/cba/cba/global/spectra/joint_fire_science_program/western_montana/soil/rockunbu.txt',
              '/home/cba/cba/global/spectra/joint_fire_science_program/western_montana/soil/morelcal.txt',
              '/home/cba/cba/global/spectra/joint_fire_science_program/western_montana/soil/teepeeca.txt',
              '/home/cba/cba/global/spectra/joint_fire_science_program/western_montana/soil/soil_unb.txt',
              '/home/cba/cba/global/spectra/joint_fire_science_program/western_montana/soil/sgsaddle.txt',
              '/home/cba/cba/global/spectra/joint_fire_science_program/western_montana/soil/cooney_grayrock.txt',
              '/home/cba/cba/global/spectra/joint_fire_science_program/western_montana/soil/hillcal.txt']

woody_files = ['/home/cba/cba/global/spectra/joint_fire_science_program/southern_california/npv/deadneed.txt',
               '/home/cba/cba/global/spectra/joint_fire_science_program/southern_california/npv/deadlitt.txt',
               '/home/cba/cba/global/spectra/joint_fire_science_program/southern_california/npv/deadmanz.txt',
               '/home/cba/cba/global/spectra/joint_fire_science_program/southern_california/npv/kellbark.txt',
               '/home/cba/cba/global/spectra/joint_fire_science_program/southern_california/npv/deaddumo.txt',
               '/home/cba/cba/global/spectra/joint_fire_science_program/southern_california/npv/crosscut.txt',
               '/home/cba/cba/global/spectra/joint_fire_science_program/southern_california/npv/deadgras.txt',
               '/home/cba/cba/global/spectra/joint_fire_science_program/southern_california/npv/goldgras.txt',
               '/home/cba/cba/global/spectra/joint_fire_science_program/southern_california/npv/deadceon.txt',
               '/home/cba/cba/global/spectra/joint_fire_science_program/southern_california/npv/bleachwd.txt',
               '/home/cba/cba/global/spectra/joint_fire_science_program/southern_california/npv/coulbark.txt',
               '/home/cba/cba/global/spectra/joint_fire_science_program/western_montana/npv/yewdead.txt',
               '/home/cba/cba/global/spectra/joint_fire_science_program/western_montana/npv/deadcott.txt',
               '/home/cba/cba/global/spectra/joint_fire_science_program/western_montana/npv/deadpond.txt',
               '/home/cba/cba/global/spectra/joint_fire_science_program/western_montana/npv/deadbark.txt',
               '/home/cba/cba/global/spectra/joint_fire_science_program/western_montana/npv/deadfern.txt',
               '/home/cba/cba/global/spectra/joint_fire_science_program/western_montana/npv/deadneed.txt',
               '/home/cba/cba/global/spectra/joint_fire_science_program/western_montana/npv/deadlitt.txt',
               '/home/cba/cba/global/spectra/joint_fire_science_program/western_montana/npv/wdslash.txt',
               '/home/cba/cba/global/spectra/joint_fire_science_program/western_montana/npv/stmpwood.txt',
               '/home/cba/cba/global/spectra/joint_fire_science_program/western_montana/npv/deadtwig.txt',
               '/home/cba/cba/global/spectra/joint_fire_science_program/western_montana/npv/deadlodg.txt',
               '/home/cba/cba/global/spectra/joint_fire_science_program/western_montana/npv/innrbark.txt',
               '/home/cba/cba/global/spectra/joint_fire_science_program/western_montana/npv/deadsfir.txt',
               '/home/cba/cba/global/spectra/joint_fire_science_program/western_montana/npv/oldwood.txt',
               '/home/cba/cba/global/spectra/joint_fire_science_program/western_montana/npv/deaddoug.txt',
               '/home/cba/cba/global/spectra/joint_fire_science_program/western_montana/npv/needbrow.txt',
               '/home/cba/cba/global/spectra/joint_fire_science_program/interior_alaska/npv/dedbirch.txt',
               '/home/cba/cba/global/spectra/joint_fire_science_program/interior_alaska/npv/deadwood.txt',
               '/home/cba/cba/global/spectra/joint_fire_science_program/interior_alaska/npv/dedaspen.txt',
               '/home/cba/cba/global/spectra/joint_fire_science_program/interior_alaska/npv/dedspruc.txt']

char_files = aei.read.ascii('charlist.txt')

# set up output arrays
npvnl = len(woody_files)
barenl = len(soil_files)
charnl = len(char_files)

npvout = np.zeros((npvnl, 2151), dtype = np.float32)
bareout = np.zeros((barenl, 2151), dtype = np.float32)
charout = np.zeros((charnl, 2151), dtype = np.float32)

# create lists for the file names to use as spectra names
npvnames = []
barenames = []
charnames = []

# loop through each lib and read info
for i in range(npvnl):
    g = aei.read.jfsc(woody_files[i])
    npvout[i,:] = g.spectra[0,:].astype(np.float32)
    npvnames.append(os.path.basename(woody_files[i])[:-4])

for i in range(barenl):
    g = aei.read.jfsc(soil_files[i])
    bareout[i,:] = g.spectra[0,:].astype(np.float32)
    barenames.append(os.path.basename(soil_files[i])[:-4])

for i in range(charnl):
    g = aei.read.jfsc(char_files[i])
    charout[i,:] = g.spectra[0,:].astype(np.float32)
    charnames.append(os.path.basename(char_files[i])[:-4])

# write the data out to the sli files
with open(npvf, 'w') as f:
    npvout.tofile(f)

with open(baref, 'w') as f:
    bareout.tofile(f)

with open(charf, 'w') as f:
    charout.tofile(f)

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
spectral.envi.write_envi_header(npvh, metadata, is_library=True)

# edit and write for bare
metadata['lines'] = barenl
metadata['spectra names'] = barenames
spectral.envi.write_envi_header(bareh, metadata, is_library=True)

# edit and write for char
metadata['lines'] = charnl
metadata['spectra names'] = charnames
spectral.envi.write_envi_header(charh, metadata, is_library = True)
