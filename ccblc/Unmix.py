"""
Routines for performing spectral unmixing on earth engine images
"""


# this routine must be run before any of the specific unmixing routines are set
def setSensor(sensor, bands=None):
    """
    Specifies the sensor to retrieve endmembers for.

    :param sensor: the name of the sensor (from ccblc.listSensors()).
    :param bands: the bands to select.
    :return none: sets a series of global endmember variables
    """
    import ee
    from .utils import selectSpectra

    # set the number of unmixing iterations (we'll hardcode these numbers later, unfortunately)
    n = 30

    # get them as a python array
    pv_list = selectSpectra("vegetation", sensor, n, bands)
    npv_list = selectSpectra("npv", sensor, n, bands)
    soil_list = selectSpectra("bare", sensor, n, bands)
    burn_list = selectSpectra("burn", sensor, n, bands)
    urban_list = selectSpectra("urban", sensor, n, bands)

    # create a series of global variables for later
    global pv
    global npv
    global soil
    global burn
    global urban

    # then convert them to ee lists
    pv = [ee.List(pv_spectra) for pv_spectra in pv_list]
    npv = [ee.List(npv_spectra) for npv_spectra in npv_list]
    soil = [ee.List(soil_spectra) for soil_spectra in soil_list]
    burn = [ee.List(burn_spectra) for burn_spectra in burn_list]
    urban = [ee.List(urban_spectra) for urban_spectra in urban_list]


def VIS(img):
    """
    Unmixes according to the Vegetation-Impervious-Soil (VIS) approach.

    :param img: the image to unmix.
    :return unmixed: a 3-band image file in order of (soil-veg-impervious)
    """
    import ee

    # run each unmixing iteration
    um_00 = img.unmix([soil["00"], pv["00"], urban["00"]], True, True).toFloat()
    um_01 = img.unmix([soil["01"], pv["01"], urban["01"]], True, True).toFloat()
    um_02 = img.unmix([soil["02"], pv["02"], urban["02"]], True, True).toFloat()
    um_03 = img.unmix([soil["03"], pv["03"], urban["03"]], True, True).toFloat()
    um_04 = img.unmix([soil["04"], pv["04"], urban["04"]], True, True).toFloat()
    um_05 = img.unmix([soil["05"], pv["05"], urban["05"]], True, True).toFloat()
    um_06 = img.unmix([soil["06"], pv["06"], urban["06"]], True, True).toFloat()
    um_07 = img.unmix([soil["07"], pv["07"], urban["07"]], True, True).toFloat()
    um_08 = img.unmix([soil["08"], pv["08"], urban["08"]], True, True).toFloat()
    um_09 = img.unmix([soil["09"], pv["09"], urban["09"]], True, True).toFloat()
    um_10 = img.unmix([soil["10"], pv["10"], urban["10"]], True, True).toFloat()
    um_11 = img.unmix([soil["11"], pv["11"], urban["11"]], True, True).toFloat()
    um_12 = img.unmix([soil["12"], pv["12"], urban["12"]], True, True).toFloat()
    um_13 = img.unmix([soil["13"], pv["13"], urban["13"]], True, True).toFloat()
    um_14 = img.unmix([soil["14"], pv["14"], urban["14"]], True, True).toFloat()
    um_15 = img.unmix([soil["15"], pv["15"], urban["15"]], True, True).toFloat()
    um_16 = img.unmix([soil["16"], pv["16"], urban["16"]], True, True).toFloat()
    um_17 = img.unmix([soil["17"], pv["17"], urban["17"]], True, True).toFloat()
    um_18 = img.unmix([soil["18"], pv["18"], urban["18"]], True, True).toFloat()
    um_19 = img.unmix([soil["19"], pv["19"], urban["19"]], True, True).toFloat()
    um_20 = img.unmix([soil["20"], pv["20"], urban["20"]], True, True).toFloat()
    um_21 = img.unmix([soil["21"], pv["21"], urban["21"]], True, True).toFloat()
    um_22 = img.unmix([soil["22"], pv["22"], urban["22"]], True, True).toFloat()
    um_23 = img.unmix([soil["23"], pv["23"], urban["23"]], True, True).toFloat()
    um_24 = img.unmix([soil["24"], pv["24"], urban["24"]], True, True).toFloat()
    um_25 = img.unmix([soil["25"], pv["25"], urban["25"]], True, True).toFloat()
    um_26 = img.unmix([soil["26"], pv["26"], urban["26"]], True, True).toFloat()
    um_27 = img.unmix([soil["27"], pv["27"], urban["27"]], True, True).toFloat()
    um_28 = img.unmix([soil["28"], pv["28"], urban["28"]], True, True).toFloat()
    um_29 = img.unmix([soil["29"], pv["29"], urban["29"]], True, True).toFloat()

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
    unmixed = coll.mean().select([0, 1, 2], ["soil", "pv", "impervious"])

    return unmixed


def SVN(img):
    """
    Unmixes using Soil-Vegetation-NonphotosyntheticVegetation (SVN) endmembers.

    :param img: the image to unmix.
    :return unmixed: a 3-band image file in order of (soil-veg-npv)
    """
    import ee

    # run each unmixing iteration
    um_00 = img.unmix([soil["00"], pv["00"], npv["00"]], True, True).toFloat()
    um_01 = img.unmix([soil["01"], pv["01"], npv["01"]], True, True).toFloat()
    um_02 = img.unmix([soil["02"], pv["02"], npv["02"]], True, True).toFloat()
    um_03 = img.unmix([soil["03"], pv["03"], npv["03"]], True, True).toFloat()
    um_04 = img.unmix([soil["04"], pv["04"], npv["04"]], True, True).toFloat()
    um_05 = img.unmix([soil["05"], pv["05"], npv["05"]], True, True).toFloat()
    um_06 = img.unmix([soil["06"], pv["06"], npv["06"]], True, True).toFloat()
    um_07 = img.unmix([soil["07"], pv["07"], npv["07"]], True, True).toFloat()
    um_08 = img.unmix([soil["08"], pv["08"], npv["08"]], True, True).toFloat()
    um_09 = img.unmix([soil["09"], pv["09"], npv["09"]], True, True).toFloat()
    um_10 = img.unmix([soil["10"], pv["10"], npv["10"]], True, True).toFloat()
    um_11 = img.unmix([soil["11"], pv["11"], npv["11"]], True, True).toFloat()
    um_12 = img.unmix([soil["12"], pv["12"], npv["12"]], True, True).toFloat()
    um_13 = img.unmix([soil["13"], pv["13"], npv["13"]], True, True).toFloat()
    um_14 = img.unmix([soil["14"], pv["14"], npv["14"]], True, True).toFloat()
    um_15 = img.unmix([soil["15"], pv["15"], npv["15"]], True, True).toFloat()
    um_16 = img.unmix([soil["16"], pv["16"], npv["16"]], True, True).toFloat()
    um_17 = img.unmix([soil["17"], pv["17"], npv["17"]], True, True).toFloat()
    um_18 = img.unmix([soil["18"], pv["18"], npv["18"]], True, True).toFloat()
    um_19 = img.unmix([soil["19"], pv["19"], npv["19"]], True, True).toFloat()
    um_20 = img.unmix([soil["20"], pv["20"], npv["20"]], True, True).toFloat()
    um_21 = img.unmix([soil["21"], pv["21"], npv["21"]], True, True).toFloat()
    um_22 = img.unmix([soil["22"], pv["22"], npv["22"]], True, True).toFloat()
    um_23 = img.unmix([soil["23"], pv["23"], npv["23"]], True, True).toFloat()
    um_24 = img.unmix([soil["24"], pv["24"], npv["24"]], True, True).toFloat()
    um_25 = img.unmix([soil["25"], pv["25"], npv["25"]], True, True).toFloat()
    um_26 = img.unmix([soil["26"], pv["26"], npv["26"]], True, True).toFloat()
    um_27 = img.unmix([soil["27"], pv["27"], npv["27"]], True, True).toFloat()
    um_28 = img.unmix([soil["28"], pv["28"], npv["28"]], True, True).toFloat()
    um_29 = img.unmix([soil["29"], pv["29"], npv["29"]], True, True).toFloat()

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
    unmixed = coll.mean().select([0, 1, 2], ["soil", "pv", "npv"])

    return unmixed


def BVNS(img):
    """
    Unmixes using Burned-Vegetation-NonphotosyntheticVegetation-Soil (BVNS) endmembers.

    :param img: the image to unmix.
    :return unmixed: a 4-band image file in order of (burned-veg-npv-soil)
    """
    import ee

    # run each unmixing iteration
    um_00 = img.unmix(
        [burn["00"], pv["00"], npv["00"], soil["00"]], True, True
    ).toFloat()
    um_01 = img.unmix(
        [burn["01"], pv["01"], npv["01"], soil["01"]], True, True
    ).toFloat()
    um_02 = img.unmix(
        [burn["02"], pv["02"], npv["02"], soil["02"]], True, True
    ).toFloat()
    um_03 = img.unmix(
        [burn["03"], pv["03"], npv["03"], soil["03"]], True, True
    ).toFloat()
    um_04 = img.unmix(
        [burn["04"], pv["04"], npv["04"], soil["04"]], True, True
    ).toFloat()
    um_05 = img.unmix(
        [burn["05"], pv["05"], npv["05"], soil["05"]], True, True
    ).toFloat()
    um_06 = img.unmix(
        [burn["06"], pv["06"], npv["06"], soil["06"]], True, True
    ).toFloat()
    um_07 = img.unmix(
        [burn["07"], pv["07"], npv["07"], soil["07"]], True, True
    ).toFloat()
    um_08 = img.unmix(
        [burn["08"], pv["08"], npv["08"], soil["08"]], True, True
    ).toFloat()
    um_09 = img.unmix(
        [burn["09"], pv["09"], npv["09"], soil["09"]], True, True
    ).toFloat()
    um_10 = img.unmix(
        [burn["10"], pv["10"], npv["10"], soil["10"]], True, True
    ).toFloat()
    um_11 = img.unmix(
        [burn["11"], pv["11"], npv["11"], soil["11"]], True, True
    ).toFloat()
    um_12 = img.unmix(
        [burn["12"], pv["12"], npv["12"], soil["12"]], True, True
    ).toFloat()
    um_13 = img.unmix(
        [burn["13"], pv["13"], npv["13"], soil["13"]], True, True
    ).toFloat()
    um_14 = img.unmix(
        [burn["14"], pv["14"], npv["14"], soil["14"]], True, True
    ).toFloat()
    um_15 = img.unmix(
        [burn["15"], pv["15"], npv["15"], soil["15"]], True, True
    ).toFloat()
    um_16 = img.unmix(
        [burn["16"], pv["16"], npv["16"], soil["16"]], True, True
    ).toFloat()
    um_17 = img.unmix(
        [burn["17"], pv["17"], npv["17"], soil["17"]], True, True
    ).toFloat()
    um_18 = img.unmix(
        [burn["18"], pv["18"], npv["18"], soil["18"]], True, True
    ).toFloat()
    um_19 = img.unmix(
        [burn["19"], pv["19"], npv["19"], soil["19"]], True, True
    ).toFloat()
    um_20 = img.unmix(
        [burn["20"], pv["20"], npv["20"], soil["20"]], True, True
    ).toFloat()
    um_21 = img.unmix(
        [burn["21"], pv["21"], npv["21"], soil["21"]], True, True
    ).toFloat()
    um_22 = img.unmix(
        [burn["22"], pv["22"], npv["22"], soil["22"]], True, True
    ).toFloat()
    um_23 = img.unmix(
        [burn["23"], pv["23"], npv["23"], soil["23"]], True, True
    ).toFloat()
    um_24 = img.unmix(
        [burn["24"], pv["24"], npv["24"], soil["24"]], True, True
    ).toFloat()
    um_25 = img.unmix(
        [burn["25"], pv["25"], npv["25"], soil["25"]], True, True
    ).toFloat()
    um_26 = img.unmix(
        [burn["26"], pv["26"], npv["26"], soil["26"]], True, True
    ).toFloat()
    um_27 = img.unmix(
        [burn["27"], pv["27"], npv["27"], soil["27"]], True, True
    ).toFloat()
    um_28 = img.unmix(
        [burn["28"], pv["28"], npv["28"], soil["28"]], True, True
    ).toFloat()
    um_29 = img.unmix(
        [burn["29"], pv["29"], npv["29"], soil["29"]], True, True
    ).toFloat()

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
    unmixed = coll.mean().select([0, 1, 2, 3], ["burned", "pv", "npv", "soil"])

    return unmixed
