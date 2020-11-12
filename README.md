# CCB-LC

The Stanford Center for Conservation Biology's Land Cover mapping system.

This work is in early production and has not yet been formally described. Soon, friends.

### Table of Contents

- [Installation](#installation)
- [Data Sources](#data-sources)
- [Contact](#contact)

# Installation

### via pip

This library can be installed via pip directly from Github.

```bash
pip install git+https://github.com/earth-chris/ccb-lc.git
```

You can also clone the source repository and install it locally.

```bash
git clone https://github.com/earth-chris/ccb-lc.git
cd ccb-lc
pip install . -r requirements.txt
```

### via conda

I recommend working with `ccblc` in `conda` (download from [here](https://docs.conda.io/en/latest/miniconda.html)). The `environment.yml` file in this repository contains a series of packages that are either required (`earthengine-api`) or just convenient (`jupyter`, `folium`) to have.

```bash
git clone https://github.com/earth-chris/ccb-lc.git
cd ccb-lc
conda env update
```

### using iPython defaults

If you're interested in using the ccb default `ipython` profile, which contains a few plotting defaults, you can set an environment variable to do this for you. From the base `ccb-lc` directory, run the following:

```bash
conda activate ccblc
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

All (c) 2018+ Christopher B. Anderson

- [E-mail](mailto:cbanders@stanford.edu)
- [Google Scholar](https://scholar.google.com/citations?user=LoGxS40AAAAJ&hl=en)
- [Personal website](https://earth-chris.github.io/)
