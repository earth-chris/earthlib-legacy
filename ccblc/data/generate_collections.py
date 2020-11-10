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
            "B1",
            "B2",
            "B3",
            "B4",
            "B5",
            "B6",
            "B7",
            "B10",
            "B11",
        ],
        "band_descriptions": [
            "ultra blue",
            "blue",
            "green",
            "red",
            "near infrared",
            "shortwave infrared 1",
            "shortwave infrared 2",
        ],
        "band_centers": [0.443, 0.482, 0.561, 0.655, 0.865, 1.609, 2.201],
        "band_widths": [0.016, 0.060, 0.057, 0.037, 0.028, 0.085, 0.187],
    }
}


# write the output file
with open(output_path, "w+") as f:
    f.write(json.dumps(collections, indent=2, sort_keys=True))
