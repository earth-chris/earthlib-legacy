# The Earth Library

<img src="docs/figures/earth-unmixed.png">

`earthlib` is a spectral library and a set of software tools for satellite-base land cover mapping.

The spectral library contains several thousand unique spectral endmembers representing green vegetation, soil, non-photosynthetic vegetation, urban materials, and char. The reflectance data cover the visible to the shortwave infrared wavelengths (400-2450 nm) at 10 nm band widths.

The software tools i) resample these data to match the wavelenths of popular satellite and airborne earth observing sensors and ii) run spectral mixture analysis in Google Earth Engine via the `earthengine` python package. The goal is to quantify spatial and temporal patterns of change in global vegetation cover, as well as patterns of soil cover, burned area, non-photosynthetic vegetation, and impervious surfaces. With `earthlib`, you can do this using any satellite data source.

This work is still in development and has not yet been formally described.

### Table of Contents

- [Installation](#installation)
- [Data Sources](#data-sources)
- [Contact](#contact)

# Installation

### via pip

This library can be installed via `pip`.

```bash
pip install earthlib
```

You can also clone the source repository and install it locally.

```bash
git clone https://github.com/earth-chris/earthlib.git
cd earthlib
pip install -e .
```

### via conda

I recommend working with `earthlib` in `conda` (download from [here](https://docs.conda.io/en/latest/miniconda.html)). The `environment.yml` file in this repository contains a series of packages that are either required (`earthengine-api`) or just convenient (`jupyter`, `folium`) to have.

```bash
git clone https://github.com/earth-chris/earthlib.git
cd earthlib
conda env update
```

Once the environment has been created, you can activate it with `conda activate earthlib`.


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
