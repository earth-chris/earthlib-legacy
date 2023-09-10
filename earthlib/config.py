"""Default configuration paths and parameters"""

import json
import os

import pandas as pd

# file paths for the package data
package_path = os.path.realpath(__file__)
package_dir = os.path.dirname(package_path)
collections_path = os.path.join(package_dir, "data", "collections.json")
metadata_path = os.path.join(package_dir, "data", "spectra.csv")
endmember_path = os.path.join(package_dir, "data", "spectra.sli")

# read critical data into memory
metadata = pd.read_csv(metadata_path)
with open(collections_path, "r+") as f:
    collections = json.load(f)


# BRDF correction coefficients
# https://www.sciencedirect.com/science/article/pii/S0034425716300220
BRDF_COEFFICIENTS_L457 = {
    "SR_B1": {"fiso": 0.0774, "fgeo": 0.0079, "fvol": 0.0372},
    "SR_B2": {"fiso": 0.1306, "fgeo": 0.0178, "fvol": 0.0580},
    "SR_B3": {"fiso": 0.1690, "fgeo": 0.0227, "fvol": 0.0574},
    "SR_B4": {"fiso": 0.3093, "fgeo": 0.0330, "fvol": 0.1535},
    "SR_B5": {"fiso": 0.3430, "fgeo": 0.0453, "fvol": 0.1154},
    "SR_B7": {"fiso": 0.2658, "fgeo": 0.0387, "fvol": 0.0639},
}
BRDF_COEFFICIENTS_L8 = {
    "SR_B2": {"fiso": 0.0774, "fgeo": 0.0079, "fvol": 0.0372},
    "SR_B3": {"fiso": 0.1306, "fgeo": 0.0178, "fvol": 0.0580},
    "SR_B4": {"fiso": 0.1690, "fgeo": 0.0227, "fvol": 0.0574},
    "SR_B5": {"fiso": 0.3093, "fgeo": 0.0330, "fvol": 0.1535},
    "SR_B6": {"fiso": 0.3430, "fgeo": 0.0453, "fvol": 0.1154},
    "SR_B7": {"fiso": 0.2658, "fgeo": 0.0387, "fvol": 0.0639},
}

# https://www.sciencedirect.com/science/article/pii/S0034425717302791
# bands without provided values (red edge, B8A) estimated by
# linear interpolation by wavelength
BRDF_COEFFICIENTS_S2 = {
    "B2": {"fiso": 0.0774, "fgeo": 0.0079, "fvol": 0.0372},
    "B3": {"fiso": 0.1306, "fgeo": 0.0178, "fvol": 0.0580},
    "B4": {"fiso": 0.1690, "fgeo": 0.0227, "fvol": 0.0574},
    "B5": {"fiso": 0.2014, "fgeo": 0.0251, "fvol": 0.0796},
    "B6": {"fiso": 0.2313, "fgeo": 0.0273, "fvol": 0.1001},
    "B7": {"fiso": 0.2653, "fgeo": 0.0298, "fvol": 0.1234},
    "B8": {"fiso": 0.3093, "fgeo": 0.0330, "fvol": 0.1535},
    "B8A": {"fiso": 0.3106, "fgeo": 0.0335, "fvol": 0.1538},
    "B11": {"fiso": 0.3430, "fgeo": 0.0453, "fvol": 0.1154},
    "B12": {"fiso": 0.2658, "fgeo": 0.0387, "fvol": 0.0639},
}

# spectral mixture analysis defaults
N_ITERATIONS = 30
SHADE_NORMALIZE = True
RMSE = "RMSE"
WEIGHT = "WEIGHT"
