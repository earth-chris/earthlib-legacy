"""Functions for reading specifically formatted data, mostly spectral libraries."""

import os

import numpy as np
import spectral

from earthlib.config import endmember_path


class Spectra:
    """Class for storing one or more reference spectra

    Attributes:
        band_centers: center wavelength for each band
        band_quantity: the quantity measured for each band
        band_unit: the unit of measurement (micrometers or nanometers)
        names: list of reference names for each spectra
        spectra: array of numerical spectral data
    """

    band_centers: np.array
    band_quantity: str
    band_unit: str
    names: list
    spectra: np.array

    def __init__(
        self,
        data: np.ndarray = None,
        names: list = None,
        n_spectra: int = 1,
        n_wavelengths: int = 2151,
        instrument: str = None,
        band_centers: np.ndarray = None,
        band_quantity: str = "Wavelength",
        band_unit: str = "Nanometers",
    ):
        """Read, store and write spectral data.

        Args:
            data: an array of spectral responses
                should be of shape (n_spectra, n_wavelengths)
            names: list of names to assign to each spectra
            n_spectra: the number of spectra included in the library
                this and n_wavelengths are ignored if `data` is passed
            n_wavelengths: the number of wavelengths for each spectrum
            instrument: the spectroradiometer name
            band_centers: the center wavelength for each band
            band_quantity: the quantity measured by each band
            band_unit: the unit of measurement (typically micrometers or nanometers)
        """
        # get shape parameters from the data itself
        if data is None:
            data = np.zeros([n_spectra, n_wavelengths])
        else:
            n_spectra, n_wavelengths = data.shape

        # set to asd type if no params set to change n_wl
        if n_wavelengths == 2151:
            instrument = "asd"

        # set up pre-defined types
        if instrument is not None:
            if instrument.lower() == "asd":
                n_wavelengths = 2151
                band_unit = "Nanometers"
                band_quantity = "Wavelength"
                band_centers = np.arange(350, 2501)

        # return a list same size as number of spectra
        if names is None:
            names = [f"Spectrum {i}" for i in range(n_spectra)]

        # store the outputs
        self.band_centers = band_centers
        self.band_quantity = band_quantity
        self.band_unit = band_unit
        self.names = names
        self.spectra = data

    def remove_water_bands(self, set_nan: bool = False) -> None:
        """Sets reflectance data from water absorption bands to eithr 0 or NaN.

        Wavelengths in the ranges of (1.35-1.46 um and 1.79-1.96 um) will be masked.
            Updates the self.spectra array in-place.

        Args:
            set_nan: set the water bands to NaN. False sets values to 0.
        """

        if set_nan:
            update_val = np.nan
        else:
            update_val = 0

        if self.band_unit.lower() == "micrometers":
            water_bands = [[1.35, 1.46], [1.79, 1.96]]
        else:
            water_bands = [[1350.0, 1460.0], [1790.0, 1960.0]]

        # start with nir-swir1 transition
        gt = np.where(self.band_centers > water_bands[0][0])
        lt = np.where(self.band_centers < water_bands[0][1])
        nd = np.intersect1d(gt[0], lt[0])
        self.spectra[:, nd] = update_val
        self.band_centers = np.delete(self.band_centers, nd)

        # then swir1-swir2 transition
        gt = np.where(self.band_centers > water_bands[1][0])
        lt = np.where(self.band_centers < water_bands[1][1])
        nd = np.intersect1d(gt[0], lt[0])
        self.spectra[:, nd] = update_val
        self.band_centers = np.delete(self.band_centers, nd)

    def get_shortwave_bands(self) -> np.ndarray:
        """Returns indices of the bands that encompass the shortwave range.

        This refers to the range (350 - 2500 nm).

        Returns:
            an index of bands to subset to the shortwave range.
        """

        # set range to return in nanometers
        shortwave_range = [350.0, 2500.0]

        # normalize if wavelength units are different
        if self.band_unit.lower() == "micrometers":
            shortwave_range /= 1000.0

        # find overlapping range
        gt = np.where(self.band_centers > shortwave_range[0])
        lt = np.where(self.band_centers < shortwave_range[1])
        overlap = np.intersect1d(gt[0], lt[0])

        # return output
        return overlap

    def bn(self, inds: list = None) -> None:
        """Brightness normalizes the spectra.

        Updates the self.spectra array in-place.

        Args:
            inds: the band indices to use for normalization.
        """
        # check if indices were set and valid. if not, use all bands
        if inds:
            if max(inds) > self.spectra.shape[-1]:
                inds = range(0, self.spectra.shape[-1])
                warn("Invalid range set. using all spectra")

            if min(inds) < 0:
                inds = range(0, self.spectra.shape[-1])
                warn("Invalid range set. using all spectra")

        else:
            inds = range(0, self.spectra.shape[-1])

        # perform the bn
        self.spectra = self.spectra[:, inds] / np.expand_dims(
            np.sqrt((self.spectra[:, inds] ** 2).sum(1)), 1
        )

        # subset band centers to the indices selected, if they exist
        if self.band_centers.ndim != 0:
            self.band_centers = self.band_centers[inds]

    def write_sli(
        self, path: str, row_inds: list = None, spectral_inds: list = None
    ) -> None:
        """Writes the spectral object to an ENVI spectral library file.

        Args:
            path: the output file to write the array to.
            row_inds: the row-wise indices of the array to write.
            spectral_inds: indices for which spectral to write
        """

        # set up the output file names for the library and the header
        base, ext = os.path.splitext(path)
        if ext.lower() == ".sli":
            osli = path
            ohdr = "{}.hdr".format(base)
        elif ext.lower() == ".hdr":
            osli = "{}.hdr".format(base)
            ohdr = path
        else:
            osli = "{}.sli".format(base)
            ohdr = "{}.hdr".format(base)

        # subset the data if specific indices are set
        spectra = self.spectra
        names = self.names
        band_centers = self.band_centers

        if row_inds is not None:
            spectra = spectra[row_inds, :]
            names = np.array(names)[row_inds]

        if spectral_inds is not None:
            spectra = spectra[:, spectral_inds]
            band_centers = band_centers[spectral_inds]

        # set up the metadata for the ENVI header file
        metadata = {
            "samples": len(band_centers),
            "lines": len(names),
            "bands": 1,
            "data type": 4,
            "header offset": 0,
            "interleave": "bsq",
            "byte order": 0,
            "sensor type": "earthlib",
            "spectra names": names,
            "wavelength units": self.band_unit,
            "wavelength": band_centers,
        }
        spectral.envi.write_envi_header(ohdr, metadata, is_library=True)

        # then write the spectral library
        with open(osli, "w") as f:
            spectra.astype(np.float32).tofile(f)


def spectralLibrary(path: str) -> Spectra:
    """Reads an ENVI-format spectral library into memory.

    Args:
        path: file path to the ENVI spectral library file. Looks for a .hdr sidecar file.

    Returns:
        an earthlib Spectra with the spectral library data.
    """

    # get the header file path
    if check_file(path[:-4] + ".hdr"):
        hdr = path[:-4] + ".hdr"
    else:
        if check_file(path + ".hdr"):
            hdr = path + ".hdr"
        else:
            return None

    slib = spectral.envi.open(hdr, path)
    s = Spectra(
        data=slib.spectra,
        names=slib.names,
        band_centers=np.asarray(slib.bands.centers),
        band_unit=slib.bands.band_unit,
        band_quantity=slib.bands.band_quantity,
    )

    return s


def endmembers() -> Spectra:
    """Reads the earthlib spectral endmember library into memory.

    Returns:
        an earthlib Spectra class with the endmember library reflectance data.
    """
    return spectralLibrary(endmember_path)


def jfsp(path: str) -> Spectra:
    """Reads JFSP-formatted ASCII files.

    Reads the ASCII format spectral data from the joint-fire-science-program
        and returns an object with the mean and +/- standard deviation reflectance.
        https://www.frames.gov/assessing-burn-severity/spectral-library/overview

    Args:
        path: file path to the JFSP spectra text file.

    Returns:
        an earthlib Spectra with the JFSP reflectance data.
    """

    # create the spectral object
    s = spectralObject(n_spectra=1, instrument="asd")
    s.spectra_stdevm = np.zeros(s.spectra.shape)
    s.spectra_stdevp = np.zeros(s.spectra.shape)

    # open the file and read the data
    with open(path, "r") as f:
        f.readline()
        for i, line in enumerate(f):
            line = line.strip().split()
            s.spectra[0, i] = line[1]
            s.spectra_stdevp[0, i] = line[2]
            s.spectra_stdevm[0, i] = line[3]

        return s


def usgs(path: str) -> Spectra:
    """Reads USGS-formatted ASCII files.

    Reads ascii spectral data from USGS-format files and returns
        the mean and +/- standard deviation.
        https://www.sciencebase.gov/catalog/item/5807a2a2e4b0841e59e3a18d

    Args:
        path: file path the the USGS spectra text file.

    Returns:
        an earthlib Spectra with the USGS reflectance data.
    """

    # open the file and read header info
    with open(path, "r") as f:
        x_start = "gibberish"
        for line in f:
            if x_start in line:
                break
            if "Name:" in line:
                spectrum_name = line.strip().split("Name:")[-1].strip()
            if "X Units:" in line:
                band_unit = line.strip().split()
                band_unit = band_unit[-1].strip("()").capitalize()
            if "Y Units:" in line:
                refl_unit = line.strip().split()
                refl_unit = refl_unit[-1].strip("()").capitalize()
            if "First X Value:" in line:
                x_start = line.strip().split()[-1]
            if "Number of X Values:" in line:
                n_values = int(line.strip().split()[-1])

        # now that we got our header info, create the arrays
        band_centers = np.empty(n_values)
        reflectance = np.empty(n_values)

        line = line.strip().split()
        band_centers[0] = float(line[0])
        reflectance[0] = float(line[1])

        # resume reading through file
        i = 1
        for line in f:
            line = line.strip().split()
            band_centers[i] = float(line[0])
            reflectance[i] = float(line[1])
            i += 1

        # some files read last -> first wavelength
        if band_centers[0] > band_centers[-1]:
            band_centers = band_centers[::-1]
            reflectance = reflectance[::1]

        # convert units to nanometers and scale 0-1
        if band_unit.lower() == "micrometers":
            band_centers *= 1000.0
            band_unit = "Nanometers"

        if refl_unit.lower() == "percent":
            reflectance /= 100.0

        # create the spectral object
        s = Spectra(
            n_spectra=1,
            n_wavelengths=n_values,
            band_centers=band_centers,
            band_unit=band_unit,
            band_quantity="Wavelength",
        )

        # assign relevant values
        s.spectra[0] = reflectance
        if spectrum_name:
            s.names[0] = spectrum_name

    return s


def check_file(path: str) -> bool:
    """Verifies whether a file exists and can be read.

    Args:
        path: the file path to check.

    Returns:
        file status.
    """
    return os.path.isfile(path) and os.access(path, os.R_OK)
