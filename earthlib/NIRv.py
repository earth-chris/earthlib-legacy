"""Methods for computing NIRv (near infrared reflectance of vegetation) from ee.Image data"""

from typing import Callable

import ee

from earthlib.config import collections
from earthlib.utils import getBandDescriptions, getBands


def bySensor(sensor: str) -> Callable:
    """Returns the appropriate NIRv function to use by sensor type.

    Args:
        sensor: string with the sensor name to return (e.g. "Landsat8", "Sentinel2").

    Returns:
        the NIRv function associated with a sensor to pass to an ee .map() call
    """
    lookup = {
        "ASTER": ASTER,
        "AVNIR2": AVNIR2,
        "DoveR": DoveR,
        "Landsat4": Landsat4,
        "Landsat5": Landsat5,
        "Landsat7": Landsat7,
        "Landsat8": Landsat8,
        "MODIS": MODIS,
        "PlanetScope": PlanetScope,
        "Sentinel2": Sentinel2,
        "SuperDove": SuperDove,
        "VIIRS": VIIRS,
    }
    try:
        function = lookup[sensor]
        return function
    except KeyError:
        supported = ", ".join(lookup.keys())
        raise SensorError(
            f"NIRv calculation not supported for '{sensor}'. Supported: {supported}"
        )


def ASTER(image: ee.Image) -> ee.Image:
    """Transform ASTER image data to scaled reflectance values"""
    sensor = "ASTER"
    red, nir = getNIRvBands(sensor)
    return NIRvWrapper(image, red, nir)


def AVNIR2(image: ee.Image) -> ee.Image:
    """Transform ALOS-AVNIR2 image data to scaled reflectance values"""
    sensor = "AVNIR2"
    red, nir = getNIRvBands(sensor)
    return NIRvWrapper(image, red, nir)


def DoveR(image: ee.Image) -> ee.Image:
    """Transform Planet DoveR image data to scaled reflectance values"""
    sensor = "DoveR"
    red, nir = getNIRvBands(sensor)
    return NIRvWrapper(image, red, nir)


def Landsat4(image: ee.Image) -> ee.Image:
    """Transform Landsat4 image data to scaled reflectance values"""
    sensor = "Landsat4"
    red, nir = getNIRvBands(sensor)
    return NIRvWrapper(image, red, nir)


def Landsat5(image: ee.Image) -> ee.Image:
    """Transform Landsat5 image data to scaled reflectance values"""
    sensor = "Landsat5"
    red, nir = getNIRvBands(sensor)
    return NIRvWrapper(image, red, nir)


def Landsat7(image: ee.Image) -> ee.Image:
    """Transform Landsat7 image data to scaled reflectance values"""
    sensor = "Landsat7"
    red, nir = getNIRvBands(sensor)
    return NIRvWrapper(image, red, nir)


def Landsat8(image: ee.Image) -> ee.Image:
    """Transform Landsat8 image data to scaled reflectance values"""
    sensor = "Landsat8"
    red, nir = getNIRvBands(sensor)
    return NIRvWrapper(image, red, nir)


def MODIS(image: ee.Image) -> ee.Image:
    """Transform MODIS image data to scaled reflectance values"""
    sensor = "MODIS"
    red, nir = getNIRvBands(sensor)
    return NIRvWrapper(image, red, nir)


def PlanetScope(image: ee.Image) -> ee.Image:
    """Transform PlanetScope image data to scaled reflectance values"""
    sensor = "PlanetScope"
    red, nir = getNIRvBands(sensor)
    return NIRvWrapper(image, red, nir)


def Sentinel2(image: ee.Image) -> ee.Image:
    """Transform Sentinel2 image data to scaled reflectance values"""
    sensor = "Sentinel2"
    red, nir = getNIRvBands(sensor)
    return NIRvWrapper(image, red, nir)


def SuperDove(image: ee.Image) -> ee.Image:
    """Transform Planet SuperDove image data to scaled reflectance values"""
    sensor = "SuperDove"
    red, nir = getNIRvBands(sensor)
    return NIRvWrapper(image, red, nir)


def VIIRS(image: ee.Image) -> ee.Image:
    """Transform VIIRS image data to scaled reflectance values"""
    sensor = "VIIRS"
    red, nir = getNIRvBands(sensor)
    return NIRvWrapper(image, red, nir)


def getNIRvBands(sensor: str) -> tuple:
    """Look-up the red and near infrared bands for NIRv calculation"""
    bnames = getBands(sensor)
    descriptions = getBandDescriptions(sensor)
    idx_red = descriptions.index("red")
    idx_nir = descriptions.index("near infrared")
    red = bnames[idx_red]
    nir = bnames[idx_nir]
    return red, nir


def NIRvWrapper(image: ee.Image, red_band: str, nir_band: str) -> ee.Image:
    """Compute NIRv for an image.

    Args:
        image: the input image object.
        red_band: the name of the red band to use
        nir_band: the name of the near infrared band to use

    Returns:
        appends the input image with and "NIRv" band.
    """
    red = image.select(red_band)
    nir = image.select(nir_band)
    ndvi = (nir.subtract(red)).divide(nir.add(red))
    ndviScaled = ndvi.subtract(0.08)
    nirv = ndviScaled.multiply(nir).rename("NIRv")
    return image.addBands(nirv)
