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
        "Landsat4": Landsat4,
        "Landsat5": Landsat5,
        "Landsat7": Landsat7,
        "Landsat8": Landsat8,
        "Sentinel2": Sentinel2,
    }
    try:
        function = lookup[sensor]
        return function
    except KeyError:
        supported = ", ".join(lookup.keys())
        raise SensorError(
            f"BRDF adjustment not supported for '{sensor}'. Supported: {supported}"
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


def getScaleParams(sensor: str) -> tuple:
    """Look-up the scale and offset values for a sensor"""
    scale = collections[sensor].pop("scale", None)
    offset = collections[sensor].pop("offset", None)
    return scale, offset


def scaleWrapper(image: ee.Image, scale: float, offset: float = None) -> ee.Image:
    """Apply image rescaling and offset adjustments

    Args:
        image: the input image object
        scale: the image rescaling factor
        offset: the image offset factor

    Returns:
        the input rescaled as a 0-1 floating point image
    """
    scaled = image.multiply(scale).add(offset) if offset else image.multiply(scale)
    return scaled.toFloat()
