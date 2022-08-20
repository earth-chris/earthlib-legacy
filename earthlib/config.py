"""Default configuration parameters for preprocessing routines"""

# https://www.sciencedirect.com/science/article/pii/S0034425716300220
BRDF_COEFFICIENTS_L457 = {
    "B1": {"fiso": 0.0774, "fgeo": 0.0079, "fvol": 0.0372},
    "B2": {"fiso": 0.1306, "fgeo": 0.0178, "fvol": 0.0580},
    "B3": {"fiso": 0.1690, "fgeo": 0.0227, "fvol": 0.0574},
    "B4": {"fiso": 0.3093, "fgeo": 0.0330, "fvol": 0.1535},
    "B5": {"fiso": 0.3430, "fgeo": 0.0453, "fvol": 0.1154},
    "B7": {"fiso": 0.2658, "fgeo": 0.0387, "fvol": 0.0639},
}
BRDF_COEFFICIENTS_L8 = {
    "B2": {"fiso": 0.0774, "fgeo": 0.0079, "fvol": 0.0372},
    "B3": {"fiso": 0.1306, "fgeo": 0.0178, "fvol": 0.0580},
    "B4": {"fiso": 0.1690, "fgeo": 0.0227, "fvol": 0.0574},
    "B5": {"fiso": 0.3093, "fgeo": 0.0330, "fvol": 0.1535},
    "B6": {"fiso": 0.3430, "fgeo": 0.0453, "fvol": 0.1154},
    "B7": {"fiso": 0.2658, "fgeo": 0.0387, "fvol": 0.0639},
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
