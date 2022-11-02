"""Functions for reading specifically formatted data."""

import numpy as _np
import spectral as _spectral

from earthlib.utils import _endmember_path
from earthlib.utils import checkFile as _checkFile
from earthlib.utils import spectralObject as _spectralObject


# for ENVI spectral libraries
def spectralLibrary(path):
    """Reads an ENVI-format spectral library into memory.

    Args:
        path: file path to the ENVI spectral library file. Looks for a .hdr sidecar file.

    Returns:
        s: an earthlib spectralObject with the spectral library data.
    """

    # check for header files
    if _checkFile(path[:-4] + ".hdr"):
        hdr = path[:-4] + ".hdr"
    else:
        if _checkFile(path + ".hdr"):
            hdr = path + ".hdr"
        else:
            return None

    # read the spectral data
    slib = _spectral.envi.open(hdr, path)
    s = _spectralObject(
        slib.params.nrows,
        slib.params.ncols,
        band_centers=_np.asarray(slib.bands.centers),
        band_unit=slib.bands.band_unit,
        band_quantity=slib.bands.band_quantity,
    )

    # pull the spectra and names from the library
    s.spectra = slib.spectra
    s.names = slib.names

    return s


def endmembers():
    """Reads the earthlib spectral endmember library.

    Args:
        None.

    Returns:
        s: an earthlib spectralObject with the endmember library reflectance data.
    """

    s = spectralLibrary(_endmember_path)

    return s


def jfsp(path):
    """Reads JFSP-formatted ASCII files.

    Reads the ASCII format spectral data from the joint-fire-science-program
    and returns an object with the mean and +/- standard deviation reflectance data.
    Reference: https://www.frames.gov/assessing-burn-severity/spectral-library/overview

    Args:
        path: file path to the JFSP spectra text file.

    Returns:
        s: an earthlib spectralObject with the JFSP reflectance data.
    """

    # create the spectral object
    s = spectralObject(1, type="asd")
    s.spectra_stdevm = _np.zeros(s.spectra.shape)
    s.spectra_stdevp = _np.zeros(s.spectra.shape)

    # open the file and read the data
    with open(path, "r") as f:
        f.readline()
        for i, line in enumerate(f):
            line = line.strip().split()
            s.spectra[0, i] = line[1]
            s.spectra_stdevp[0, i] = line[2]
            s.spectra_stdevm[0, i] = line[3]

        return s


def usgs(path):
    """Reads USGS-formatted ASCII files.

    Reads the ascii format spectral data from USGS and returns an object with the mean
    and +/- standard deviation. Reference: https://www.sciencebase.gov/catalog/item/5807a2a2e4b0841e59e3a18d

    Args:
        path: file path the the USGS spectra text file.

    Returns:
        s: an earthlib spectralObject with the USGS reflectance data.
    """

    # open the file and read header info
    with open(path, "r") as f:
        x_start = "gibberish"
        for line in f:
            if x_start in line:
                break
            if "Name:" in line:
                spectrum_name = line.strip().split("Name:")[-1].strip()
            if "X Units:" in line:
                band_unit = line.strip().split()
                band_unit = band_unit[-1].strip("()").capitalize()
            if "Y Units:" in line:
                refl_unit = line.strip().split()
                refl_unit = refl_unit[-1].strip("()").capitalize()
            if "First X Value:" in line:
                x_start = line.strip().split()[-1]
            if "Number of X Values:" in line:
                n_values = int(line.strip().split()[-1])

        # now that we got our header info, create the arrays
        band_centers = _np.empty(n_values)
        reflectance = _np.empty(n_values)

        line = line.strip().split()
        band_centers[0] = float(line[0])
        reflectance[0] = float(line[1])

        # resume reading through file
        i = 1
        for line in f:
            line = line.strip().split()
            band_centers[i] = float(line[0])
            reflectance[i] = float(line[1])
            i += 1

        # some files read last -> first wavelength
        if band_centers[0] > band_centers[-1]:
            band_centers = band_centers[::-1]
            reflectance = reflectance[::1]

        # convert units to nanometers and scale 0-1
        if band_unit.lower() == "micrometers":
            band_centers *= 1000.0
            band_unit = "Nanometers"

        if refl_unit.lower() == "percent":
            reflectance /= 100.0

        # create the spectral object
        s = spectralObject(
            1,
            n_values,
            band_centers=band_centers,
            band_unit=band_unit,
            band_quantity="Wavelength",
        )

        # assign relevant values
        s.spectra[0] = reflectance
        if spectrum_name:
            s.names[0] = spectrum_name

    return s
