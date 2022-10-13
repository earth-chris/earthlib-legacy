"""Functions for shade masking earth engine images."""

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
    }
    try:
        function = lookup[sensor]
        return function
    except KeyError:
        supported = ", ".join(lookup.keys())
        raise SensorError(
            f"Shade masking not supported for '{sensor}'. Supported: {supported}"
        )


def shadeMask(img: ee.Image, threshold: float) -> ee.Image:
    """Use brightness normalization to identify and remove dark pixels.

    Args:
        img: the ee.Image to shade mask.
        threshold: the brightness/reflectance value to exclude.
            pixels below this value are flagged as shade.

    Returns:
        a pixel byte map with 0 for shade pixels, 1 for bright pixels.
    """
    brightness = img.reduce(ee.Reducer.mean())
    mask = brightness.gt(threshold)
    return mask


def Landsat457(img: ee.Image, threshold: float = 0.03) -> ee.Image:
    """Apply shade masking to a Landsat 4/5/7 image.

    Args:
        img: the ee.Image to shade mask.
        threshold: the brightness/reflectance value to exclude.
            pixels below this value are flagged as shade.

    Returns:
        the same input image with an updated mask.
    """
    subset = img.select(getBands("Landsat7"))
    shade = shadeMask(subset, threshold)
    return img.updateMask(shade)


def Landsat8(img: ee.Image, threshold: float = 0.03) -> ee.Image:
    """Apply shade masking to a Landsat 8 image.

    Args:
        img: the ee.Image to shade mask.
        threshold: the brightness/reflectance value to exclude.
            pixels below this value are flagged as shade.

    Returns:
        the same input image with an updated mask.
    """
    subset = img.select(getBands("Landsat8"))
    shade = shadeMask(subset, threshold)
    return img.updateMask(shade)
