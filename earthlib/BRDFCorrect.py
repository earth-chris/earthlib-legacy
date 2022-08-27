"""Routines to prepare datasets prior to unmixing"""
import math
import re
from typing import Callable

import ee

from earthlib.config import (
    BRDF_COEFFICIENTS_L8,
    BRDF_COEFFICIENTS_L457,
    BRDF_COEFFICIENTS_S2,
)
from earthlib.errors import SensorError


def bySensor(sensor: str) -> Callable:
    """Get the appropriate BRDF correction function by sensor type.

    Args:
        sensor: sensor name to return (e.g. "Landsat8", "Sentinel2").

    Returns:
        the BRDF correction function associated with a sensor to pass to a .map() call
    """
    lookup = {
        "Landsat4": Landsat457,
        "Landsat5": Landsat457,
        "Landsat7": Landsat457,
        "Landsat8": Landsat8,
        "Sentinel2": Sentinel2,
    }
    try:
        function = lookup[sensor]
        return function
    except KeyError:
        supported = ", ".join(lookup.keys())
        raise SensorError(
            f"BRDF adjustment not supported for '{sensor}'. Supported: {supported}"
        )


def Landsat457(
    image: ee.Image,
    scaleFactor: float = 1,
) -> ee.Image:
    """Apply BRDF adjustments to a Landsat ETM+ image

    As described in https://www.sciencedirect.com/science/article/pii/S0034425716300220
        and https://groups.google.com/g/google-earth-engine-developers/c/KDqlUCj4LTs/m/hQ5mGodsAQAJ

    Args:
        image: Landsat 4/5/7 surface reflectance image
        scaleFactor: a scaling factor to tune the volumetric scattering adjustment

    Returns:
        a BRDF-corrected image
    """
    return brdfCorrectWrapper(image, BRDF_COEFFICIENTS_L457, scaleFactor)


def Landsat8(
    image: ee.Image,
    scaleFactor: float = 1,
) -> ee.Image:
    """Apply BRDF adjustments to a Landsat8 image

    As described in https://www.sciencedirect.com/science/article/pii/S0034425716300220
        and https://groups.google.com/g/google-earth-engine-developers/c/KDqlUCj4LTs/m/hQ5mGodsAQAJ

    Args:
        image: Landsat8 surface reflectance image
        scaleFactor: a scaling factor to tune the volumetric scattering adjustment

    Returns:
        a BRDF-corrected image
    """
    return brdfCorrectWrapper(image, BRDF_COEFFICIENTS_L8, scaleFactor)


def Sentinel2(
    image: ee.Image,
    scaleFactor: float = 1,
) -> ee.Image:
    """Apply BRDF adjustments to a Sentinel2 image

    As described in https://www.sciencedirect.com/science/article/pii/S0034425717302791

    Args:
        image: Sentinel-2 surface reflectance image
        scaleFactor: a scaling factor to tune the volumetric scattering adjustment

    Returns:
        a BRDF-corrected image
    """
    return brdfCorrectWrapper(image, BRDF_COEFFICIENTS_S2, scaleFactor)


def brdfCorrectWrapper(
    image: ee.Image, coefficientsByBand: dict = None, scaleFactor: float = 1
) -> ee.Image:
    """Wrapper to support keyword arguments that can't be passed during .map() calls"""
    inputBandNames = image.bandNames()
    corners = findCorners(image)
    image = viewAngles(image, corners)
    image = solarPosition(image)
    image = sunZenOut(image)
    image = set(image, "relativeSunViewAz", "i.sunAz - i.viewAz")
    image = rossThick(image, "kvol", "i.sunZen", "i.viewZen", "i.relativeSunViewAz")
    image = rossThick(image, "kvol0", "i.sunZenOut", 0, 0)
    image = liThin(image, "kgeo", "i.sunZen", "i.viewZen", "i.relativeSunViewAz")
    image = liThin(image, "kgeo0", "i.sunZenOut", 0, 0)
    image = adjustBands(image, coefficientsByBand, scaleFactor)
    return image.select(inputBandNames).toInt16()


def viewAngles(image: ee.Image, corners: dict) -> ee.Image:
    """Compute sensor view angles

    Args:
        image: an ee.Image
        corners: a dictionary with corner coords. get from findCorners()

    Returns:
        adds 'viewAz' and 'viewZen' bands to `image`
    """
    maxDistanceToSceneEdge = 1000000
    maxSatelliteZenith = 7.5
    upperCenter = pointBetween(corners["upperLeft"], corners["upperRight"])
    lowerCenter = pointBetween(corners["lowerLeft"], corners["lowerRight"])
    slope = slopeBetween(lowerCenter, upperCenter)
    slopePerp = ee.Number(-1).divide(slope)
    image = set(
        image, "viewAz", ee.Image(ee.Number(math.pi / 2).subtract((slopePerp).atan()))
    )
    leftLine = toLine(corners["upperLeft"], corners["lowerLeft"])
    rightLine = toLine(corners["upperRight"], corners["lowerRight"])
    leftDistance = ee.FeatureCollection(leftLine).distance(maxDistanceToSceneEdge)
    rightDistance = ee.FeatureCollection(rightLine).distance(maxDistanceToSceneEdge)
    viewZenith = (
        rightDistance.multiply(maxSatelliteZenith * 2)
        .divide(rightDistance.add(leftDistance))
        .subtract(maxSatelliteZenith)
    )
    image = set(image, "viewZen", viewZenith.multiply(math.pi).divide(180))
    return image


def solarPosition(image: ee.Image) -> ee.Image:
    """Compute solar position from the time of collection

    From https://www.pythonfmask.org/en/latest/_modules/fmask/landsatangles.html

    Args:
        image: an ee.Image with a "system:time_start" attribute

    Returns:
        adds a series of solar geometry bands to `image`
    """
    date = ee.Date(ee.Number(image.get("system:time_start")))
    secondsInHour = 3600
    image = set(image, "longDeg", ee.Image.pixelLonLat().select("longitude"))
    image = set(
        image,
        "latRad",
        ee.Image.pixelLonLat().select("latitude").multiply(math.pi).divide(180),
    )
    image = set(
        image,
        "hourGMT",
        ee.Number(date.getRelative("second", "day")).divide(secondsInHour),
    )
    image = set(image, "jdp", date.getFraction("year"))  # Julian Date Proportion
    image = set(image, "jdpr", "i.jdp * 2 * {pi}")  # Julian Date Proportion in Radians
    image = set(image, "meanSolarTime", "i.hourGMT + i.longDeg / 15")
    image = set(
        image,
        "localSolarDiff",
        "(0.000075 + 0.001868 * cos(i.jdpr) - 0.032077 * sin(i.jdpr)"
        + "- 0.014615 * cos(2 * i.jdpr) - 0.040849 * sin(2 * i.jdpr))"
        + "* 12 * 60 / {pi}",
    )
    image = set(image, "TrueSolarTime", "i.meanSolarTime + i.localSolarDiff / 60 - 12")
    image = set(image, "angleHour", "i.TrueSolarTime * 15 * {pi} / 180")
    image = set(
        image,
        "delta",
        "0.006918 - 0.399912 * cos(i.jdpr) + 0.070257 * sin(i.jdpr) - 0.006758 * cos(2 * i.jdpr)"
        + "+ 0.000907 * sin(2 * i.jdpr) - 0.002697 * cos(3 * i.jdpr) + 0.001480 * sin(3 * i.jdpr)",
    )
    image = set(
        image,
        "cosSunZen",
        "sin(i.latRad) * sin(i.delta) "
        + "+ cos(i.latRad) * cos(i.delta) * cos(i.angleHour)",
    )
    image = set(image, "sunZen", "acos(i.cosSunZen)")
    image = set(
        image,
        "sinSunAzSW",
        toImage(image, "cos(i.delta) * sin(i.angleHour) / sin(i.sunZen)").clamp(-1, 1),
    )
    image = set(
        image,
        "cosSunAzSW",
        "(-cos(i.latRad) * sin(i.delta)"
        + "+ sin(i.latRad) * cos(i.delta) * cos(i.angleHour)) / sin(i.sunZen)",
    )
    image = set(image, "sunAzSW", "asin(i.sinSunAzSW)")
    image = setIf(image, "sunAzSW", "i.cosSunAzSW <= 0", "{pi} - i.sunAzSW", "sunAzSW")
    image = setIf(
        image,
        "sunAzSW",
        "i.cosSunAzSW > 0 and i.sinSunAzSW <= 0",
        "2 * {pi} + i.sunAzSW",
        "sunAzSW",
    )
    image = set(image, "sunAz", "i.sunAzSW + {pi}")
    image = setIf(image, "sunAz", "i.sunAz > 2 * {pi}", "i.sunAz - 2 * {pi}", "sunAz")
    return image


def sunZenOut(image: ee.Image) -> ee.Image:
    """Compute the solar zenith angle from an image center

    From https://hls.gsfc.nasa.gov/wp-content/uploads/2016/08/HLS.v1.0.UserGuide.pdf

    Args:
        image: an ee.Image with a "system:footprint" attribute

    Returns:
        adds a "sunZenOut" band to `image`
    """
    image = set(
        image,
        "centerLat",
        ee.Number(
            ee.Geometry(image.get("system:footprint"))
            .bounds()
            .centroid(30)
            .coordinates()
            .get(0)
        )
        .multiply(math.pi)
        .divide(180),
    )
    image = set(
        image,
        "sunZenOut",
        "(31.0076"
        + "- 0.1272 * i.centerLat"
        + "+ 0.01187 * pow(i.centerLat, 2)"
        + "+ 2.40E-05 * pow(i.centerLat, 3)"
        + "- 9.48E-07 * pow(i.centerLat, 4)"
        + "- 1.95E-09 * pow(i.centerLat, 5)"
        + "+ 6.15E-11 * pow(i.centerLat, 6)) * {pi}/180",
    )
    return image


def rossThick(
    image: ee.Image, bandName: str, sunZen: str, viewZen: str, relativeSunViewAz: str
) -> ee.Image:
    """From https://modis.gsfc.nasa.gov/data/atbd/atbd_mod09.pdf"""
    args = {
        "sunZen": sunZen,
        "viewZen": viewZen,
        "relativeSunViewAz": relativeSunViewAz,
    }
    image = cosPhaseAngle(image, "cosPhaseAngle", sunZen, viewZen, relativeSunViewAz)
    image = set(image, "phaseAngle", "acos(i.cosPhaseAngle)")
    image = set(
        image,
        bandName,
        "(({pi}/2 - i.phaseAngle) * i.cosPhaseAngle + sin(i.phaseAngle)) "
        + "/ (cos({sunZen}) + cos({viewZen})) - {pi}/4",
        args,
    )
    return image


def liThin(
    image: ee.Image, bandName: str, sunZen: str, viewZen: str, relativeSunViewAz: str
) -> ee.Image:
    """From https://modis.gsfc.nasa.gov/data/atbd/atbd_mod09.pdf"""
    args = {
        "sunZen": sunZen,
        "viewZen": viewZen,
        "relativeSunViewAz": relativeSunViewAz,
        "hb": 2,
    }
    image = anglePrime(image, "sunZenPrime", sunZen)
    image = anglePrime(image, "viewZenPrime", viewZen)
    image = cosPhaseAngle(
        image,
        "cosPhaseAnglePrime",
        "i.sunZenPrime",
        "i.viewZenPrime",
        relativeSunViewAz,
    )
    image = set(
        image,
        "distance",
        "sqrt(pow(tan(i.sunZenPrime), 2) + pow(tan(i.viewZenPrime), 2)"
        + "- 2 * tan(i.sunZenPrime) * tan(i.viewZenPrime) * cos({relativeSunViewAz}))",
        args,
    )
    image = set(image, "temp", "1/cos(i.sunZenPrime) + 1/cos(i.viewZenPrime)")
    image = set(
        image,
        "cosT",
        toImage(
            image,
            "{hb} * sqrt(pow(i.distance, 2) + pow(tan(i.sunZenPrime) * tan(i.viewZenPrime) * sin({relativeSunViewAz}), 2))"
            + "/ i.temp",
            args,
        ).clamp(-1, 1),
    )
    image = set(image, "t", "acos(i.cosT)")
    image = set(image, "overlap", "(1/{pi}) * (i.t - sin(i.t) * i.cosT) * (i.temp)")
    image = setIf(image, "overlap", "i.overlap > 0", 0)
    image = set(
        image,
        bandName,
        "i.overlap - i.temp"
        + "+ (1/2) * (1 + i.cosPhaseAnglePrime) * (1/cos(i.sunZenPrime)) * (1/cos(i.viewZenPrime))",
    )
    return image


def anglePrime(image: ee.Image, name: str, angle: str) -> ee.Image:
    """Prime angle is computed from sun/sensor zenith and used to estimate phase angle"""
    args = {"br": 1, "angle": angle}
    image = set(image, "tanAnglePrime", "{br} * tan({angle})", args)
    image = setIf(image, "tanAnglePrime", "i.tanAnglePrime < 0", 0)
    image = set(image, name, "atan(i.tanAnglePrime)")
    return image


def cosPhaseAngle(
    image: ee.Image, name: str, sunZen: str, viewZen: str, relativeSunViewAz: str
) -> ee.Image:
    """Phase angle estimates the relative deviation between sun/sensor geometry"""
    args = {
        "sunZen": sunZen,
        "viewZen": viewZen,
        "relativeSunViewAz": relativeSunViewAz,
    }
    image = set(
        image,
        name,
        toImage(
            image,
            "cos({sunZen}) * cos({viewZen})"
            + "+ sin({sunZen}) * sin({viewZen}) * cos({relativeSunViewAz})",
            args,
        ).clamp(-1, 1),
    )
    return image


def adjustBands(
    image: ee.Image, coefficientsByBand: dict, scaleFactor: float = 1
) -> ee.Image:
    """Apply estimated BRDF adjustments band-by-band"""
    for bandName in coefficientsByBand:
        image = applyCFactor(image, bandName, coefficientsByBand[bandName], scaleFactor)
    return image


def applyCFactor(
    image: ee.Image, bandName: str, coefficients: dict, scaleFactor: float
) -> ee.Image:
    """Apply BRDF C-factor adjustments to a single band"""
    image = brdf(image, "brdf", "kvol", "kgeo", coefficients, scaleFactor)
    image = brdf(image, "brdf0", "kvol0", "kgeo0", coefficients, scaleFactor)
    image = set(image, "cFactor", "i.brdf0 / i.brdf", coefficients)
    image = set(
        image, bandName, "{bandName} * i.cFactor", {"bandName": "i." + bandName}
    )
    return image


def brdf(
    image: ee.Image,
    bandName: str,
    kvolBand: str,
    kgeoBand: str,
    coefficients: dict,
    scaleFactor: float,
) -> ee.Image:
    """Apply the BRDF volumetric scattering adjustment"""
    args = merge_dicts(
        coefficients,
        {
            "kvol": f"{scaleFactor} * i." + kvolBand,
            "kgeo": "i." + kgeoBand,
        },
    )
    image = set(image, bandName, "{fiso} + {fvol} * {kvol} + {fgeo} * {kvol}", args)
    return image


def x(point: ee.Geometry.Point):
    """Get the X location from a point geometry"""
    return ee.Number(ee.List(point).get(0))


def y(point: ee.Geometry.Point):
    """Get the Y location from a point geometry"""
    return ee.Number(ee.List(point).get(1))


def findCorners(image: ee.Image) -> dict:
    """Get corner coordinates from an images 'system:footprint' attribute"""

    def get_xs(coord):
        return x(coord)

    def get_ys(coord):
        return y(coord)

    def findCorner(targetValue, values):
        def get_diff(value):
            return ee.Number(value).subtract(targetValue).abs()

        diff = values.map(get_diff)
        minValue = diff.reduce(ee.Reducer.min())
        idx = diff.indexOf(minValue)
        return coords.get(idx)

    footprint = ee.Geometry(image.get("system:footprint"))
    bounds = ee.List(footprint.bounds().coordinates().get(0))
    coords = footprint.coordinates()
    xs = coords.map(get_xs)
    ys = coords.map(get_ys)
    lowerLeft = findCorner(x(bounds.get(0)), xs)
    lowerRight = findCorner(y(bounds.get(1)), ys)
    upperRight = findCorner(x(bounds.get(2)), xs)
    upperLeft = findCorner(y(bounds.get(3)), ys)
    return {
        "upperLeft": upperLeft,
        "upperRight": upperRight,
        "lowerRight": lowerRight,
        "lowerLeft": lowerLeft,
    }


def pointBetween(
    pointA: ee.Geometry.Point, pointB: ee.Geometry.Point
) -> ee.Geometry.Point:
    """Compute the cetroid of two points"""
    return ee.Geometry.LineString([pointA, pointB]).centroid().coordinates()


def slopeBetween(
    pointA: ee.Geometry.Point, pointB: ee.Geometry.Point
) -> ee.Geometry.Point:
    """Compute the slope of the distance between two points"""
    return ((y(pointA)).subtract(y(pointB))).divide((x(pointA)).subtract(x(pointB)))


def toLine(
    pointA: ee.Geometry.Point, pointB: ee.Geometry.Point
) -> ee.Geometry.LineString:
    """Create a LineString from two Points"""
    return ee.Geometry.LineString([pointA, pointB])


def set(
    image: ee.Image,
    name: str,
    toAdd: str,
    args: dict = None,
) -> ee.Image:
    """Append the value of `toAdd` as a band `name` to `image`"""
    toAdd = toImage(image, toAdd, args)
    return image.addBands(toAdd.rename(name), None, True)


def setIf(
    image: ee.Image, name: str, condition: str, TrueValue: float, FalseValue: float = 0
) -> ee.Image:
    """Create a conditional mask and add it as a band to `image`"""

    def invertMask(mask):
        return mask.multiply(-1).add(1)

    condition = toImage(image, condition)
    TrueMasked = toImage(image, TrueValue).mask(toImage(image, condition))
    FalseMasked = toImage(image, FalseValue).mask(invertMask(condition))
    value = TrueMasked.unmask(FalseMasked)
    image = set(image, name, value)
    return image


def toImage(image: ee.Image, band: str, args: dict = None) -> ee.Image:
    """Convenience function to convert scalars or expressions to new bands"""
    if type(band) is str:
        if "." in band or " " in band or "{" in band:
            band = image.expression(format(band, args), {"i": image})
        else:
            band = image.select(band)
    return ee.Image(band)


def format(s: str, args: dict, constants: dict = {"pi": f"{math.pi:0.8f}"}) -> str:
    """Format a string to strip out {} values"""
    args = args or {}
    allArgs = merge_dicts(constants, args)
    vars = re.findall(r"\{([A-Za-z0-9_]+)\}", s)
    for var in vars:
        replacement_var = str(allArgs[var])
        s = s.replace("{" + f"{var}" + "}", replacement_var)
    return s


def merge_dicts(d1: dict, d2: dict) -> dict:
    """Create one dictionary from two"""
    return {**d1, **d2}
