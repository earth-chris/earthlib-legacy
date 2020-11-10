"""
Functions for interacting with earth engine map data in folium
"""


def addLayer(self, eeImage, visParams={}, name="Layer"):
    """
    Adds an earth engine image object to a folium map

    source: https://colab.research.google.com/github/google/earthengine-api/blob/master/python/examples/ipynb/ee-api-colab-setup.ipynb
    """
    import ee
    import folium

    map_id_dict = ee.Image(eeImage).getMapId(visParams)
    folium.raster_layers.TileLayer(
        tiles=map_id_dict["tile_fetcher"].url_format,
        attr="Map Data &copy; <a href='https://earthengine.google.com/'>Google Earth Engine</a>",
        name=name,
        overlay=True,
        control=True,
    ).add_to(self)
