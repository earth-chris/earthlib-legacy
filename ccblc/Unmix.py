"""
Routines for performing spectral unmixing on earth engine images
"""


# this routine must be run before any of the specific unmixing routines are set
def setSensor(sensor):
    """
    Specifies the sensor to retrieve endmembers for.

    :param sensor: the name of the sensor (from ccblc.listSensors()).
    :return none: sets a series of global endmember variables
    """
    import ee
    from .utils import selectSpectra

    # set the number of unmixing iterations (we'll hardcode these numbers later, unfortunately)
    n = 30

    # get them as a python array
    pv_list = selectSpectra("vegetation", sensor, n)
    npv_list = selectSpectra("npv", sensor, n)
    soil_list = selectSpectra("bare", sensor, n)
    burn_list = selectSpectra("burn", sensor, n)
    urban_list = selectSpectra("urban", sensor, n)

    # create a series of global variables for later
    global pv
    global npv
    global soil
    global burn
    global urban

    # then convert them to ee lists
    pv = dict()
    npv = dict()
    soil = dict()
    burn = dict()
    urban = dict()

    for i in range(n):
        pv[f"{i:02d}"] = ee.List(pv_list[i].tolist())
        npv[f"{i:02d}"] = ee.List(npv_list[i].tolist())
        soil[f"{i:02d}"] = ee.List(soil_list[i].tolist())
        burn[f"{i:02d}"] = ee.List(burn_list[i].tolist())
        urban[f"{i:02d}"] = ee.List(urban_list[i].tolist())


def VIS(img):
    """
    Unmixes according to the Vegetation-Impervious-Soil (VIS) approach.

    :param img: the image to unmix.
    :return unmixed: a 3-band image file in order of (soil-veg-impervious)
    """
    import ee

    # run each unmixing iteration
    um_00 = img.unmix([soil["00"], pv["00"], urban["00"]], True, True)
    um_01 = img.unmix([soil["01"], pv["01"], urban["01"]], True, True)
    um_02 = img.unmix([soil["02"], pv["02"], urban["02"]], True, True)
    um_03 = img.unmix([soil["03"], pv["03"], urban["03"]], True, True)
    um_04 = img.unmix([soil["04"], pv["04"], urban["04"]], True, True)
    um_05 = img.unmix([soil["05"], pv["05"], urban["05"]], True, True)
    um_06 = img.unmix([soil["06"], pv["06"], urban["06"]], True, True)
    um_07 = img.unmix([soil["07"], pv["07"], urban["07"]], True, True)
    um_08 = img.unmix([soil["08"], pv["08"], urban["08"]], True, True)
    um_09 = img.unmix([soil["09"], pv["09"], urban["09"]], True, True)
    um_10 = img.unmix([soil["10"], pv["10"], urban["10"]], True, True)
    um_11 = img.unmix([soil["11"], pv["11"], urban["11"]], True, True)
    um_12 = img.unmix([soil["12"], pv["12"], urban["12"]], True, True)
    um_13 = img.unmix([soil["13"], pv["13"], urban["13"]], True, True)
    um_14 = img.unmix([soil["14"], pv["14"], urban["14"]], True, True)
    um_15 = img.unmix([soil["15"], pv["15"], urban["15"]], True, True)
    um_16 = img.unmix([soil["16"], pv["16"], urban["16"]], True, True)
    um_17 = img.unmix([soil["17"], pv["17"], urban["17"]], True, True)
    um_18 = img.unmix([soil["18"], pv["18"], urban["18"]], True, True)
    um_19 = img.unmix([soil["19"], pv["19"], urban["19"]], True, True)
    um_20 = img.unmix([soil["20"], pv["20"], urban["20"]], True, True)
    um_21 = img.unmix([soil["21"], pv["21"], urban["21"]], True, True)
    um_22 = img.unmix([soil["22"], pv["22"], urban["22"]], True, True)
    um_23 = img.unmix([soil["23"], pv["23"], urban["23"]], True, True)
    um_24 = img.unmix([soil["24"], pv["24"], urban["24"]], True, True)
    um_25 = img.unmix([soil["25"], pv["25"], urban["25"]], True, True)
    um_26 = img.unmix([soil["26"], pv["26"], urban["26"]], True, True)
    um_27 = img.unmix([soil["27"], pv["27"], urban["27"]], True, True)
    um_28 = img.unmix([soil["28"], pv["28"], urban["28"]], True, True)
    um_29 = img.unmix([soil["29"], pv["29"], urban["29"]], True, True)

    # generate a collection of images
    coll = ee.ImageCollection.fromImages(
        [
            um_00,
            um_01,
            um_02,
            um_03,
            um_04,
            um_05,
            um_06,
            um_07,
            um_08,
            um_09,
            um_10,
            um_11,
            um_12,
            um_13,
            um_14,
            um_15,
            um_16,
            um_17,
            um_18,
            um_19,
            um_20,
            um_21,
            um_22,
            um_23,
            um_24,
            um_25,
            um_26,
            um_27,
            um_28,
            um_29,
        ]
    )

    # reduce it to a single image and return
    unmixed = coll.mean()

    return unmixed
