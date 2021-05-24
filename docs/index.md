# The Earth Library

![earthlib unmixed](img/earth-unmixed.png)

---

**Documentation**: [earth-chris.github.io/earthlib](https://earth-chris.github.io/earthlib)

**Source code**: [earth-chris/earthlib](https://github.com/earth-chris/earthlib)

---

# Introduction

`earthlib` is a spectral library and a set of software tools for satellite-base land cover mapping.

The spectral library contains several thousand unique spectral endmembers representing green vegetation, soil, non-photosynthetic vegetation, urban materials, and char. The reflectance data cover the visible to the shortwave infrared wavelengths (400-2450 nm) at 10 nm band widths.

The software tools i) resample these data to match the wavelenths of popular satellite and airborne earth observing sensors and ii) run spectral mixture analysis in Google Earth Engine via the `earthengine` python package.

The goal is to quantify spatial and temporal patterns of change in global vegetation cover, as well as patterns of soil cover, burned area, non-photosynthetic vegetation, and impervious surfaces. With `earthlib`, you can do this using any satellite data source.

This work is still in active development.

### Table of Contents

- [Spectral mixture analysis](#spectral-mixture-analysis)
- [Installation](#installation)
- [Contact](#contact)


# Spectral mixture analysis

The contents of a satellite image pixel are rarely homogeneous. An area 30x30m in size can include buildings, trees, and roads in urban environments; grasses, soils, and char in recently burned landscapes; trees, gaps, and downed logs in forested areas. These patterns all affect the reflectance patterns measured by satellites, and it's important to be able to estimate the sub-pixel abundances of each of these land cover types.

![earthlib spectral mixture analysis](img/sma-basics.png)

Spectral mixture analysis is an approach to estimating the sub-pixel contents of an image pixel based on a set of representaive reflectance spectra (i.e., a reference library). Linear spectral mixture analysis uses an iterative, least-squares fitting approach to estimate the proportions of land cover types based on observed reflectance measurements. In order to run these analyses, you need 1) a high quality reference library of different land cover types, and 2) to resample these reference data to the wavelengths of the instrument you plan to analyze.

To support these analysise, `earthlib` provides a rich spectral library with thousands of [labeled reference spectra](sources.md) and tools for working with common satellite instruments.


# Installation

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

### conda

I recommend working with `earthlib` in `conda` (download from [here](https://docs.conda.io/en/latest/miniconda.html)). The `environment.yml` file in this repository contains a series of packages that are either required (`earthengine-api`) or just convenient (`jupyter`, `folium`) to have.

```bash
git clone https://github.com/earth-chris/earthlib.git
cd earthlib
conda env update
```

Once the environment has been created, you can activate it with `conda activate earthlib`.


# Contact

All (c) 2018+ [Christopher B. Anderson](mailto:cbanders@stanford.edu) & [Lingling Liu](mailto:lingling.liu@stanford.edu). This work is supported by the Stanford Center for Conservation Biology and the Natural Capital Project.
