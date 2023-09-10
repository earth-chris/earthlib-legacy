"""Functions for brightness masking earth engine images."""

from typing import Callable

import ee

from earthlib.errors import SensorError
from earthlib.utils import getBands


def bySensor(sensor: str) -> Callable:
    """Returns the appropriate shade mask function to use by sensor type.

    Args:
        sensor: string with the sensor name to return (e.g. "Landsat8", "Sentinel2").

    Returns:
        the mask function associated with a sensor to pass to an ee .map() call
    """
    lookup = {
        "Landsat4": Landsat457,
        "Landsat5": Landsat457,
        "Landsat7": Landsat457,
        "Landsat8": Landsat8,
        "MODIS": MODIS,
    }
    try:
        function = lookup[sensor]
        return function
    except KeyError:
        supported = ", ".join(lookup.keys())
        raise SensorError(
            f"Shade masking not supported for '{sensor}'. Supported: {supported}"
        )


def brightMask(img: ee.Image, threshold: float) -> ee.Image:
    """Use brightness normalization to identify and remove bright pixels.

    Args:
        img: the ee.Image to shade mask.
        threshold: the brightness/reflectance value to exclude.
            pixels above this value are flagged as bright.

    Returns:
        a pixel byte map with 0 for shade pixels, 1 for bright pixels.
    """
    brightness = img.reduce(ee.Reducer.mean())
    mask = brightness.lt(threshold)
    return mask


def Landsat457(img: ee.Image, threshold: float = 0.4) -> ee.Image:
    """Apply bright pixel masking to a Landsat 4/5/7 image.

    Args:
        img: the ee.Image to shade mask.
        threshold: the brightness/reflectance value to exclude.
            pixels above this value are flagged as bright.

    Returns:
        the same input image with an updated mask.
    """
    # remove SWIR2 band where most ground/cloud confusion occurs
    bands = getBands("Landsat7")
    bands.remove("SR_B7")
    subset = img.select()
    shade = brightMask(subset, threshold)
    return img.updateMask(shade)


def Landsat8(img: ee.Image, threshold: float = 0.4) -> ee.Image:
    """Apply bright pixel masking to a Landsat 8 image.

    Args:
        img: the ee.Image to shade mask.
        threshold: the brightness/reflectance value to exclude.
            pixels above this value are flagged as bright.

    Returns:
        the same input image with an updated mask.
    """
    bands = getBands("Landsat8")
    bands.remove("SR_B7")
    subset = img.select(bands)
    shade = brightMask(subset, threshold)
    return img.updateMask(shade)


def MODIS(img: ee.Image, threshold: float = 0.4) -> ee.Image:
    """Apply bright pixel masking to a MODIS image.

    Args:
        img: the ee.Image to shade mask.
        threshold: the brightness/reflectance value to exclude.
            pixels above this value are flagged as bright.

    Returns:
        the same input image with an updated mask.
    """
    bands = getBands("MODIS")
    bands.remove("sur_refl_b07")
    subset = img.select(bands)
    shade = brightMask(subset, threshold)
    return img.updateMask(shade)
