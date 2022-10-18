"""Methods for running Soil / Photosynthetic Vegetation / Non-Photosynthetic Vegetation unmixing."""

from typing import Callable, Tuple

import ee

from earthlib.config import N_ITERATIONS, SHADE_NORMALIZE
from earthlib.Unmix import fractionalCover
from earthlib.utils import getBands, selectSpectra

# default band names
ENDMEMBER_NAMES = ["Soil", "PV", "NPV"]


def bySensor(sensor: str) -> Callable:
    """Returns the appropriate scaling function to use by sensor type.

    Args:
        sensor: string with the sensor name to return (e.g. "Landsat8", "Sentinel2").

    Returns:
        the scale function associated with a sensor to pass to an ee .map() call
    """
    lookup = {
        "Landsat8": Landsat8,
    }
    try:
        function = lookup[sensor]
        return function
    except KeyError:
        supported = ", ".join(lookup.keys())
        raise SensorError(
            f"Scaling adjustment not supported for '{sensor}'. Supported: {supported}"
        )


def getEndmembers(sensor: str, bands: list, n: int = N_ITERATIONS) -> Tuple[list]:
    """Get a series of ee.List objects with the SoilPVNPV endmembers.

    Args:
        sensor: the name of the sensor (from earthlib.listSensors()).
        bands: a list of bands to select (from earthlib.getBands(sensor)).
        n: the number of iterations for unmixing.

    Returns:
        (soil, pv, npv) endmembers
    """
    soil_list = selectSpectra("bare", sensor, n, bands)
    pv_list = selectSpectra("vegetation", sensor, n, bands)
    npv_list = selectSpectra("npv", sensor, n, bands)
    soil = [ee.List(soil_spectra.tolist()) for soil_spectra in soil_list]
    pv = [ee.List(pv_spectra.tolist()) for pv_spectra in pv_list]
    npv = [ee.List(npv_spectra.tolist()) for npv_spectra in npv_list]

    return soil, pv, npv


def Landsat8(
    img: ee.Image,
    bands: list = getBands("Landsat8"),
    n: int = N_ITERATIONS,
    shade_normalize: bool = SHADE_NORMALIZE,
) -> ee.Image:
    """Unmix a Landsat8 image with soil, pv, npv endmembers.

    Args:
        image: the ee.Image to unmix
        bands: a list of bands to select (from earthlib.getBands(sensor)).
        n: the number of iterations for unmixing.
        shade_normalize: apply shade normalization during unmixing.
            reduces the influences of brightness and illumination geometry.

    Returns:
        unmixed: a 4- or 5-band image with bands (%soil, %pv, %npv, RMSE) or
            (%soil, %pv, %npv, %shade, RMSE) depending on whether shade
            normalization is applied. The first three bands should sum to 1
            regardless of whether normalization was applied.
    """
    sensor = "Landsat8"
    n_bands = len(bands)
    endmembers = getEndmembers(sensor, bands, n)
    unmixed = fractionalCover(
        img,
        endmembers,
        endmember_names=ENDMEMBER_NAMES,
        shade_normalize=shade_normalize,
        n_bands=n_bands,
    )

    return unmixed
