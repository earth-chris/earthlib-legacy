"""Functions to return the default image collections for linear unmixing and surface temp retrieval
"""
import sys as _sys

if "ee" not in sys.modules:
    import ee

    ee.Initialize()

# landsat 5
def landsat_5():
    bnds = []
    coll = ee.ImageCollection("LANDSAT/LT05/C01/T2_SR")
    return bnds, coll


# landsat 7
def landsat_7():
    bnds = []
    coll = ee.ImageCollection("LANDSAT/LE07/C01/T2_SR")
    return bnds, coll


# landsat 8
def landsat_8():
    bnds = ["B2", "B3", "B4", "B5", "B6", "B7"]
    coll = ee.ImageCollection("LANDSAT/LC08/C01/T2_SR")
    return bnds, coll
