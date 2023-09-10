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
        "ASTER": ASTER,
        "AVNIR2": AVNIR2,
        "DoveR": DoveR,
        "Landsat4": Landsat457,
        "Landsat5": Landsat457,
        "Landsat7": Landsat457,
        "Landsat8": Landsat8,
        "MODIS": MODIS,
        "NEON": NEON,
        "PlanetScope": PlanetScope,
        "Sentinel2": Sentinel2,
        "SuperDove": SuperDove,
        "VIIRS": VIIRS,
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


def ASTER(
    img: ee.Image,
    bands: list = getBands("ASTER"),
    n: int = N_ITERATIONS,
    shade_normalize: bool = SHADE_NORMALIZE,
) -> ee.Image:
    """Unmix an ASTER image with soil, pv, npv endmembers.

    Args:
        image: the ee.Image to unmix
        bands: a list of bands to select (from earthlib.getBands(sensor)).
        n: the number of iterations for unmixing.
        shade_normalize: apply shade normalization during unmixing.
            reduces the influences of brightness and illumination geometry.

    Returns:
        unmixed: a 3-band image with bands (%soil, %pv, %npv).
    """
    sensor = "ASTER"
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


def AVNIR2(
    img: ee.Image,
    bands: list = getBands("AVNIR2"),
    n: int = N_ITERATIONS,
    shade_normalize: bool = SHADE_NORMALIZE,
) -> ee.Image:
    """Unmix an AVNIR2 image with soil, pv, npv endmembers.

    Args:
        image: the ee.Image to unmix
        bands: a list of bands to select (from earthlib.getBands(sensor)).
        n: the number of iterations for unmixing.
        shade_normalize: apply shade normalization during unmixing.
            reduces the influences of brightness and illumination geometry.

    Returns:
        unmixed: a 3-band image with bands (%soil, %pv, %npv).
    """
    sensor = "AVNIR2"
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


def DoveR(
    img: ee.Image,
    bands: list = getBands("DoveR"),
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
        unmixed: a 3-band image with bands (%soil, %pv, %npv).
    """
    sensor = "DoveR"
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


def Landsat457(
    img: ee.Image,
    bands: list = getBands("Landsat7"),
    n: int = N_ITERATIONS,
    shade_normalize: bool = SHADE_NORMALIZE,
) -> ee.Image:
    """Unmix a Landsat4 image with soil, pv, npv endmembers.

    Args:
        image: the ee.Image to unmix
        bands: a list of bands to select (from earthlib.getBands(sensor)).
        n: the number of iterations for unmixing.
        shade_normalize: apply shade normalization during unmixing.
            reduces the influences of brightness and illumination geometry.

    Returns:
        unmixed: a 3-band image with bands (%soil, %pv, %npv).
    """
    sensor = "Landsat7"
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
        unmixed: a 3-band image with bands (%soil, %pv, %npv).
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


def MODIS(
    img: ee.Image,
    bands: list = getBands("MODIS"),
    n: int = N_ITERATIONS,
    shade_normalize: bool = SHADE_NORMALIZE,
) -> ee.Image:
    """Unmix a MODIS image with soil, pv, npv endmembers.

    Args:
        image: the ee.Image to unmix
        bands: a list of bands to select (from earthlib.getBands(sensor)).
        n: the number of iterations for unmixing.
        shade_normalize: apply shade normalization during unmixing.
            reduces the influences of brightness and illumination geometry.

    Returns:
        unmixed: a 3-band image with bands (%soil, %pv, %npv).
    """
    sensor = "MODIS"
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


def NEON(
    img: ee.Image,
    bands: list = getBands("NEON"),
    n: int = N_ITERATIONS,
    shade_normalize: bool = SHADE_NORMALIZE,
) -> ee.Image:
    """Unmix a NEON image with soil, pv, npv endmembers.

    Args:
        image: the ee.Image to unmix
        bands: a list of bands to select (from earthlib.getBands(sensor)).
        n: the number of iterations for unmixing.
        shade_normalize: apply shade normalization during unmixing.
            reduces the influences of brightness and illumination geometry.

    Returns:
        unmixed: a 3-band image with bands (%soil, %pv, %npv).
    """
    sensor = "NEON"
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


def PlanetScope(
    img: ee.Image,
    bands: list = getBands("PlanetScope"),
    n: int = N_ITERATIONS,
    shade_normalize: bool = SHADE_NORMALIZE,
) -> ee.Image:
    """Unmix a PlanetScope image with soil, pv, npv endmembers.

    Args:
        image: the ee.Image to unmix
        bands: a list of bands to select (from earthlib.getBands(sensor)).
        n: the number of iterations for unmixing.
        shade_normalize: apply shade normalization during unmixing.
            reduces the influences of brightness and illumination geometry.

    Returns:
        unmixed: a 3-band image with bands (%soil, %pv, %npv).
    """
    sensor = "PlanetScope"
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


def Sentinel2(
    img: ee.Image,
    bands: list = getBands("Sentinel2"),
    n: int = N_ITERATIONS,
    shade_normalize: bool = SHADE_NORMALIZE,
) -> ee.Image:
    """Unmix a Sentinel2 image with soil, pv, npv endmembers.

    Args:
        image: the ee.Image to unmix
        bands: a list of bands to select (from earthlib.getBands(sensor)).
        n: the number of iterations for unmixing.
        shade_normalize: apply shade normalization during unmixing.
            reduces the influences of brightness and illumination geometry.

    Returns:
        unmixed: a 3-band image with bands (%soil, %pv, %npv).
    """
    sensor = "Sentinel2"
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


def SuperDove(
    img: ee.Image,
    bands: list = getBands("SuperDove"),
    n: int = N_ITERATIONS,
    shade_normalize: bool = SHADE_NORMALIZE,
) -> ee.Image:
    """Unmix a SuperDove image with soil, pv, npv endmembers.

    Args:
        image: the ee.Image to unmix
        bands: a list of bands to select (from earthlib.getBands(sensor)).
        n: the number of iterations for unmixing.
        shade_normalize: apply shade normalization during unmixing.
            reduces the influences of brightness and illumination geometry.

    Returns:
        unmixed: a 3-band image with bands (%soil, %pv, %npv).
    """
    sensor = "SuperDove"
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


def VIIRS(
    img: ee.Image,
    bands: list = getBands("VIIRS"),
    n: int = N_ITERATIONS,
    shade_normalize: bool = SHADE_NORMALIZE,
) -> ee.Image:
    """Unmix a VIIRS image with soil, pv, npv endmembers.

    Args:
        image: the ee.Image to unmix
        bands: a list of bands to select (from earthlib.getBands(sensor)).
        n: the number of iterations for unmixing.
        shade_normalize: apply shade normalization during unmixing.
            reduces the influences of brightness and illumination geometry.

    Returns:
        unmixed: a 3-band image with bands (%soil, %pv, %npv).
    """
    sensor = "VIIRS"
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
