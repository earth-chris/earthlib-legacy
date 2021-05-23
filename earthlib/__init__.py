from . import Map, Mask, Read, Unmix, __version__
from .utils import (
    getBands,
    getCollection,
    getScaler,
    listSensors,
    listTypes,
    metadata,
    selectSpectra,
)

# expose the full spectral library
library = Read.endmembers()
