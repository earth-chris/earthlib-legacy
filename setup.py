from setuptools import setup

version = open("earthlib/__version__.py").read().strip('"\n')
long_description = open("README.md", "r", encoding="utf-8").read()
requirements = open("requirements.txt", "r", encoding="utf-8").read().strip().split()

setup_args = {
    "name": "earthlib",
    "version": version,
    "url": "https://github.com/earth-chris/earthlib",
    "license": "MIT",
    "author": "Christopher Anderson",
    "author_email": "cbanders@stanford.edu",
    "description": "Spectral unmixing library for satellite land cover mapping",
    "long_description": long_description,
    "long_description_content_type": "text/markdown",
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
    "install_requires": requirements,
    "python_requires": ">=3.4",
    "classifiers": [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
}

setup(**setup_args)
