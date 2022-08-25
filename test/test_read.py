import random

from earthlib import read


def test_Spectra():
    n_spectra = 5
    s = read.Spectra(n_spectra=n_spectra, instrument="asd")
    assert len(s.spectra) == 5
    assert max(s.band_centers <= 2500)
    assert min(s.band_centers >= 350)

    s.remove_water_bands()
    assert 1400 not in s.band_centers
    assert 1300 in s.band_centers

    shortwave_bands = s.get_shortwave_bands()
    assert min(s.band_centers[shortwave_bands]) >= 350
    assert max(s.band_centers[shortwave_bands]) <= 2500


def test_check_file():
    random_str = "{num:06d}.xyz".format(num=random.randint(1e6, 1e7 - 1))
    assert read.check_file(__file__)
    assert not read.check_file(random_str)
