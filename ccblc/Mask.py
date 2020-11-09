"""Functions for masking earth engine images
"""

class Clouds:
    def __init__(self):
        pass

    @staticmethod
    def Landsat8(img):
        # get the cloud mask bit corresponding to the qa band
        cloud_bit = 1
        cloud_bit_mask = 2 ** cloud_bit

        # label the cloudy pixels a la the selected bits
        mask = img.select("pixel_qa").bitwiseAnd(cloud_bit_mask).eq(0)

        # and apply the mask to the image
        return img.mask(mask)

    @staticmethod
    def Sentinel2(img):
        # get the cloud mask bit corresponding to the qa band
        cloud_bit = 10
        cloud_bit_mask = 2 ** cloud_bit

        # label the cloudy pixels
        mask = img.select("QA60").bitwiseAnd(cloud_bit_mask).eq(0)

        # and apply the mask to the image
        return img.mask(mask)
