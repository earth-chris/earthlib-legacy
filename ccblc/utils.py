"""
Utility functions for working with spectral libraries and earth engine routines
"""
import json
import logging
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import spectral

# set up logging
logging.basicConfig(
    level=logging.WARNING,
    format=("%(asctime)s %(levelname)s %(name)s [%(funcName)s] | %(message)s"),
    stream=sys.stdout,
)
LOGGER = logging.getLogger("ccblc")

# get file paths for the package data
_package_path = os.path.realpath(__file__)
_package_dir = os.path.dirname(_package_path)
_collections_path = os.path.join(_package_dir, "data", "collections.json")
_metadata_path = os.path.join(_package_dir, "data", "spectra.csv")
_endmember_path = os.path.join(_package_dir, "data", "spectra.sli")

# read the collections data into memory
with open(_collections_path, "r+") as f:
    collections = json.load(f)

# read the spectral metadata into memory
metadata = pd.read_csv(_metadata_path)


# helper / utility functions
def checkFile(path):
    """
    Checks if a file exists and can be read.

    :param path: the file path to check
    :return bool:
    """
    if os.path.isfile(path) and os.access(path, os.R_OK):
        return True
    else:
        return False


def listSensors():
    """
    Returns a list of the supported sensor image collections.

    :returns sensors: a list of supported sensors using the names referenced by this package
    """
    sensors = list(collections.keys())
    return sensors


def listBands(sensor):
    """
    Returns a list of the band names for a specific sensor.

    :param sensor: the sensor type
    :return bands: a list of band names for that sensor
    """
    bands = collections[sensor]["band_names"]
    return bands


def listTypes(level=2):
    """
    Returns a list of the spectral classification types.

    :param level: the level of spectral classification specificity to return. Supports integers 1-4.
    :returns classes: a list of spectral data types referenced throughout this package
    """
    key = f"LEVEL_{level}"
    types = list(metadata[key].unique())
    return types


def getTypeLevel(Type):
    """
    Checks whether a spectral data type is available in the endmember library.

    :param Type: the type of spectra to select
    :return level: the metadata "level" of the group for subsetting. returns 0 if not found.
    """
    for i in range(4):
        level = i + 1
        available_types = listTypes(level=level)
        if Type in available_types:
            return level

    return 0


def getCollection(sensor):
    """
    Returns the earth engine collection name for a specific satellite sensor.

    :param sensor: the name of the sensor (from ccblc.listSensors()).
    :return collection: a string with the earth engine collection
    """
    collection = collections[sensor]["collection"]
    return collection


def getScaler(sensor):
    """
    Returns the scaling factor to convert sensor data to percent reflectance (0-1).

    :param sensor: the name of the sensor (from ccblc.listSensors()).
    """
    scaler = collections[sensor]["scale"]
    return scaler


def getBands(sensor):
    """
    Returns a list of available band names by sensor

    :param sensor: the name of the sensor (from ccblc.listSensors()).
    :return bands: a list of sensor-specific band names
    """
    bands = collections[sensor]["band_names"]
    return bands


def getBandIndices(custom_bands, sensor):
    """
    Cross-references a list of bands passed as strings to the 0-based integer indices

    :param custom_bands: a list of band names
    :param sensor: a string sensor type for indexing the supported collections
    :return indices: a list of integer band indices
    """
    sensor_bands = collections[sensor]["band_names"]
    indices = list()
    for band in custom_bands:
        if band in sensor_bands:
            indices.append(sensor_bands.index(band))
    indices.sort()
    return indices


def selectSpectra(Type, sensor, n=0, bands=None):
    """
    Subsets the ccblc spectral endmember library to a specific class and resamples the spectra
    to the wavelengths of a specific satellite sensor. This also performs random spectra selection.

    :param Type: the type of spectra to select
    :param sensor: the sensor type to resample wavelengths to
    :param n: the number of random spectra to sample. n=0 returns all spectra
    :param bands: a list of bands to use. Accepts 0-based indices or a list of band names (e.g. ["B2", "B3", "B4"])
    :return spectra: a list of spectral endmembers resampled to a specific sensor's wavelengths.
    """
    import spectral

    from . import Read

    # get the level of the group selected
    level = getTypeLevel(Type)
    if level == 0:
        LOGGER.warning(
            f"Invalid group parameter: {Type}. Get valid values from ccblc.listTypes()."
        )
        return None

    # qc the collection selected
    if sensor not in listSensors():
        LOGGER.warning(
            f"Invalid sensor parameter: {sensor}. Get valid values from ccblc.listSensors()."
        )
        return None

    # read the spectral library into memory
    endmembers = Read.spectralLibrary(_endmember_path)

    # subset to specific bands, if set
    if bands is None:
        bands = range(len(getBands(sensor)))
    else:
        if type(bands[0]) is str:
            bands = getBandIndices(bands, sensor)

    # create a band resampler for this collection
    sensor_centers = np.array(collections[sensor]["band_centers"])[bands]
    sensor_fwhm = np.array(collections[sensor]["band_widths"])[bands]
    resampler = spectral.BandResampler(
        endmembers.band_centers, sensor_centers, fwhm2=sensor_fwhm
    )

    # select the endmembers from just the type passed
    key = f"LEVEL_{level}"
    indices = metadata[key] == Type
    spectra_raw = endmembers.spectra[indices, :]

    # subset them further if the n parameter is passed
    if n > 0:
        random_indices = np.random.randint(indices.sum(), size=n)
        spectra_raw = spectra_raw[random_indices, :]

    # loop through each spectrum and resample to the sensor wavelengths
    resampled = list()
    for i in range(spectra_raw.shape[0]):
        spectrum = resampler(spectra_raw[i, :])
        resampled.append(spectrum)

    return resampled


class spectralObject:
    def __init__(
        self,
        n_spectra=1,
        n_wl=2151,
        sensor=None,
        band_unit=None,
        band_centers=None,
        band_quantity="Wavelength",
    ):
        """
        A custom object that reads, stores, writes, and plots spectral data.

        :param n_spectra: the number of spectra included in the library
        :param n_wl: the number of wavelengths for each spectrum
        :param sensor: the sensor name
        :param band_unit: the unit of measurement (typically micrometers or nanometers)
        :param band_centers: the center wavelength for each band
        :param band_quantity: the quantity measured by each band
        :return s: a spectral object
        """

        # set to asd type if no params set to change n_wl
        if n_wl == 2151:
            sensor = "asd"

        # set up pre-defined types
        if sensor is not None:
            if sensor.lower() == "asd":
                n_wl = 2151
                band_unit = "Nanometers"
                band_quantity = "Wavelength"
                band_centers = np.arange(350, 2501)

        # return a list same size as number of spectra
        self.names = []
        for i in range(n_spectra):
            self.names.append("Spectrum {}".format(i))

        # set up the band definitions
        try:
            self.band_unit = band_unit
        except NameError:
            self.band_unit = None
        try:
            self.band_quantity = band_quantity
        except NameError:
            self.band_quantity = None
        try:
            self.band_centers = band_centers
        except NameError:
            self.band_centers = None

        # return an np array size of n spectra x n wavelengths
        self.spectra = np.zeros([n_spectra, n_wl])

    def remove_water_bands(self, set_nan=False):
        """
        Sets reflectance data from water absorption bands to 0 or NaN (1.35-1.46 um and 1.79-1.96 um).

        :param set_nan: set the water bands to NaN. False sets values to 0.
        :return none: updates the self.spectra array
        """
        if set_nan:
            update_val = np.nan
        else:
            update_val = 0

        if self.band_unit.lower() == "micrometers":
            water_bands = [[1.35, 1.46], [1.79, 1.96]]
        else:
            water_bands = [[1350.0, 1460.0], [1790.0, 1960.0]]

        # start with nir-swir1 transition
        gt = np.where(self.band_centers > water_bands[0][0])
        lt = np.where(self.band_centers < water_bands[0][1])
        nd = np.intersect1d(gt[0], lt[0])
        self.spectra[:, nd] = update_val

        # then swir1-swir2 transition
        gt = np.where(self.band_centers > water_bands[1][0])
        lt = np.where(self.band_centers < water_bands[1][1])
        nd = np.intersect1d(gt[0], lt[0])
        self.spectra[:, nd] = update_val

    def get_shortwave_bands(self):
        """
        Returns an index of the bands that encompass the shortwave range (350 - 2500 nm)

        :return overlap: an index of bands to subset to the shortwave range
        """
        # set range to return in nanometers
        shortwave_range = [350.0, 2500.0]

        # normalize if wavelength units are different
        if self.band_unit.lower() == "micrometers":
            shortwave_range /= 1000.0

        # find overlapping range
        gt = np.where(self.band_centers > shortwave_range[0])
        lt = np.where(self.band_centers < shortwave_range[1])
        overlap = np.intersect1d(gt[0], lt[0])

        # return output
        return overlap

    def plot(self, inds=None, legend=False):
        """
        Plots the spectra using a standard format

        :param inds: optional 0-based indices for which spectra to plot
        :param legend: add a legend with the spectra names
        :return plt: the matplotlib pyplot object
        """

        # set basic parameters
        plt.xlim((self.band_centers.min(), self.band_centers.max()))
        plt.xlabel("Wavelength ({})".format(self.band_unit))
        plt.ylabel("Reflectance (%)")

        # check if indices were set and valid. if not, plot all items
        if inds is not None:
            if np.max(inds) > len(self.names):
                inds = range(0, len(self.names))
                print("Invalid range set. using all spectra")
            if np.min(inds) < 0:
                inds = range(0, len(self.names))
                print("Invalid range set. using all spectra")
        else:
            inds = range(0, len(self.names))

        # plot differently if a single index or a list is passed
        # loop through each item to plot
        if type(inds) is list:
            for i in inds:
                plt.plot(self.band_centers, self.spectra[i, :], label=self.names[i])
        else:
            plt.plot(self.band_centers, self.spectra[inds, :], label=self.names[inds])

        # add the legend with each spectrum's name
        if legend:
            plt.legend(fontsize="small", framealpha=0.5, fancybox=True)

        # display the plot
        plt.tight_layout()
        plt.show()

        return plt

    def bn(self, inds=None):
        """
        Brightness normalizes the spectra

        :param inds: the band indices to use for normalization
        :return none: updates the self.spectra array
        """
        # check if indices were set and valid. if not, use all bands
        if inds:
            if max(inds) > self.spectra.shape[-1]:
                inds = range(0, self.spectra.shape[-1])
                print("Invalid range set. using all spectra")
            if min(inds) < 0:
                inds = range(0, self.spectra.shape[-1])
                print("Invalid range set. using all spectra")
        else:
            inds = range(0, self.spectra.shape[-1])

        # perform the bn
        self.spectra = self.spectra[:, inds] / np.expand_dims(
            np.sqrt((self.spectra[:, inds] ** 2).sum(1)), 1
        )

        # subset band centers to the indices selected, if they exist
        if self.band_centers.ndim != 0:
            self.band_centers = self.band_centers[inds]

    def write_sli(self, path, row_inds=None, spectral_inds=None):
        """
        Writes the spectral object to an ENVI spectral library file

        :param path: the output file to write the array to
        :param inds: the row-wise indices of the array to write out
        :return none: writes the data to disk
        """
        # set up the output file names for the library and the header
        base, ext = os.path.splitext(path)
        if ext.lower() == ".sli":
            osli = path
            ohdr = "{}.hdr".format(base)
        elif ext.lower() == ".hdr":
            osli = "{}.hdr".format(base)
            ohdr = path
        else:
            osli = "{}.sli".format(base)
            ohdr = "{}.hdr".format(base)

        # subset the data if specific indices are set
        spectra = self.spectra
        names = self.names
        band_centers = self.band_centers

        if row_inds is not None:
            spectra = spectra[row_inds, :]
            names = np.array(names)[row_inds]

        if spectral_inds is not None:
            spectra = spectra[:, spectral_inds]
            band_centers = band_centers[spectral_inds]

        # set up the metadata for the ENVI header file
        metadata = {
            "samples": len(band_centers),
            "lines": len(names),
            "bands": 1,
            "data type": 4,
            "header offset": 0,
            "interleave": "bsq",
            "byte order": 0,
            "sensor type": "ccblc",
            "spectra names": names,
            "wavelength units": self.band_unit,
            "wavelength": band_centers,
        }
        spectral.envi.write_envi_header(ohdr, metadata, is_library=True)

        # then write the spectral library
        with open(osli, "w") as f:
            spectra.astype(np.float32).tofile(f)
