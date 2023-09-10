"""Routines for performing spectral unmixing on earth engine images."""

from typing import Callable

import ee

from earthlib.config import RMSE, WEIGHT
from earthlib.utils import selectSpectra


def fractionalCover(
    img: ee.Image,
    endmembers: list,
    endmember_names: list,
    n_bands: int = None,
    shade_normalize: bool = True,
) -> ee.Image:
    """Computes the percent cover of each endmember spectra.

    Args:
        img: the ee.Image to unmix.
        endmembers: lists of ee.List objects, each element corresponding to a subType.
        endmember_names: list of names for each endmember. must match the number of lists passed.
        n_bands: number of reflectance bands used for unmixing.
        shade_normalize: flag to apply shade normalization during unmixing.

    Returns:
        unmixed: a 3-band image file in order of (soil-veg-impervious).
    """
    if n_bands is None:
        n_bands = len(list(img.bandNames().getInfo()))
    n_classes = len(endmembers)
    band_numbers = list(range(n_classes))
    shade = ee.List([0] * n_bands)

    # create a list of images to append and later convert to an image collection
    unmixed = list()

    # loop through each iteration and unmix each
    for spectra in zip(*endmembers):

        if shade_normalize:
            spectra += (shade,)

        unmixed_iter = img.unmix(spectra, True, True)

        # run the forward model to evaluate the fractional cover fit
        modeled_reflectance = computeModeledSpectra(spectra, unmixed_iter, n_bands)
        rmse = computeSpectralRMSE(img, modeled_reflectance, n_bands)

        # normalize by the observed shade fraction
        if shade_normalize:
            shade_fraction = unmixed_iter.select([n_classes]).subtract(1).abs()
            unmixed_iter = unmixed_iter.divide(shade_fraction)

        # rename the bands and append an rmse band
        unmixed.append(
            unmixed_iter.select(band_numbers, endmember_names).addBands(rmse)
        )

    # use the sum of rmse to weight each estimate
    rmse_sum = ee.Image(
        ee.ImageCollection.fromImages(unmixed).select([RMSE]).sum().select([0], ["SUM"])
    )
    unscaled = [computeWeight(fractions, rmse_sum) for fractions in unmixed]

    # use these weights to scale each unmixing estimate
    weight_sum = ee.Image(
        ee.ImageCollection.fromImages(unscaled).select([WEIGHT]).sum()
    )
    scaled = [
        weightedAverage(fractions, weight_sum, endmember_names)
        for fractions in unscaled
    ]

    # reduce it to a single image and return
    unmixed = ee.ImageCollection.fromImages(scaled).sum().toFloat()

    return unmixed


def computeModeledSpectra(
    endmembers: list, fractions: ee.Image, n_bands: int
) -> ee.Image:
    """Constructs a modeled spectrum for each pixel based on endmember fractions.

    Args:
        endmembers: a list of ee.List() items, each representing an endmember spectrum.
        fractions: ee.Image output from .unmix() with the same number of bands as items in `endmembers`.
        n_bands: the number of reflectance bands used to compute the unmixing.

    Returns:
        an ee.Image with n_bands equal to the number of endmember bands.
    """
    # compute the number of endmember bands
    band_range = list(range(n_bands))
    band_names = [f"M{band:02d}" for band in band_range]

    # create a list to store each reflectance fraction
    refl_fraction_images = list()

    # loop through each endmember and mulitply the fraction estimated by the reflectance value
    for i, endmember in enumerate(endmembers):
        fraction = fractions.select([i])
        refl_fraction_list = [
            fraction.multiply(ee.Number(endmember.get(band))) for band in band_range
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
        .select(band_range, band_names)
    )

    return modeled_reflectance


def computeSpectralRMSE(
    measured: ee.Image, modeled: ee.Image, n_bands: int
) -> ee.Image:
    """Computes root mean squared error between measured and modeled spectra.

    Args:
        measured: an ee.Image of measured reflectance.
        modeled: an ee.Image of modeled reflectance.
        n_bands: the number of reflectance bands used to compute the unmixing.

    Returns:
        rmse: a floating point ee.Image with pixel-wise RMSE values.
    """
    # harmonize band info to ensure element-wise computation
    band_range = list(range(n_bands))
    band_names = [f"M{band:02d}" for band in band_range]

    # compute rmse
    rmse = (
        measured.select(band_range, band_names)
        .subtract(modeled.select(band_range, band_names))
        .pow(2)
        .reduce(ee.Reducer.sum())
        .sqrt()
        .select([0], [RMSE])
    )

    return rmse


def computeWeight(fractions: ee.Image, rmse_sum: ee.Image) -> ee.Image:
    """Computes the relative weight for an image's RMSE based on the sum of the global RMSE.

    Args:
        fractions: a multi-band ee.Image object with an 'RMSE' band.
        rmse_sum: a single-band ee.Image object with the global RMSE value.

    Returns:
        the input `fractions` image with a 'weight' band added.
    """
    rmse = fractions.select([RMSE])
    ratio = rmse.divide(rmse_sum).select([0], ["ratio"])
    weight = ee.Image(1).subtract(ratio).select([0], [WEIGHT])
    unweighted = fractions.addBands([weight])

    return unweighted


def weightedAverage(
    fractions: ee.Image, weight_sum: ee.Image, band_names: list
) -> ee.Image:
    """Computes an RMSE-weighted fractional cover image.

    Args:
        fractions: a multi-band ee.Image object with a 'weight' band.
        weight_sum: a single-band ee.Image object with the global weight sum.
        band_names: list of band names to apply the weighted average to

    Returns:
        a scaled fractional cover image.
    """
    # harmonize band info
    band_range = list(range(len(band_names)))

    scaler = fractions.select([WEIGHT]).divide(weight_sum)
    weighted = fractions.select(band_range, band_names).multiply(scaler)

    return weighted
