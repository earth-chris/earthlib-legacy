"""
A script to create a formatted json file with sensor/collection parameters
"""
import json

# set the output file path
output_path = "collections.json"

# create the dictionary to write as json
collections = {
    # from http://www.gisagmaps.com/landsat-8-sentinel-2-bands/
    "Landsat8": {
        "collection": "LANDSAT/LC08/C01/T1_SR",
        "band_names": [
            "B2",
            "B3",
            "B4",
            "B5",
            "B6",
            "B7",
        ],
        "band_descriptions": [
            "blue",
            "green",
            "red",
            "near infrared",
            "shortwave infrared 1",
            "shortwave infrared 2",
        ],
        "band_centers": [0.482, 0.561, 0.655, 0.865, 1.609, 2.201],
        "band_widths": [0.060, 0.057, 0.037, 0.028, 0.085, 0.187],
        "scale": 0.0001,
    },
    # from http://www.gisagmaps.com/landsat-8-sentinel-2-bands/
    "Sentinel2": {
        "collection": "COPERNICUS/S2_SR",
        "band_names": [
            "B2",
            "B3",
            "B4",
            "B5",
            "B6",
            "B7",
            "B8",
            "B8A",
            "B11",
            "B12",
        ],
        "band_descriptions": [
            "blue",
            "green",
            "red",
            "red edge 1",
            "red edge 2",
            "red edge 3",
            "near infrared",
            "red edge 4",
            "shortwave infrared 1",
            "shortwave infrared 2",
        ],
        "band_centers": [
            0.494,
            0.560,
            0.665,
            0.704,
            0.740,
            0.781,
            0.834,
            0.864,
            1.612,
            2.194,
        ],
        "band_widths": [
            0.095,
            0.045,
            0.039,
            0.020,
            0.018,
            0.028,
            0.141,
            0.033,
            0.142,
            0.240,
        ],
        "scale": 0.0001,
    },
    "MODIS": {
        "collection": "MODIS/006/MOD09GA",
        "band_names": [
            "sur_refl_b03",
            "sur_refl_b04",
            "sur_refl_b01",
            "sur_refl_b02",
            "sur_refl_b05",
            "sur_refl_b06",
            "sur_refl_b07",
        ],
        "band_descriptions": [
            "blue",
            "green",
            "red",
            "near infrared",
            "near infrared 2",
            "shortwave infrared 1",
            "shortwave infrared 2",
        ],
        "band_centers": [
            0.469,
            0.555,
            0.645,
            0.858,
            1.240,
            1.640,
            2.130,
        ],
        "band_widths": [0.020, 0.020, 0.050, 0.035, 0.020, 0.024, 0.050],
        "scale": 0.0001,
    },
}


# write the output file
with open(output_path, "w+") as f:
    f.write(json.dumps(collections, indent=2, sort_keys=True))
