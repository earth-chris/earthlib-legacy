"""Utility functions for working with spectral libraries and earth engine routines."""

import os
from warnings import warn

import ee
import numpy as np
import spectral

from earthlib.config import collections, endmember_path, metadata
from earthlib.errors import SensorError
from earthlib.read import spectralLibrary


def listSensors() -> list:
    """Returns a list of the supported sensor image collections.

    Returns:
        sensors: a list of supported sensors using the names referenced by this package.
    """
    sensors = list(collections.keys())
    return sensors


def validateSensor(sensor: str) -> None:
    """Verify a string sensor ID is valid, raise an error otherwise.

    Args:
        sensor: the name of the sensor (from earthlib.listSensors()).

    Raises:
        SensorError: when an invalid sensor name is passed
    """
    supported = listSensors()
    if sensor not in supported:
        raise SensorError(
            f"Invalid sensor: {sensor}. Supported: {', '.join(supported)}"
        )


def listTypes(level: int = 2) -> list:
    """Returns a list of the spectral classification types.

    Args:
        level: the level of spectral classification specificity to return. Supports integers 1-4.

    Returns:
        classes: a list of spectral data types referenced throughout this package.
    """
    key = f"LEVEL_{level}"
    types = list(metadata[key].unique())
    return types


def getTypeLevel(Type: str) -> int:
    """Checks whether a spectral data type is available in the endmember library.

    Args:
        Type: the type of spectra to select.

    Returns:
        level: the metadata "level" of the group for subsetting. returns 0 if not found.
    """
    for i in range(4):
        level = i + 1
        available_types = listTypes(level=level)
        if Type in available_types:
            return level

    return 0


def getCollectionName(sensor: str) -> str:
    """Returns the earth engine collection name for a specific satellite sensor.

    Args:
        sensor: the name of the sensor (from earthlib.listSensors()).

    Returns:
        collection: a string with the earth engine collection.
    """
    validateSensor(sensor)
    collection = collections[sensor]["collection"]
    return collection


def getCollection(sensor: str) -> ee.ImageCollection:
    """Returns the default image collection for a satellite sensor.

    Args:
        sensor: the name of the sensor (from earthlib.listSensors()).

    Returns:
        that sensor's ee image collection.
    """
    return ee.ImageCollection(getCollectionName(sensor))


def getScaler(sensor: str) -> str:
    """Returns the scaling factor to convert sensor data to percent reflectance (0-1).

    Args:
        sensor: the name of the sensor (from earthlib.listSensors()).

    Returns:
        scaler: the scale factor to multiply.
    """
    validateSensor(sensor)
    scaler = collections[sensor]["scale"]
    return scaler


def getBands(sensor: str) -> list:
    """Returns a list of available band names by sensor.

    Args:
        sensor: the name of the sensor (from earthlib.listSensors()).

    Returns:
        bands: a list of sensor-specific band names.
    """
    validateSensor(sensor)
    bands = collections[sensor]["band_names"]
    return bands


def getBandDescriptions(sensor: str) -> list:
    """Returns a list band name descriptions by sensor.

    Args:
        sensor: the name of the sensor (from earthlib.listSensors()).

    Returns:
        bands: a list of sensor-specific band names.
    """
    validateSensor(sensor)
    bands = collections[sensor]["band_descriptions"]
    return bands


def getBandIndices(custom_bands: list, sensor: str) -> list:
    """Cross-references a list of bands passed as strings to the 0-based integer indices

    Args:
        custom_bands: a list of band names.
        sensor: a string sensor type for indexing the supported collections.

    Returns:
        indices: list of integer band indices.
    """
    validateSensor(sensor)
    sensor_bands = collections[sensor]["band_names"]
    indices = list()

    if type(custom_bands) in (list, tuple):
        for band in custom_bands:
            if band in sensor_bands:
                indices.append(sensor_bands.index(band))

    elif type(custom_bands) == str:
        indices.append(sensor_bands.index(custom_bands))

    indices.sort()
    return indices


def selectSpectra(Type: str, sensor: str, n: int = 20, bands: list = None) -> list:
    """Subsets the earthlib spectral endmember library.

    Selects endmembers from specific class, then resamples the spectra to the wavelengths
    of a specific satellite sensor. This also performs random spectra selection.

    Args:
        Type: the type of spectra to select (from earthlib.listTypes()).
        sensor: the sensor type to resample wavelengths to.
        n: the number of random spectra to sample. n=0 returns all spectra.
        bands: list of bands to use. Accepts 0-based indices or a list of band names (e.g. ["B2", "B3", "B4"]).

    Returns:
        a list of spectral endmembers resampled to a specific sensor's wavelengths.
    """
    validateSensor(sensor)

    # get the level of the group selected
    level = getTypeLevel(Type)
    if level == 0:
        raise EndmemberError(
            f"Invalid group parameter: {Type}. Get valid values from earthlib.listTypes()."
        )

    # read the spectral library into memory
    endmembers = spectralLibrary(endmember_path)

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
