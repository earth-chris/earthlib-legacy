"""Routines to prepare input datasets prior to unmixing"""

import math
import re

import ee

CONSTANTS = {"pi": f"{math.pi:0.8f}"}
BRDF_COEFFICIENTS_L8 = {
    "B2": {"fiso": 0.0774, "fgeo": 0.0079, "fvol": 0.0372},
    "B3": {"fiso": 0.1306, "fgeo": 0.0178, "fvol": 0.0580},
    "B4": {"fiso": 0.1690, "fgeo": 0.0227, "fvol": 0.0574},
    "B5": {"fiso": 0.3093, "fgeo": 0.0330, "fvol": 0.1535},
    "B6": {"fiso": 0.3430, "fgeo": 0.0453, "fvol": 0.1154},
    "B7": {"fiso": 0.2658, "fgeo": 0.0387, "fvol": 0.0639},
}


def brdfCorrectL8(image, coefficientsByBand=BRDF_COEFFICIENTS_L8, scaleFactor=3):
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

    return image.select(inputBandNames)


def viewAngles(image, corners):
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


def solarPosition(image):
    # Ported from http:#pythonfmask.Org/en/latest/_modules/fmask/landsatangles.html
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


def sunZenOut(image):
    # https:#nex.nasa.gov/nex/static/media/publication/HLS.v1.0.UserGuide.pdf
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


def rossThick(image, bandName, sunZen, viewZen, relativeSunViewAz):
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


def liThin(image, bandName, sunZen, viewZen, relativeSunViewAz):
    # From https:#modis.gsfc.nasa.gov/data/atbd/atbd_mod09.pdf
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


def anglePrime(image, name, angle):
    args = {"br": 1, "angle": angle}
    image = set(image, "tanAnglePrime", "{br} * tan({angle})", args)
    image = setIf(image, "tanAnglePrime", "i.tanAnglePrime < 0", 0)
    image = set(image, name, "atan(i.tanAnglePrime)")
    return image


def cosPhaseAngle(image, name, sunZen, viewZen, relativeSunViewAz):
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


def adjustBands(image, coefficientsByBand, scaleFactor=1):
    for bandName in coefficientsByBand:
        image = applyCFactor(image, bandName, coefficientsByBand[bandName], scaleFactor)

    return image


def applyCFactor(image, bandName, coefficients, scaleFactor):
    image = brdf(image, "brdf", "kvol", "kgeo", coefficients, scaleFactor)
    image = brdf(image, "brdf0", "kvol0", "kgeo0", coefficients, scaleFactor)
    image = set(image, "cFactor", "i.brdf0 / i.brdf", coefficients)
    image = set(
        image, bandName, "{bandName} * i.cFactor", {"bandName": "i." + bandName}
    )
    return image


def brdf(image, bandName, kvolBand, kgeoBand, coefficients, scaleFactor):
    """check this multiplication factor.  Is there an 'optimal' value?  Without a factor here, there is not enough correction."""
    args = merge_dicts(
        coefficients,
        {
            "kvol": f"{scaleFactor} * i." + kvolBand,
            "kgeo": "i." + kgeoBand,
        },
    )
    image = set(image, bandName, "{fiso} + {fvol} * {kvol} + {fgeo} * {kvol}", args)
    return image


def x(point):
    return ee.Number(ee.List(point).get(0))


def y(point):
    return ee.Number(ee.List(point).get(1))


def findCorners(image):
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


def pointBetween(pointA, pointB):
    return ee.Geometry.LineString([pointA, pointB]).centroid().coordinates()


def slopeBetween(pointA, pointB):
    return ((y(pointA)).subtract(y(pointB))).divide((x(pointA)).subtract(x(pointB)))


def toLine(pointA, pointB):
    return ee.Geometry.LineString([pointA, pointB])


def set(
    image,
    name,
    toAdd,
    args=None,
):
    toAdd = toImage(image, toAdd, args)
    return image.addBands(toAdd.rename(name), None, True)


def setIf(image, name, condition, TrueValue, FalseValue=0):
    def invertMask(mask):
        return mask.multiply(-1).add(1)

    condition = toImage(image, condition)
    TrueMasked = toImage(image, TrueValue).mask(toImage(image, condition))
    FalseMasked = toImage(image, FalseValue).mask(invertMask(condition))
    value = TrueMasked.unmask(FalseMasked)
    image = set(image, name, value)
    return image


def toImage(image, band, args=None):
    if type(band) is str:
        if "." in band or " " in band or "{" in band:
            band = image.expression(format(band, args), {"i": image})
        else:
            band = image.select(band)

    return ee.Image(band)


def format(s, args, constants=CONSTANTS):
    args = args or {}
    allArgs = merge_dicts(constants, args)
    vars = re.findall(r"\{([A-Za-z0-9_]+)\}", s)
    for var in vars:
        replacement_var = str(allArgs[var])
        s = s.replace("{" + f"{var}" + "}", replacement_var)

    return s


def merge_dicts(d1, d2):
    return {**d1, **d2}
