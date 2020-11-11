"""
Functions for masking earth engine images
"""


def Landsat8(img):
    import ee

    cloudShadowBitMask = ee.Number(2).pow(3).int()
    cloudsBitMask = ee.Number(2).pow(5).int()
    qa = img.select("pixel_qa")
    mask = (
        qa.bitwiseAnd(cloudShadowBitMask).eq(0).And(qa.bitwiseAnd(cloudsBitMask).eq(0))
    )
    return img.mask(mask)


def Sentinel2(img):
    import ee

    # get the cloud mask bit corresponding to the qa band
    cloud_bit = 10
    cloud_bit_mask = 2 ** cloud_bit

    # label the cloudy pixels
    mask = img.select("QA60").bitwiseAnd(cloud_bit_mask).eq(0)

    # and apply the mask to the image
    return img.mask(mask)
