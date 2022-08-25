"""Functions for masking earth engine images."""

from typing import Callable

import ee

from earthlib.errors import SensorError


def Landsat8(img: ee.Image) -> ee.Image:
    """Masks Landsat8 images.

    Args:
        img: the ee.Image to mask. Must have a Landsat "pixel_qa" band.

    Returns:
        the same input image with an updated mask.
    """
    cloudShadowBitMask = ee.Number(2).pow(3).int()
    cloudsBitMask = ee.Number(2).pow(5).int()
    qa = img.select("pixel_qa")
    mask = (
        qa.bitwiseAnd(cloudShadowBitMask).eq(0).And(qa.bitwiseAnd(cloudsBitMask).eq(0))
    )
    return img.mask(mask)


def Sentinel2(img: ee.Image) -> ee.Image:
    """Masks Sentinel2 images.

    Args:
        img: the ee.Image to mask. Must have a Sentinel "QA60" band.

    Returns:
        the same input image with an updated mask.
    """
    cirrusBitMask = ee.Number(2).pow(11).int()
    cloudsBitMask = ee.Number(2).pow(10).int()
    qa = img.select("QA60")
    mask = qa.bitwiseAnd(cloudsBitMask).eq(0).And(qa.bitwiseAnd(cirrusBitMask).eq(0))
    return img.updateMask(mask)


def MODIS(img: ee.Image) -> ee.Image:
    """Masks MODIS images.

    Args:
        img: the ee.Image to mask. Must have a MODIS "state_1km" band.

    Returns:
        the same input image with an updated mask.
    """
    cloudShadowBitMask = ee.Number(2).pow(2).int()
    cloudsBitMask = ee.Number(2).pow(0).int()
    qa = img.select("state_1km")
    mask = (
        qa.bitwiseAnd(cloudShadowBitMask).eq(0).And(qa.bitwiseAnd(cloudsBitMask).eq(0))
    )
    return img.mask(mask)


def bySensor(sensor: str) -> Callable:
    """Returns the appropriate mask function to use by sensor type.

    Args:
        sensor: string with the sensor name to return (e.g. "Landsat8", "Sentinel2").

    Returns:
        the mask function associated with a sensor to pass to an ee .map() call
    """
    lookup = {
        "Landsat8": Landsat8,
        "Sentinel2": Sentinel2,
        "MODIS": MODIS,
    }
    try:
        function = lookup[sensor]
        return function
    except KeyError:
        supported = ", ".join(lookup.keys())
        raise SensorError(
            f"BRDF adjustment not supported for '{sensor}'. Supported: {supported}"
        )
