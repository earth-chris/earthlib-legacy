from setuptools import setup

version = open("ccblc/__version__.py").read().strip('"\n')

setup_args = {
    "name": "ccblc",
    "version": version,
    "url": "https://github.com/earth-chris/ccb-lc",
    "license": "MIT",
    "author": "Christopher Anderson",
    "author_email": "cbanders@stanford.edu",
    "description": "Spectral unmixing package for land cover mapping",
    "keywords": [
        "ecology",
        "conservation",
        "remote sensing",
        "earth engine",
        "spectral unmixing",
    ],
    "packages": ["ccblc"],
    "include_package_data": True,
    "platforms": "any",
    "data_files": [
        (
            "ccblc",
            [
                "ccblc/data/spectra.csv",
                "ccblc/data/spectra.sli",
                "ccblc/data/spectra.sli.hdr",
                "ccblc/data/collections.json",
            ],
        )
    ],
    "install_requires": ["folium", "matplotlib", "numpy", "pandas", "spectral"],
}

setup(**setup_args)
