"""Functions for masking imagery
"""

# masking clouds in landsat collection data
def clouds_landsat(img):
    """"""
    # get the cloud mask bit corresponding to the qa band
    cloud_bit = 1
    cloud_bit_mask = 2 ** cloud_bit

    # label the cloudy pixels a la the selected bits
    mask = img.select("pixel_qa").bitwiseAnd(cloud_bit_mask).eq(0)

    # and apply the mask to the image
    return img.mask(mask)


# masking clouds in sentinel-2 data
def clouds_sentinel(img):
    """"""
    # get the cloud mask bit corresponding to the qa band
    cloud_bit = 10
    cloud_bit_mask = 2 ** cloud_bit

    # label the cloudy pixels
    mask = img.select("QA60").bitwiseAnd(cloud_bit_mask).eq(0)

    # and apply the mask to the image
    return img.mask(mask)


# masking cirrus in sentinel-2 data
def cirrus_sentinel(img):
    """"""
    # get the cirrus mask bit corresponding to the qa band
    cirrus_bit = 10
    cirrus_bit_mask = 2 ** cirrus_bit

    # label the cirrus pixels
    mask = img.select("QA60").bitwiseAnd(cirrus_bit_mask).eq(0)

    # and apply the mask to the image
    return img.mask(mask)
