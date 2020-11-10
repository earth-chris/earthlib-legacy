"""
Functions for reading specifically formatted data
"""


# function to read ascii spectra from the joint fire science program
# (https://www.frames.gov/assessing-burn-severity/spectral-library/overview)
def jfsp(path):
    """
    Reads the ASCII format spectral data from the joint-fire-science-program
    and returns an object with the mean and +/- standard deviation reflectance data

    :param path: file path to the JFSP spectra text file
    :return s: a ccblc spectralObject with the JFSP reflectance data
    """
    from ccblc.utils import checkFile, spectralObject

    # create the spectral object
    s = spectralObject(1, type="asd")
    s.spectra_stdevm = np.zeros(s.spectra.shape)
    s.spectra_stdevp = np.zeros(s.spectra.shape)

    # open the file and read the data
    with open(path, "r") as f:
        header = f.readline()
        for i, line in enumerate(f):
            line = line.strip().split()
            s.spectra[0, i] = line[1]
            s.spectra_stdevp[0, i] = line[2]
            s.spectra_stdevm[0, i] = line[3]

        # return the spectral object
        return s


# function to read ENVI spectral libraries
def spectralLibrary(path):
    """
    Reads an ENVI-format spectral library into memory.

    :param path: file path to the ENVI spectral library file. Looks for an accompanying .hdr file.
    :return s: a ccblc spectralObject with the spectral library data
    """
    import numpy as np
    import spectral

    from ccblc.utils import checkFile, spectralObject

    # check for header files
    if checkFile(path[:-4] + ".hdr"):
        hdr = path[:-4] + ".hdr"
    else:
        if checkFile(path + ".hdr"):
            hdr = path + ".hdr"
        else:
            return None

    # read the spectral data
    slib = spectral.envi.open(hdr, path)

    # create the spectral object
    s = spectralObject(
        slib.params.nrows,
        slib.params.ncols,
        band_centers=np.asarray(slib.bands.centers),
        band_unit=slib.bands.band_unit,
        band_quantity=slib.bands.band_quantity,
    )

    # set the spectra and names
    s.spectra = slib.spectra
    s.names = slib.names

    # return the final object
    return s
