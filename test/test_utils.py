import random

from earthlib import utils

random_str = "{num:06d}.xyz".format(num=random.randint(1e6, 1e7 - 1))
sensor = "Sentinel2"
band = "B8"
dtype = "vegetation"


def test_checkFile_exists():
    assert utils.checkFile(__file__)
    assert not utils.checkFile(random_str)


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


def test_getCollection():
    assert "COPERNICUS" in utils.getCollection(sensor)


def test_getScaler():
    assert utils.getScaler(sensor) == 0.0001


def test_getBands():
    assert band in utils.getBands(sensor)


def test_getBandIndices():
    assert 6 in utils.getBandIndices([band], sensor)
    assert 6 in utils.getBandIndices(band, sensor)


def test_selectSpectra():
    n = 20
    all_spectra = utils.selectSpectra(dtype, sensor)
    some_spectra = utils.selectSpectra(dtype, sensor, n)
    assert len(all_spectra) > 1000
    assert len(some_spectra) == n


def test_spectralObject():
    n_spectra = 5
    s = utils.spectralObject(n_spectra, sensor="asd")
    assert len(s.spectra) == 5
    assert max(s.band_centers <= 2500)
    assert min(s.band_centers >= 350)

    s.remove_water_bands()
    assert 1400 not in s.band_centers
    assert 1300 in s.band_centers

    shortwave_bands = s.get_shortwave_bands()
    assert min(s.band_centers[shortwave_bands]) >= 350
    assert max(s.band_centers[shortwave_bands]) <= 2500
