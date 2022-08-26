"""Methods for scaling image data to normalized reflectance values (0-1 float)"""

from typing import Callable

import ee

from earthlib.config import collections


def bySensor(sensor: str) -> Callable:
    """Returns the appropriate scaling function to use by sensor type.

    Args:
        sensor: string with the sensor name to return (e.g. "Landsat8", "Sentinel2").

    Returns:
        the scale function associated with a sensor to pass to an ee .map() call
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
        "NEON": NEON,
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
            f"Scaling adjustment not supported for '{sensor}'. Supported: {supported}"
        )


def Landsat4(image: ee.Image) -> ee.Image:
    """Transform Landsat4 image data to scaled reflectance values"""
    sensor = "Landsat4"
    scale, offset = getScaleParams(sensor)
    return scaleWrapper(image, scale, offset)


def Landsat5(image: ee.Image) -> ee.Image:
    """Transform Landsat5 image data to scaled reflectance values"""
    sensor = "Landsat5"
    scale, offset = getScaleParams(sensor)
    return scaleWrapper(image, scale, offset)


def Landsat7(image: ee.Image) -> ee.Image:
    """Transform Landsat7 image data to scaled reflectance values"""
    sensor = "Landsat7"
    scale, offset = getScaleParams(sensor)
    return scaleWrapper(image, scale, offset)


def Landsat8(image: ee.Image) -> ee.Image:
    """Transform Landsat8 image data to scaled reflectance values"""
    sensor = "Landsat8"
    scale, offset = getScaleParams(sensor)
    return scaleWrapper(image, scale, offset)


def Sentinel2(image: ee.Image) -> ee.Image:
    """Transform Sentinel2 image data to scaled reflectance values"""
    sensor = "Sentinel2"
    scale, offset = getScaleParams(sensor)
    return scaleWrapper(image, scale, offset)


def MODIS(image: ee.Image) -> ee.Image:
    """Transform MODIS image data to scaled reflectance values"""
    sensor = "MODIS"
    scale, offset = getScaleParams(sensor)
    return scaleWrapper(image, scale, offset)


def VIIRS(image: ee.Image) -> ee.Image:
    """Transform VIIRS image data to scaled reflectance values"""
    sensor = "VIIRS"
    scale, offset = getScaleParams(sensor)
    return scaleWrapper(image, scale, offset)


def ASTER(image: ee.Image) -> ee.Image:
    """Transform ASTER image data to scaled reflectance values"""
    sensor = "ASTER"
    scale, offset = getScaleParams(sensor)
    return scaleWrapper(image, scale, offset)


def AVNIR2(image: ee.Image) -> ee.Image:
    """Transform ALOS-AVNIR2 image data to scaled reflectance values"""
    sensor = "AVNIR2"
    scale, offset = getScaleParams(sensor)
    return scaleWrapper(image, scale, offset)


def NEON(image: ee.Image) -> ee.Image:
    """Transform NEON image data to scaled reflectance values"""
    sensor = "NEON"
    scale, offset = getScaleParams(sensor)
    return scaleWrapper(image, scale, offset)


def DoveR(image: ee.Image) -> ee.Image:
    """Transform Planet Dove-R image data to scaled reflectance values"""
    sensor = "DoveR"
    scale, offset = getScaleParams(sensor)
    return scaleWrapper(image, scale, offset)


def SuperDove(image: ee.Image) -> ee.Image:
    """Transform Planet SuperDove image data to scaled reflectance values"""
    sensor = "SuperDove"
    scale, offset = getScaleParams(sensor)
    return scaleWrapper(image, scale, offset)


def PlanetScope(image: ee.Image) -> ee.Image:
    """Transform PlanetScope image data to scaled reflectance values"""
    sensor = "PlanetScope"
    scale, offset = getScaleParams(sensor)
    return scaleWrapper(image, scale, offset)


def getScaleParams(sensor: str) -> tuple:
    """Look-up the scale and offset values for a sensor"""
    scale = collections[sensor].get("scale", 1)
    offset = collections[sensor].get("offset", 0)
    return scale, offset


def scaleWrapper(image: ee.Image, scale: float = 1, offset: float = 0) -> ee.Image:
    """Apply image rescaling and offset adjustments

    Args:
        image: the input image object
        scale: the image rescaling factor
        offset: the image offset factor

    Returns:
        the input rescaled as a 0-1 floating point image
    """
    scaled = image.multiply(scale).add(offset)
    return scaled.toFloat()
