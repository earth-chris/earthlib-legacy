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
    "keywords": ["ecology", "conservation", "remote sensing", "earth engine", "spectral unmixing"],
    "packages": ["ccblc"],
    "include_package_data": True,
    "platforms": "any",
    "data_files": [("ccblc", ["ccblc/data/Branner.csv", "ccblc/data/Branner.sli", "ccblc/data/Branner.sli.hdr"])],
}

setup(**setup_args)
