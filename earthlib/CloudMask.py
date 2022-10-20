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
        "Landsat4": Landsat457,
        "Landsat5": Landsat457,
        "Landsat7": Landsat457,
        "Landsat8": Landsat8,
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


def Landsat457(
    img: ee.Image, use_qa: bool = True, use_thresholds: bool = True
) -> ee.Image:
    """Cloud-mask Landsat 4/5/7 images using multiple methods.

    Args:
        img: the ee.Image to mask.
        use_qa: mask with the Landsat QA band.
        use_thresholds: mask with a series of band thresholds.

    Returns:
        the same input image with an updated mask.
    """
    if use_qa:
        img = Landsat4578QA(img)

    if use_thresholds:
        img = Landsat457Threshold(img)

    return img


def Landsat8(
    img: ee.Image, use_qa: bool = True, use_thresholds: bool = True
) -> ee.Image:
    """Cloud-mask Landsat 8 images using multiple methods.

    Args:
        img: the ee.Image to mask. Must have a Landsat "QA_PIXEL" band.
        use_qa: mask with the Landsat QA band.
        use_thresholds: mask with a series of band thresholds.

    Returns:
        the same input image with an updated mask.
    """
    if use_qa:
        img = Landsat4578QA(img)

    if use_thresholds:
        img = Landsat8Threshold(img)

    return img


def Landsat4578QA(img: ee.Image) -> ee.Image:
    """Cloud-mask Landsat images based on the QA bands.

    See https://gis.stackexchange.com/questions/349371/creating-cloud-free-images-out-of-a-mod09a1-modis-image-in-gee
    Previously: https://gis.stackexchange.com/questions/425159/how-to-make-a-cloud-free-composite-for-landsat-8-collection-2-surface-reflectanc/425160

    Args:
        img: the ee.Image to mask. Must have Landsat "QA_PIXEL" and "QA_RADSAT" band.

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


def Landsat457Threshold(img: ee.Image, probability_threshold: float = 0.4) -> ee.Image:
    """Compute cloud probability using a series of band ratios and apply a mask threshold.

    See Sun & Tian 2017: https://www.sciencedirect.com/science/article/pii/S0924271616306189

    Args:
        img: the ee.Image to mask. Must have all the "SR_*" reflectance bands.
        probability_threshold: pixels above this threshold are included in the mask.

    Returns:
        the same input image with an updated mask.
    """
    # band specifications
    blue = img.select("SR_B1")
    green = img.select("SR_B2")
    red = img.select("SR_B3")
    nir = img.select("SR_B4")
    swir1 = img.select("SR_B5")
    swir2 = img.select("SR_B7")

    # single band thresholds
    s1 = blue.gt(0.2)
    s2 = green.gt(0.2)
    s3 = red.gt(0.21)
    s4 = swir1.gt(0.29)
    s5 = swir2.gt(0.25)

    # multi-band thresholds
    m3 = blue.gt(0.16).And(nir.gt(0.26))
    m4 = blue.gt(0.20).And(swir1.gt(0.20))
    m5 = green.gt(0.12).And(nir.gt(0.32))
    m6 = red.gt(0.14).And(nir.gt(0.35))
    m7 = nir.gt(0.40).And(swir1.gt(0.30))

    # band ratio
    ratio = swir1.divide(swir2)
    ratio_thresh = ratio.gt(0.91).And(ratio.lt(1.83))

    # merge and average the results
    stack = s1.addBands([s2, s3, s4, s5, m1, m2, m3, m4, m5, m6, m7, ratio_thresh])
    probability = stack.reduce(ee.Reducer.mean())
    mask = probability.lt(probability_threshold)

    return img.updateMask(mask)


def Landsat8Threshold(img: ee.Image, probability_threshold: float = 0.4) -> ee.Image:
    """Compute cloud probability using a series of band ratios and apply a mask threshold.

    See Sun & Tian 2017: https://www.sciencedirect.com/science/article/pii/S0924271616306189

    Args:
        img: the ee.Image to mask. Must have all the "SR_*" reflectance bands.
        probability_threshold: pixels above this threshold are included in the mask.

    Returns:
        the same input image with an updated mask.
    """
    # band specifications
    ultrablue = img.select("SR_B1")
    blue = img.select("SR_B2")
    green = img.select("SR_B3")
    red = img.select("SR_B4")
    nir = img.select("SR_B5")
    swir1 = img.select("SR_B6")
    swir2 = img.select("SR_B7")

    # single band thresholds
    s1 = blue.gt(0.2)
    s2 = green.gt(0.2)
    s3 = red.gt(0.21)
    s4 = swir1.gt(0.29)
    s5 = swir2.gt(0.25)

    # multi-band thresholds
    m1 = ultrablue.gt(0.24).And(nir.gt(0.26))
    m2 = ultrablue.gt(0.24).And(swir1.gt(0.20))
    m3 = blue.gt(0.16).And(nir.gt(0.26))
    m4 = blue.gt(0.20).And(swir1.gt(0.20))
    m5 = green.gt(0.12).And(nir.gt(0.32))
    m6 = red.gt(0.14).And(nir.gt(0.35))
    m7 = nir.gt(0.40).And(swir1.gt(0.30))

    # band ratio
    ratio = swir1.divide(swir2)
    ratio_thresh = ratio.gt(0.91).And(ratio.lt(1.83))

    # merge and average the results
    stack = s1.addBands([s2, s3, s4, s5, m1, m2, m3, m4, m5, m6, m7, ratio_thresh])
    probability = stack.reduce(ee.Reducer.mean())
    mask = probability.lt(probability_threshold)

    return img.updateMask(mask)


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


def Sentinel2QA(img: ee.Image) -> ee.Image:
    """Mask Sentinel2 images using the QA band.

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
    """Mask Sentinel2 images using scene classification labels.

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


def MODIS(img: ee.Image, use_qa: bool = True, use_thresholds: bool = True) -> ee.Image:
    """Mask MODIS images using multiple masking approaches.

    Args:
        img: the ee.Image to mask.
        use_qa: apply QA band cloud masking. img must have a "state_1km" band.
        use_thresholds: apply SCL band cloud masking. img must have a "SCL" band.

    Returns:
        the same input image with an updated mask.
    """
    if use_qa:
        img = MODISQA(img)

    if use_thresholds:
        img = MODISThreshold(img)

    return img


def MODISQA(img: ee.Image) -> ee.Image:
    """Mask MODIS images.

    Args:
        img: the ee.Image to mask.

    Returns:
        the same input image with an updated mask.
    """
    qa = img.select("state_1km")

    clearMask = bitwiseSelect(qa, 0, 1).eq(0)
    shadowMask = bitwiseSelect(qa, 2).eq(0)
    aerosolMask = bitwiseSelect(qa, 6, 7).lte(1)
    cirrusMask = bitwiseSelect(qa, 8, 9).eq(0)
    cloudMask = bitwiseSelect(qa, 10).eq(0)
    fireMask = bitwiseSelect(qa, 11).eq(0)
    snowMask = bitwiseSelect(qa, 15).eq(0)

    mask = (
        clearMask.And(shadowMask)
        .And(aerosolMask)
        .And(cirrusMask)
        .And(cloudMask)
        .And(fireMask)
        .And(snowMask)
    )
    return img.updateMask(mask)


def MODISThreshold(img: ee.Image, probability_threshold: float = 0.6) -> ee.Image:
    """Compute cloud probability using a series of band ratios and apply a mask threshold.

    See Sun & Tian 2017: https://www.sciencedirect.com/science/article/pii/S0924271616306189

    Args:
        img: the ee.Image to mask. Must have all the "sur_refl_b*" reflectance bands.
        probability_threshold: pixels above this threshold are included in the mask.

    Returns:
        the same input image with an updated mask.
    """
    # band specifications
    b1 = img.select("sur_refl_b01")
    b2 = img.select("sur_refl_b02")
    b3 = img.select("sur_refl_b03")
    b4 = img.select("sur_refl_b04")
    b5 = img.select("sur_refl_b05")
    b6 = img.select("sur_refl_b06")
    b7 = img.select("sur_refl_b07")

    # single band thresholds
    s1 = b1.gt(0.29)
    s2 = b3.gt(0.23)
    s3 = b4.gt(0.24)

    # multi-band thresholds
    m1 = b1.gt(0.28).And(b5.gt(0.24))
    m2 = b1.gt(0.28).And(b6.gt(0.16))
    m3 = b3.gt(0.28).And(b7.gt(0.08))

    # band ratios
    ratio = b2.divide(b1)
    ratio_thresh = ratio.gt(0.95).And(ratio.lt(1.15))

    # merge and average the results
    stack = s1.addBands([s2, s3, m1, m2, m3, ratio_thresh])
    probability = stack.reduce(ee.Reducer.mean())
    mask = probability.lt(probability_threshold)

    return img.updateMask(mask)


def VIIRS(img: ee.Image, use_qa: bool = True, use_thresholds: bool = True) -> ee.Image:
    """Mask VIIRS images using multiple masking approaches.

    Args:
        img: the ee.Image to mask.
        use_qa: mask with QA bands.
        use_thresholds: mask with a series of band thresholds.

    Returns:
        the same input image with an updated mask.
    """
    if use_qa:
        img = VIIRSQA(img)

    if use_thresholds:
        img = VIIRSThreshold(img)

    return img


def VIIRSQA(img: ee.Image) -> ee.Image:
    """Mask VIIRS images using QA bands.

    Args:
        img: the ee.Image to mask. Must have "QF1", "QF2" and "QF7" bands.

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


def VIIRSThreshold(img: ee.Image, probability_threshold: float = 0.4) -> ee.Image:
    """Compute cloud probability using a series of band ratios and apply a mask threshold.

    See Sun & Tian 2017: https://www.sciencedirect.com/science/article/pii/S0924271616306189

    Args:
        img: the ee.Image to mask. Must have all the "M*" reflectance bands.
        probability_threshold: pixels above this threshold are included in the mask.

    Returns:
        the same input image with an updated mask.
    """
    # band specifications
    b1 = img.select("M1")
    b2 = img.select("M2")
    b3 = img.select("M3")
    b4 = img.select("M4")
    b5 = img.select("M5")
    b6 = img.select("M6")
    b7 = img.select("M7")
    b8 = img.select("M8")

    # single band thresholds
    s1 = b1.gt(0.31)
    s2 = b2.gt(0.25)
    s3 = b3.gt(0.25)
    s4 = b4.gt(0.25)
    s5 = b5.gt(0.30)
    s6 = b7.gt(0.52)
    s7 = b8.gt(0.46)

    # multi-band thresholds
    m1 = b1.gt(0.29).And(b7.gt(0.30))
    m2 = b1.gt(0.29).And(b8.gt(0.22))
    m3 = b1.gt(0.31).And(b10.gt(0.08))
    m4 = b1.gt(0.29).And(b11.gt(0.12))
    m5 = b2.gt(0.27).And(b8.gt(0.22))
    m6 = b2.gt(0.72).And(b10.gt(0.14))
    m7 = b3.gt(0.23).And(b8.gt(0.24))
    m8 = b3.gt(0.16).And(b9.gt(0.08))

    # band ratios
    ratio1 = b6.divide(b4)
    ratio2 = b7.divide(b5)
    ratio1_thresh = ratio1.gt(0.12).And(ratio1.lt(0.48))
    ratio2_thresh = ratio2.gt(1.0).And(ratio2.lt(1.15))

    # merge and average the results
    stack = s1.addBands(
        [
            s2,
            s3,
            s4,
            s5,
            s6,
            s7,
            m1,
            m2,
            m3,
            m4,
            m5,
            m6,
            m7,
            m8,
            ratio1_thresh,
            ratio2_thresh,
        ]
    )
    probability = stack.reduce(ee.Reducer.mean())
    mask = probability.lt(probability_threshold)

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
