import random

import ee

from earthlib import utils

sensor = "Sentinel2"
band = "B8"
dtype = "vegetation"
random_str = "{num:06d}.xyz".format(num=random.randint(1e6, 1e7 - 1))


def test_listSensors():
    sensors = utils.listSensors()
    assert sensor in sensors
    assert random_str not in sensors


def test_listTypes():
    types = utils.listTypes()
    assert dtype in types
    assert random_str not in types


def test_getTypeLevel():
    valid_level = utils.getTypeLevel(dtype)
    assert valid_level == 2

    invalid_level = utils.getTypeLevel(random_str)
    assert invalid_level == 0


def test_getCollectionName():
    assert "COPERNICUS" in utils.getCollectionName(sensor)


def test_getScaler():
    assert utils.getScaler(sensor) == 0.0001


def test_getBands():
    assert band in utils.getBands(sensor)


def test_getBandIndices():
    assert 6 in utils.getBandIndices([band], sensor)
    assert 6 in utils.getBandIndices(band, sensor)


def test_selectSpectra():
    n = 20
    all_spectra = utils.selectSpectra(dtype, sensor, n=0)
    some_spectra = utils.selectSpectra(dtype, sensor, n)
    assert len(all_spectra) > 1000
    assert len(some_spectra) == n
