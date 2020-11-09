"""
Functions for reading specifically formatted data
"""
import numpy as np
import spectral

from ccblc.utils import spectralObject


# function to read ascii spectra from the joint fire science program
# (https://www.frames.gov/partner-sites/assessing-burn-severity/spectral/spectral-library-southern-california/)
def jfsc(path):
    """reads the ascii format spectral data from the joint-fire-science-program
    and returns an object with the mean and +/- standard deviation reflectance data

    Args:
        infile:

    Returns:
        a ccblc spectralObject with the jfsp reflectance data
    """

    # create the spectral object
    s = spectralObject(1, type="asd")
    s.spectra_stdevm = _np.zeros(s.spectra.shape)
    s.spectra_stdevp = _np.zeros(s.spectra.shape)

    # open the file and read the data
    with open(path, "r") as f:
        header = f.readline()
        i = 0
        for line in f:
            line = line.strip().split()
            s.spectra[0, i] = line[1]
            s.spectra_stdevp[0, i] = line[2]
            s.spectra_stdevm[0, i] = line[3]
            i += 1

        # return the spectral object
        return s


# function to read an envi spectral library file
def spectralLibrary(path):
    """reads an envi format spectral library

    Args:
        infile: the envi spectral library file (looks for an accompanying .hdr)

    Returns:
        a ccblc spectralObject with the spectral library data
    """
    # check for header files
    if check_file(infile[:-4] + ".hdr", quiet=True):
        hdr = infile[:-4] + ".hdr"
    else:
        if check_file(infile + ".hdr"):
            hdr = infile + ".hdr"
        else:
            return None

    # read the spectral data
    slib = spectral.envi.open(hdr, infile)

    # create the spectral object
    s = spectralObject(
        slib.params.nrows,
        slib.params.ncols,
        band_centers=_np.asarray(slib.bands.centers),
        band_unit=slib.bands.band_unit,
        band_quantity=slib.bands.band_quantity,
    )

    # set the spectra and names
    s.spectra = slib.spectra
    s.names = slib.names

    # return the final object
    return s


# clean up namespace
del np
del spectral
del spectralObject
