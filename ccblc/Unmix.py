"""
Routines for performing spectral unmixing on earth engine images
"""


# this routine must be run before any of the specific unmixing routines are set
def setSensor(sensor, n=30, bands=None):
    """
    Specifies the sensor to retrieve endmembers for.

    :param sensor: the name of the sensor (from ccblc.listSensors()).
    :param n: the number of iterations for unmixing
    :param bands: the bands to select.
    :return none: sets a series of global endmember variables
    """
    import ee
    from .utils import selectSpectra

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
    pv = [ee.List(pv_spectra.tolist()) for pv_spectra in pv_list]
    npv = [ee.List(npv_spectra.tolist()) for npv_spectra in npv_list]
    soil = [ee.List(soil_spectra.tolist()) for soil_spectra in soil_list]
    burn = [ee.List(burn_spectra.tolist()) for burn_spectra in burn_list]
    urban = [ee.List(urban_spectra.tolist()) for urban_spectra in urban_list]


def computeModeledSpectra(endmembers, fractions):
    """
    Constructs a modeled spectrum for each image pixel based on the estimated endmember fractions

    :param endmembers: a list of ee.List() items, each representing an endmember spectrum
    :param fractions: an ee.Image output from .unmix() with the same number of bands as items in `endmembers`
    :return modeled_reflectance: an ee.Image with n_bands equal to the number of endmember bands
    """
    import ee

    # compute the number of endmember bands
    nb = endmembers[0].length()
    band_range = range(nb)
    band_names = [f"M{band:02d}" for band in band_range]

    # create a list to store each reflectance fraction
    refl_fraction_images = list()

    # loop through each endmember and mulitply the fraction estimated by the reflectance value
    for i, endmember in enumerate(endmembers):
        refl_fraction_list = [
            ee.Image(endmember.get(band)).multiply(fractions.select[i])
            for band in range(nb)
        ]
        refl_fraction_images.append(
            ee.ImageCollection.fromImages(refl_fraction_list).toBands()
        )

    # convert these images to an image collection and sum them together
    modeled_reflectance = (
        ee.ImageCollection.fromImages(refl_fraction_images)
        .sum()
        .select(band_range, band_names)
    )

    return modeled_reflectance


def VIS(img):
    """
    Unmixes according to the Vegetation-Impervious-Soil (VIS) approach.

    :param img: the image to unmix.
    :return unmixed: a 3-band image file in order of (soil-veg-impervious)
    """
    import ee

    # create a list of images to append and later convert to an image collection
    unmixed = list()

    # loop through each iteration and unmix each
    for soil_spectra, pv_spectra, urban_spectra in zip(soil, pv, urban):
        unmixed_iter = img.unmix(
            [soil_spectra, pv_spectra, urban_spectra], True, True
        ).toFloat()
        unmixed.append(unmixed_iter)

    # generate an image collection
    coll = ee.ImageCollection.fromImages(unmixed)

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

    # create a list of images to append and later convert to an image collection
    unmixed = list()

    # loop through each iteration and unmix each
    for soil_spectra, pv_spectra, npv_spectra in zip(soil, pv, npv):
        unmixed_iter = img.unmix(
            [soil_spectra, pv_spectra, npv_spectra], True, True
        ).toFloat()
        unmixed.append(unmixed_iter)

    # generate an image collection
    coll = ee.ImageCollection.fromImages(unmixed)

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

    # create a list of images to append and later convert to an image collection
    unmixed = list()

    # loop through each iteration and unmix each
    for burn_spectra, pv_spectra, npv_spectra, soil_spectra in zip(
        burn, pv, npv, soil
    ):
        unmixed_iter = img.unmix(
            [burn_spectra, pv_spectra, npv_spectra, soil_spectra], True, True
        ).toFloat()
        unmixed.append(unmixed_iter)

    # generate an image collection
    coll = ee.ImageCollection.fromImages(unmixed)

    # reduce it to a single image and return
    unmixed = coll.mean().select([0, 1, 2, 3], ["burned", "pv", "npv", "soil"])

    return unmixed
