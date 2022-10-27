from earthlib import (
    BRDFCorrect,
    BrightMask,
    CloudMask,
    NIRv,
    Scale,
    ShadeMask,
    ThresholdMask,
    Unmix,
    __version__,
    read,
)
from earthlib.config import collections, metadata
from earthlib.utils import (
    getBands,
    getCollection,
    getScaler,
    listSensors,
    listTypes,
    selectSpectra,
)

# expose the full spectral library
library = read.endmembers()
