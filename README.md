# The Earth Library

`eli` is a spectral library and a set of software tools for satellite-base land cover mapping.

The spectral library contains several thousand unique spectral endmembers representing green vegetation, soil, non-photosynthetic vegetation, urban materials, and char. The reflectance cover the visible to the shortwave infrared (400-2450 nm) at 10 nm band widths.

The software tools resample these data to match the wavelenths of popular satellite and airborne earth observing sensors and to run spectral mixture analysis in Google Earth Engine via the `earthengine` python package.

This work is in development and has not yet been formally described. Soon, friends.

### Table of Contents

- [Installation](#installation)
- [Data Sources](#data-sources)
- [Contact](#contact)

# Installation

### via pip

This library can be installed via pip directly from Github.

```bash
pip install git+https://github.com/earth-chris/earthlib.git
```

You can also clone the source repository and install it locally.

```bash
git clone https://github.com/earth-chris/earthlib.git
cd earthlib
pip install . -r requirements.txt
```

### via conda

I recommend working with `earthlib` in `conda` (download from [here](https://docs.conda.io/en/latest/miniconda.html)). The `environment.yml` file in this repository contains a series of packages that are either required (`earthengine-api`) or just convenient (`jupyter`, `folium`) to have.

```bash
git clone https://github.com/earth-chris/earthlib.git
cd earthlib
conda env update
```

### using iPython defaults

If you're interested in using our custom `ipython` profile, which contains a few plotting defaults, you can set an environment variable to do this for you. From the base `earthlib` directory, run the following:

```bash
conda activate earthlib
conda env config vars set IPYTHONDIR=$PWD/ipython
```

# Data Sources

This package uses spectral library data from a range of sources. These include:

- [The Joint Fire Science Program](https://www.frames.gov/assessing-burn-severity/spectral-library/overview)
- World Agroforestry (ICRAF) Global [Soil Spectral Library](https://www.worldagroforestry.org/sd/landhealth/soil-plant-spectral-diagnostics-laboratory/soil-spectra-library)
- UCSB's [Urban Reflectance Spectra](https://ecosis.org/package/urban-reflectance-spectra-from-santa-barbara--ca)
- UW/BNL/NASA HySPIRI [airborne calibration spectra](https://ecosis.org/package/uw-bnl-nasa-hyspiri-airborne-campaign-leaf-and-canopy-spectra-and-trait-data)
- [USGS Spectral Library Version 7](https://www.sciencebase.gov/catalog/item/5807a2a2e4b0841e59e3a18d)
- Vegetation spectra modeled using [PROSAIL](http://teledetection.ipgp.jussieu.fr/prosail/) (using [PyPROSAIL](https://pyprosail.readthedocs.io/en/latest/))

# Contact

All (c) 2018+ [Christopher B. Anderson](mailto:cbanders@stanford.edu) & [Lingling Liu](mailto:lingling.liu@stanford.edu). This work is supported by the Stanford Center for Conservation Biology and the Natural Capital Project.
