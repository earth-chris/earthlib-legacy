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
    nb = int(endmembers[0].length().getInfo())
    band_range = list(range(nb))
    band_names = [f"M{band:02d}" for band in band_range]

    # create a list to store each reflectance fraction
    refl_fraction_images = list()

    # loop through each endmember and mulitply the fraction estimated by the reflectance value
    for i, endmember in enumerate(endmembers):
        fraction = fractions.select([i])
        refl_fraction_list = [
            fraction.multiply(ee.Image(endmember.get(band).getInfo()))
            for band in band_range
        ]
        refl_fraction_images.append(
            ee.ImageCollection.fromImages(refl_fraction_list)
            .toBands()
            .select(band_range, band_names)
        )

    # convert these images to an image collection and sum them together to reconstruct the spectrum
    modeled_reflectance = (
        ee.ImageCollection.fromImages(refl_fraction_images)
        .sum()
        .toFloat()
        .select(band_range, band_names)
    )

    return modeled_reflectance


def computeSpectralRMSE(measured, modeled):
    """
    Computes the root mean squared error between measured and modeled spectra

    :param measured: an ee.Image of measured reflectance
    :param modeled: an ee.Image of modeled reflectance
    :return rmse: a floating point ee.Image with pixel-wise RMSE values
    """
    import ee

    # harmonize band info to ensure element-wise computation
    band_names = list(measured.bandNames().getInfo())
    band_range = list(range(len(band_names)))

    # compute rmse
    rmse = (
        measured.select(band_range, band_names)
        .subtract(modeled.select(band_range, band_names))
        .pow(2)
        .reduce(ee.Reducer.sum())
        .sqrt()
        .select([0], ["RMSE"])
        .toFloat()
    )

    return rmse


def computeWeight(fractions, rmse_sum):
    """
    Computes the relative weight for an image's RMSE based on the sum of the global RMSE

    :param fractions: a multi-band ee.Image object with an 'RMSE' band
    :param rmse_sum: a single-band ee.Image object with the global RMSE value
    :return unweighted: appends the fractions image with a 'weight' band
    """
    import ee

    # compute the relative weight
    rmse = fractions.select(["RMSE"])
    ratio = rmse.divide(rmse_sum).toFloat()
    weight = ee.Image(1).subtract(ratio).select([0], ["weight"])
    unweighted = fractions.addBands([weight])

    return unweighted


def weightedAverage(fractions, weight_sum):
    """
    Computes an RMSE-weighted fractional cover image

    :param fractions: a multi-band ee.Image object with a 'weight' band
    :param weight_sum: a single-band ee.Image object with the global weight sum
    :return weighted: scales the fractions image
    """
    import ee

    # harmonize band info
    band_names = list(fractions.bandNames().getInfo())
    band_names.pop(band_names.index("weight"))
    band_range = list(range(len(band_names)))

    scaler = fractions.select(["weight"]).divide(weight_sum)
    weighted = fractions.select(band_range, band_names).multiply(scaler)

    return weighted


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
        unmixed_iter = (
            img.unmix([soil_spectra, pv_spectra, urban_spectra], True, True)
            .toFloat()
            .select([0, 1, 2], ["soil", "pv", "impervious"])
        )
        endmembers = [soil_spectra, pv_spectra, urban_spectra]
        modeled_refl = computeModeledSpectra(endmembers, unmixed_iter)
        rmse = computeSpectralRMSE(img, modeled_refl)
        unmixed.append(unmixed_iter.addBands(rmse))

    # generate an image collection
    coll = ee.ImageCollection.fromImages(unmixed)

    # use the sum of rmse to weight each estimate
    rmse_sum = ee.Image(coll.select(["RMSE"]).sum().select([0], ["SUM"]).toFloat())
    unscaled = [computeWeight(fractions, rmse_sum) for fractions in unmixed]

    # use these weights to scale each unmixing estimate
    weight_sum = ee.Image(
        ee.ImageCollection.fromImages(unscaled).select(["weight"]).sum().toFloat()
    )
    scaled = [weightedAverage(fractions, weight_sum) for fractions in unscaled]

    # reduce it to a single image and return
    unmixed = ee.ImageCollection.fromImages(scaled).sum().toFloat()

    # return unmixed
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
