"""Functions for masking earth engine images."""

from typing import Callable

import ee

from earthlib.errors import SensorError


def bitwiseSelect(img: ee.Image, fromBit: int, toBit: int = None) -> ee.Image:
    """Filter QA bit masks.

    Args:
        img: the QA band image
        fromBit: QA start bit
        toBit: QA end bit

    Returns:
        encoded bitmap for the passed QA bits
    """
    toBit = fromBit if toBit is None else toBit
    size = ee.Number(1).add(toBit).subtract(fromBit)
    mask = ee.Number(1).leftShift(size).subtract(1)
    return img.rightShift(fromBit).bitwiseAnd(mask)


def bySensor(sensor: str) -> Callable:
    """Returns the appropriate mask function to use by sensor type.

    Args:
        sensor: string with the sensor name to return (e.g. "Landsat8", "Sentinel2").

    Returns:
        the mask function associated with a sensor to pass to an ee .map() call
    """
    lookup = {
        "Landsat4": Landsat4578,
        "Landsat5": Landsat4578,
        "Landsat7": Landsat4578,
        "Landsat8": Landsat4578,
        "Sentinel2": Sentinel2,
        "MODIS": MODIS,
        "VIIRS": VIIRS,
    }
    try:
        function = lookup[sensor]
        return function
    except KeyError:
        supported = ", ".join(lookup.keys())
        raise SensorError(
            f"Cloud masking not supported for '{sensor}'. Supported: {supported}"
        )


def Landsat4578_new(img: ee.Image) -> ee.Image:
    """Cloud-masks Landsat images.

    See https://gis.stackexchange.com/questions/349371/creating-cloud-free-images-out-of-a-mod09a1-modis-image-in-gee
    Previously: https://gis.stackexchange.com/questions/425159/how-to-make-a-cloud-free-composite-for-landsat-8-collection-2-surface-reflectanc/425160#425160

    Args:
        img: the ee.Image to mask. Must have a Landsat "QA_PIXEL" band.

    Returns:
        the same input image with an updated mask.
    """
    qa = img.select("QA_PIXEL")
    sat = img.select("QA_RADSAT")

    qaDilatedCloud = bitwiseSelect(qa, 1).eq(0)
    qaCloudShadow = bitwiseSelect(qa, 4).eq(0)
    qaSnow = bitwiseSelect(qa, 5).eq(0)
    qaMask = qaDilatedCloud.And(qaCloudShadow).And(qaSnow)

    satMask = sat.eq(0)
    jointMask = qaMask.And(satMask)

    return img.updateMask(jointMask)


def Landsat4578(img: ee.Image) -> ee.Image:
    """Cloud-masks Landsat images.

    See https://gis.stackexchange.com/questions/425159/how-to-make-a-cloud-free-composite-for-landsat-8-collection-2-surface-reflectanc/425160#425160

    Args:
        img: the ee.Image to mask. Must have a Landsat "QA_PIXEL" band.

    Returns:
        the same input image with an updated mask.
    """
    qa = img.select("QA_PIXEL")
    sat = img.select("QA_RADSAT")

    qamask = qa.bitwiseAnd(int("111111", 2)).eq(0)
    satmask = sat.eq(0)

    return img.updateMask(qamask).updateMask(satmask)


def Sentinel2(img: ee.Image) -> ee.Image:
    """Masks Sentinel2 images.

    Args:
        img: the ee.Image to mask. Must have a Sentinel "QA60" band.

    Returns:
        the same input image with an updated mask.
    """
    qa = img.select("QA60")

    cirrusBit = ee.Number(2).pow(11).int()
    cloudsBit = ee.Number(2).pow(10).int()

    cirrusMask = qa.bitwiseAnd(cloudsBit).eq(0)
    cloudsMask = qa.bitwiseAnd(cirrusBit).eq(0)

    mask = cirrusMask.And(cloudsMask)

    return img.updateMask(mask)


def MODIS(img: ee.Image) -> ee.Image:
    """Masks MODIS images.

    Args:
        img: the ee.Image to mask. Must have a MODIS "state_1km" band.

    Returns:
        the same input image with an updated mask.
    """
    qa = img.select("state_1km")

    cloudShadowBit = ee.Number(2).pow(2).int()
    cloudBit = ee.Number(2).pow(0).int()

    cloudShadowMask = qa.bitwiseAnd(cloudShadowBit).eq(0)
    cloudMask = qa.bitwiseAnd(cloudBit).eq(0)

    mask = cloudShadowMask.And(cloudMask)

    return img.mask(mask)


def VIIRS(img: ee.Image) -> ee.Image:
    """Masks VIIRS images.

    Args:
        img: the ee.Image to mask. Must have "QF1" and "QF2" bands.

    Returns:
        the same input image with an updated mask.
    """
    qa1 = img.select("QF1")
    qa2 = img.select("QF2")

    clearBit = ee.Number(2).pow(2).int()
    dayBit = ee.Number(2).pow(4).int()
    shadowBit = ee.Number(2).pow(3).int()
    snowBit = ee.Number(2).pow(5).int()
    cirrus1Bit = ee.Number(2).pow(6).int()
    cirrus2Bit = ee.Number(2).pow(7).int()

    clearMask = qa1.bitwiseAnd(clearBit).eq(0)
    dayMask = qa1.bitwiseAnd(dayBit).eq(0)
    shadowMask = qa2.bitwiseAnd(shadowBit).eq(0)
    snowMask = qa2.bitwiseAnd(snowBit).eq(0)
    cirrus1Mask = qa2.bitwiseAnd(cirrus1Bit).eq(0)
    cirrus2Mask = qa2.bitwiseAnd(cirrus2Bit).eq(0)

    mask = (
        clearMask.And(dayMask)
        .And(shadowMask)
        .And(snowMask)
        .And(cirrus1Mask)
        .And(cirrus2Mask)
    )

    return img.mask(mask)
