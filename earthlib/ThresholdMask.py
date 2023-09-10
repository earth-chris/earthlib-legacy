"""Functions for cloud masking earth engine images based on band thresholds."""

from typing import Callable

import ee

from earthlib.errors import SensorError


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


def Landsat457(img: ee.Image, probability_threshold: float = 0.4) -> ee.Image:
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


def Landsat8(img: ee.Image, probability_threshold: float = 0.4) -> ee.Image:
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


def MODIS(img: ee.Image, probability_threshold: float = 0.6) -> ee.Image:
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


def VIIRS(img: ee.Image, probability_threshold: float = 0.4) -> ee.Image:
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
