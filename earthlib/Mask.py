"""Functions for masking earth engine images."""


def Landsat8(img):
    import ee

    cloudShadowBitMask = ee.Number(2).pow(3).int()
    cloudsBitMask = ee.Number(2).pow(5).int()
    qa = img.select("pixel_qa")
    mask = (
        qa.bitwiseAnd(cloudShadowBitMask).eq(0).And(qa.bitwiseAnd(cloudsBitMask).eq(0))
    )
    return img.mask(mask)


def Sentinel2(img):
    import ee

    cirrusBitMask = ee.Number(2).pow(11).int()
    cloudsBitMask = ee.Number(2).pow(10).int()
    qa = img.select("QA60")
    mask = qa.bitwiseAnd(cirrusBitMask).eq(0).And(qa.bitwiseAnd(cloudsBitMask).eq(0))
    return img.mask(mask)


def MODIS(img):
    import ee

    cloudShadowBitMask = ee.Number(2).pow(2).int()
    cloudsBitMask = ee.Number(2).pow(0).int()
    qa = img.select("state_1km")
    mask = (
        qa.bitwiseAnd(cloudShadowBitMask).eq(0).And(qa.bitwiseAnd(cloudsBitMask).eq(0))
    )
    return img.mask(mask)


def bySensor(sensor):
    """
    Returns the appropriate mask function to use by sensor type.

    :param sensor:
    :return function: the mask function associated with a sensor to pass to an ee .map() call
    """
    lookup = {
        "Landsat8": Landsat8,
        "Sentinel2": Sentinel2,
        "MODIS": MODIS,
    }
    function = lookup[sensor]
    return function
