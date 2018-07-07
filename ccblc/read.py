"""
"""
import os as _os
import numpy as _np
import spectral as _spectral
import matplotlib.pyplot as _plt


# set up class for spectral objects
class _spectralObject:
    def __init__(self, n_spectra=1, n_wl=2151, sensor=None, band_unit=None,
            band_quantity=None, band_centers=None):
        
        # set to asd type if no params set to change n_wl
        if n_wl == 2151:
            sensor = 'asd'
        
        # set up pre-defined types
        if sensor is not None:
            if sensor.lower() == 'asd':
                n_wl = 2151
                band_unit = 'Nanometers'
                band_quantity = 'Wavelength'
                band_centers = _np.arange(350, 2501)
        
        # return a list same size as number of spectra
        self.names = []
        for i in range(n_spectra):
            self.names.append('Spectrum {}'.format(i))
        
        # set up the band definitions
        try:
            self.band_unit = band_unit
        except NameError:
            self.band_unit = None
        try:
            self.band_quantity = band_quantity
        except NameError:
            self.band_quantity = None
        try:
            self.band_centers = band_centers
        except NameError:
            self.band_centers = None
        
        # return an _np array size of n spectra x n wavelengths
        self.spectra = _np.zeros([n_spectra, n_wl])
        
    def remove_water_bands(self, set_nan=True):
        """sets reflectance data from water absorption bands
        (i.e. 1350 - 1460 nm and 1790 - 1960 nm) to NaN (or 0)
        
        Args:
            set_nan: set this to true to set the water bands to NaN. False sets to 0
        
        Returns:
            None. updates the self.spectra array
        """
        if set_nan:
            update_val = _np.nan
        else:
            update_val = 0
            
        if self.band_unit == 'micrometers':
            water_bands = [[1.35, 1.46], [1.79, 1.96]]
        else:
            water_bands = [[1350.0, 1460.0], [1790.0, 1960.0]]
        
        # start with nir-swir1 transition
        gt = _np.where(self.band_centers > water_bands[0][0])
        lt = _np.where(self.band_centers < water_bands[0][1])
        nd = _np.intersect1d(gt[0], lt[0])
        self.spectra[:,nd] = update_val
        
        # then swir1-swir2 transition
        gt = _np.where(self.band_centers > water_bands[1][0])
        lt = _np.where(self.band_centers < water_bands[1][1])
        nd = _np.intersect1d(gt[0], lt[0])
        self.spectra[:,nd] = update_val
    
    def get_shortwave_bands(self):
        """returns an index of the bands that encompass
        the shortwave range (350 - 2500 nm)
        
        Args:
            None
        
        Returns: 
            overlap: an index of bands to subset to the shortwave range
        """
        # set range to return in nanometers
        shortwave_range = [350., 2500.]
        
        # normalize if wavelength units are different
        if self.band_unit == 'Micrometers':
            shortwave_range /= 1000.
            
        # find overlapping range
        gt = _np.where(self.band_centers > shortwave_range[0])
        lt = _np.where(self.band_centers < shortwave_range[1])
        overlap = _np.intersect1d(gt[0], lt[0])
        
        # return output
        return overlap
        
    def plot(self, inds = None, legend = False):
        """plots the spectra using a standard plot format
        
        usage: self.plot(inds = [], legend = False)
          where inds = optional 0-based indices for spectra to plot
                legend = set this to force a legend to be created
        """
        
        # set basic parameters
        _plt.xlim((self.band_centers.min(), self.band_centers.max()))
        _plt.xlabel('Wavelength ({})'.format(self.band_unit))
        _plt.ylabel('Reflectance (%)')
        
        # check if indices were set and valid. if not, plot all items
        if inds is not None:
            if _np.max(inds) > len(self.names):
                inds = range(0, len(self.names))
                print("[ ERROR! ]: invalid range set. using all spectra")
            if _np.min(inds) < 0:
                inds = range(0, len(self.names))
                print("[ ERROR! ]: invalid range set. using all spectra")
        else:
            inds = range(0, len(self.names))
            
        # plot differently if a single index or a list is passed
        # loop through each item to plot
        if type(inds) is list:
            for i in inds:
                _plt.plot(self.band_centers, self.spectra[i,:], 
                          label = self.names[i])
        else:
            _plt.plot(self.band_centers, self.spectra[inds,:], 
                label = self.names[inds])
            
        # add the legend with each spectrum's name
        if legend:
            _plt.legend(fontsize = 'small', framealpha = 0.5, 
                fancybox = True)
        
        # display the plot
        _plt.tight_layout()
        _plt.show()
        
    def bn(self, inds=None):
        """brightness normalizes the spectra
        
        Args:
            inds: the indices to use for BN
            
        Returns:
            None. Updates the self.spectra array
        """
        # check if indices were set and valid. if not, use all bands
        if inds:
            if max(inds) > self.spectra.shape[-1]:
                inds = range(0, self.spectra.shape[-1])
                print("[ ERROR ]: invalid range set. using all spectra")
            if min(inds) < 0:
                inds = range(0, self.spectra.shape[-1])
                print("[ ERROR ]: invalid range set. using all spectra")
        else:
            inds = range(0, self.spectra.shape[-1])
            
        # perform the bn
        self.spectra = self.spectra[:,inds] / _np.expand_dims(
            _np.sqrt((self.spectra[:,inds]**2).sum(1)),1)
        
        # subset band centers to the indices selected, if they exist
        if self.band_centers.ndim != 0:
            self.band_centers = self.band_centers[inds]
            
    def write_sli(self, outfile, row_inds=None, spectral_inds=None):
        """writes the spectral object to an envi spectral library
        
        Args:
            outfile: the output file to write the array to
            inds: the row-wise indices of the array to write out
            
        Returns:
            None. Writes the data to disk
        """
        # set up the output file names for the library and the header
        base, ext = _os.path.splitext(outfile)
        if ext.lower() == '.sli':
            osli = outfile
            ohdr = '{}.hdr'.format(base)
        elif ext.lower() == '.hdr':
            osli = '{}.hdr'.format(base)
            ohdr = outfile
        else:
            osli = '{}.sli'.format(base)
            ohdr = '{}.hdr'.format(base)
        
        # subset the data if specific indices are set
        spectra = self.spectra
        names = self.names
        band_centers = self.band_centers
        
        if row_inds is not None:
            spectra = spectra[row_inds, :]
            names = _np.array(names)[row_inds]
        
        if spectral_inds is not None:
            spectra = spectra[:, spectral_inds]
            band_centers = band_centers[spectral_inds]
            
        # set up the metadata for the ENVI header file 
        metadata = {
            'samples' : len(band_centers),
            'lines' : len(names),
            'bands' : 1,
            'data type' : 4,
            'header offset' : 0,
            'interleave' : 'bsq',
            'byte order' : 0,
            'sensor type' : 'ccblc',
            'spectra names' : names,
            'wavelength units' : self.band_unit,
            'wavelength' : band_centers
            }
        _spectral.envi.write_envi_header(ohdr, metadata, is_library=True)
        
        # then write the spectral library
        with open(osli, 'w') as f: 
            spectra.astype(_np.float32).tofile(f)


# function for checking if a file exists and is readable
def check_file(infile, quiet=False):
    """Checks if a file exists and can be read
    
    Args:
        infile: the path to the file to check
        quiet : a flag to suppress a warning message
    """
    if _os.path.isfile(infile) and _os.access(infile, _os.R_OK):
        return True
    else:
        if not quiet:
            print("[ ERROR! ]: Unable to read file: {}".format(infile))
        return False
            

# function to read ascii spectra from the joint fire science program
#  (https://www.frames.gov/partner-sites/assessing-burn-severity/spectral/spectral-library-southern-california/)
def jfsc(infile):
    """reads the ascii format spectral data from the joint-fire-science-program
    and returns an object with the mean and +/- standard deviation reflectance data
    
    Args:
        infile:
        
    Returns:
        a ccblc spectralObject with the jfsp reflectance data
    """

    # create the spectral object
    s = _spectralObject(1, type='asd')
    s.spectra_stdevm = _np.zeros(s.spectra.shape)
    s.spectra_stdevp = _np.zeros(s.spectra.shape)

    # open the file and read the data
    with open(infile, 'r') as f:
        header = f.readline()
        i = 0
        for line in f:
            line = line.strip().split()
            s.spectra[0, i] = line[1]
            s.spectra_stdevp[0, i] = line[2]
            s.spectra_stdevm[0, i] = line[3]
            i += 1
    
        # return the spectral object
        return s
        

# function to read an envi spectral library file
def spectral_library(infile):
    """reads an envi format spectral library
    
    Args:
        infile: the envi spectral library file (looks for an accompanying .hdr)
        
    Returns:
        a ccblc spectralObject with the spectral library data
    """
    # check for header files
    if check_file(infile[:-4] + '.hdr', quiet=True):
        hdr = infile[:-4] + '.hdr'
    else:
        if check_file(infile + '.hdr'):
            hdr = infile + '.hdr'
        else:
            return -1
    
    # read the spectral data
    slib = _spectral.envi.open(hdr, infile)
    
    # create the spectral object
    s = _spectralObject(slib.params.nrows, slib.params.ncols,
                       band_centers=_np.asarray(slib.bands.centers),
                       band_unit=slib.bands.band_unit,
                       band_quantity=slib.bands.band_quantity)
    
    # set the spectra and names        
    s.spectra = slib.spectra
    s.names = slib.names
    
    # return the final object
    return s
