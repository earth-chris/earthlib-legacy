"""Functions for cloud masking earth engine images."""

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
    """Returns the appropriate cloud mask function to use by sensor type.

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


def Landsat4578(img: ee.Image) -> ee.Image:
    """Cloud-masks Landsat images.

    See https://gis.stackexchange.com/questions/349371/creating-cloud-free-images-out-of-a-mod09a1-modis-image-in-gee
    Previously: https://gis.stackexchange.com/questions/425159/how-to-make-a-cloud-free-composite-for-landsat-8-collection-2-surface-reflectanc/425160

    Args:
        img: the ee.Image to mask. Must have a Landsat "QA_PIXEL" band.

    Returns:
        the same input image with an updated mask.
    """
    qa = img.select("QA_PIXEL")
    sat = img.select("QA_RADSAT")

    dilatedCloud = bitwiseSelect(qa, 1).eq(0)
    cirrus = bitwiseSelect(qa, 2).eq(0)
    cloud = bitwiseSelect(qa, 3).eq(0)
    cloudShadow = bitwiseSelect(qa, 4).eq(0)
    snow = bitwiseSelect(qa, 5).eq(0)
    qaMask = dilatedCloud.And(cirrus).And(cloud).And(cloudShadow).And(snow)

    satMask = sat.eq(0)
    jointMask = qaMask.And(satMask)

    return img.updateMask(jointMask)


def Sentinel2QA(img: ee.Image) -> ee.Image:
    """Masks Sentinel2 images using the QA band.

    Args:
        img: the ee.Image to mask. Must have a Sentinel "QA60" band.

    Returns:
        the same input image with an updated mask.
    """
    qa = img.select("QA60")
    cloud = bitwiseSelect(qa, 10).eq(0)
    cirrus = bitwiseSelect(qa, 11).eq(0)
    mask = cloud.And(cirrus)

    return img.updateMask(mask)


def Sentinel2SCL(img: ee.Image) -> ee.Image:
    """Masks Sentinel2 images using scene classification labels.

    Args:
        img: the ee.Image to mask. Must have a Sentinel "SCL" class band.

    Returns:
        the same input image with an updated mask.
    """
    scl = img.select("SCL")

    # class labels
    sat = scl.neq(1)
    shadow = scl.neq(3)
    cloudLow = scl.neq(7)
    cloudMed = scl.neq(8)
    cloudHigh = scl.neq(9)
    cirrus = scl.neq(10)
    bareSoil = scl.eq(5)
    baseMask = sat.And(shadow).And(cloudLow).And(cloudMed).And(cloudHigh).And(cirrus)

    # apply morphological closing to clean up one/two pixel cloud predictions
    cleanupKernel = ee.Kernel.circle(2)
    focalOpts = {"kernel": cleanupKernel, "iterations": 1}
    erodedMask = baseMask.focalMax(**focalOpts).focalMin(**focalOpts)

    # include a search radius to include false positive bare soil predictions near clouds
    euclidean = ee.Kernel.euclidean(1000, "meters")
    distToCloud = erodedMask.subtract(1).distance(euclidean).unmask()
    notBare = ee.Image(1).subtract(bareSoil.And(distToCloud.lte(100)))
    cloudBareMask = erodedMask.And(notBare)

    return img.updateMask(cloudBareMask)


def Sentinel2(img: ee.Image, use_qa: bool = True, use_scl: bool = True) -> ee.Image:
    """Mask Sentinel2 images using multiple masking approaches.

    Args:
        img: the ee.Image to mask.
        use_qa: apply QA band cloud masking. img must have a "QA60" band.
        use_scl: apply SCL band cloud masking. img must have a "SCL" band.

    Returns:
        the same input image with an updated mask.
    """
    if use_qa:
        img = Sentinel2QA(img)

    if use_scl:
        img = Sentinel2SCL(img)

    return img


def MODIS(img: ee.Image) -> ee.Image:
    """Dummy function for MODIS images.

    This function just returns the original image because the MODIS collection
        already applies a cloud mask to all pixels. It only exists so as to
        not break other processing chains that use .bySensor() methods.

    Args:
        img: an ee.Image.

    Returns:
        the input image.
    """
    return img


def VIIRS(img: ee.Image) -> ee.Image:
    """Masks VIIRS images.

    Args:
        img: the ee.Image to mask. Must have "QF1" and "QF2" bands.

    Returns:
        the same input image with an updated mask.
    """
    qf1 = img.select("QF1")
    qf2 = img.select("QF2")
    qf7 = img.select("QF7")

    clearMask = bitwiseSelect(qf1, 2, 3).eq(0)
    dayMask = bitwiseSelect(qf1, 4).eq(0)
    shadowMask = bitwiseSelect(qf2, 3).eq(0)
    snowMask = bitwiseSelect(qf2, 5).eq(0)
    cirrus1Mask = bitwiseSelect(qf2, 6).eq(0)
    cirrus2Mask = bitwiseSelect(qf2, 7).eq(0)
    adjacentMask = bitwiseSelect(qf7, 1).eq(0)
    thinCirrusMask = bitwiseSelect(qf7, 4).eq(0)

    mask = (
        clearMask.And(dayMask)
        .And(shadowMask)
        .And(snowMask)
        .And(cirrus1Mask)
        .And(cirrus2Mask)
        .And(adjacentMask)
        .And(thinCirrusMask)
    )

    return img.updateMask(mask)


def Opening(img: ee.Image, iterations: int = 3) -> ee.Image:
    """Apply a morphological opening filter to an image mask.

    Args:
        img: the ee.Image to mask. Must have a mask band set.
        iterations: the number of sequential dilate/erode operations.

    Returns:
        the input image with an updated, opened mask.
    """
    mask = img.mask()
    kernel = ee.Kernel.circle(iterations)
    dilateOpts = {"kernel": kernel, "iterations": iterations}
    erodeOpts = {"kernel": kernel, "iterations": iterations}
    openedMask = mask.focalMin(**dilateOpts).focalMax(**erodeOpts)

    return img.updateMask(openedMask)
