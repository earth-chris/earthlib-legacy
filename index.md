# The Earth Library

![earthlib unmixed](img/earth-unmixed.png)

<p align="center">
  <em>A global reference library for land cover spectra, and tools for working with it.</em>
</p>

![GitHub](https://img.shields.io/github/license/earth-chris/earthlib)
![PyPI](https://img.shields.io/pypi/v/earthlib)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/earth-chris/earthlib/run-pytest)
![PyPI - Downloads](https://img.shields.io/pypi/dm/earthlib)
![GitHub last commit](https://img.shields.io/github/last-commit/earth-chris/earthlib)


---

**Documentation**: [earth-chris.github.io/earthlib](https://earth-chris.github.io/earthlib)

**Source code**: [earth-chris/earthlib](https://github.com/earth-chris/earthlib)

---

## Introduction

`earthlib` is a spectral library and a set of software tools for satellite-base land cover mapping.

The library contains several thousand unique spectral endmembers representing green vegetation, soil, non-photosynthetic vegetation, urban materials, and burned materials. The reflectance data cover the visible to the shortwave infrared wavelengths (400-2450 nm) at 10 nm band widths.

The software tools (1) resample these data to match the wavelenths of popular satellite and airborne earth observing sensors and (2) run [spectral mixture analysis](introduction.md) in Google Earth Engine via the `earthengine` python package.

The goal is to quantify spatial and temporal patterns of change in global vegetation cover, as well as patterns of soil cover, burned area, non-photosynthetic vegetation, and impervious surfaces. With `earthlib`, you can do this using most public satellite [data sources](sources.md).


## Installation

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

---

## Developed by

[Christopher Anderson](https://cbanderson.info)

<a href="https://twitter.com/earth_chris">![Twitter Follow](https://img.shields.io/twitter/follow/earth_chris)</a>
<a href="https://github.com/earth-chris">![GitHub Stars](https://img.shields.io/github/stars/earth-chris?affiliations=OWNER%2CCOLLABORATOR&style=social)</a>

This work was supported by the Stanford Center for Conservation Biology and the Natural Capital Project.
