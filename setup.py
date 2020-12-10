from setuptools import setup

version = open("earthlib/__version__.py").read().strip('"\n')

setup_args = {
    "name": "earthlib",
    "version": version,
    "url": "https://github.com/earth-chris/earthlib",
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
    "packages": ["earthlib"],
    "include_package_data": True,
    "platforms": "any",
    "data_files": [
        (
            "earthlib",
            [
                "earthlib/data/spectra.csv",
                "earthlib/data/spectra.sli",
                "earthlib/data/spectra.sli.hdr",
                "earthlib/data/collections.json",
            ],
        )
    ],
    "install_requires": ["folium", "matplotlib", "numpy", "pandas", "spectral"],
}

setup(**setup_args)
