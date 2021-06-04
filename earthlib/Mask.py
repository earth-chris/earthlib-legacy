"""Functions for masking earth engine images."""

import ee as _ee


def Landsat8(img):
    """Masks Landsat8 images.

    Args:
        img: the ee.Image to mask. Must have a Landsat "pixel_qa" band.

    Returns:
        img: the same input image with an updated mask.
    """

    cloudShadowBitMask = _ee.Number(2).pow(3).int()
    cloudsBitMask = _ee.Number(2).pow(5).int()
    qa = img.select("pixel_qa")
    mask = (
        qa.bitwiseAnd(cloudShadowBitMask).eq(0).And(qa.bitwiseAnd(cloudsBitMask).eq(0))
    )
    return img.mask(mask)


def Sentinel2(img):
    """Masks Sentinel2 images.

    Args:
        img: the ee.Image to mask. Must have a Sentinel "QA60" band.

    Returns:
        img: the same input image with an updated mask.
    """

    cirrusBitMask = _ee.Number(2).pow(11).int()
    cloudsBitMask = _ee.Number(2).pow(10).int()
    qa = img.select("QA60")
    mask = qa.bitwiseAnd(cloudsBitMask).eq(0).And(qa.bitwiseAnd(cirrusBitMask).eq(0))
    return img.updateMask(mask)


def MODIS(img):
    """Masks MODIS images.

    Args:
        img: the ee.Image to mask. Must have a MODIS "state_1km" band.

    Returns:
        img: the same input image with an updated mask.
    """

    cloudShadowBitMask = _ee.Number(2).pow(2).int()
    cloudsBitMask = _ee.Number(2).pow(0).int()
    qa = img.select("state_1km")
    mask = (
        qa.bitwiseAnd(cloudShadowBitMask).eq(0).And(qa.bitwiseAnd(cloudsBitMask).eq(0))
    )
    return img.mask(mask)


def bySensor(sensor):
    """Returns the appropriate mask function to use by sensor type.

    Args:
        sensor: string with the sensor name to return (e.g. "Landsat8", "Sentinel2").

    Returns:
        function: the mask function associated with a sensor to pass to an ee .map() call
    """
    lookup = {
        "Landsat8": Landsat8,
        "Sentinel2": Sentinel2,
        "MODIS": MODIS,
    }
    function = lookup[sensor]
    return function
