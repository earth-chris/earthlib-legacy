"""Functions for interacting with earth engine map data in folium."""

import ee as _ee
import folium as _folium


def addLayer(self, eeImage, visParams={}, name="Layer"):
    """Adds an earth engine image object to a folium map.

    This function is designed to be appended to a folium `map` object.
        source: https://colab.research.google.com/github/google/earthengine-api/blob/master/python/examples/ipynb/ee-api-colab-setup.ipynb

    Args:
        eeImage: an ee image object.
        visParams: dictionary of ee visualization parameters.
        name: the name to display in the map legend.

    Returns:
        None. Updates the `map` object this function is appended to.
    """

    map_id_dict = _ee.Image(eeImage).getMapId(visParams)

    _folium.raster_layers.TileLayer(
        tiles=map_id_dict["tile_fetcher"].url_format,
        attr="Map Data &copy; <a href='https://earthengine.google.com/'>Google Earth Engine</a>",
        name=name,
        overlay=True,
        control=True,
    ).add_to(self)
