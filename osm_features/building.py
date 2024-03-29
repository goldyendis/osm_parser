from osmium.osm import OSMObject

from manipulation.manipulate_geodataframe import MyGeoDataFrame
from osm_features.abstract.super_osm_feature import AbstractOSM
import geopandas as gpd


class OSMAreaBuilding(AbstractOSM):
    """Processor of the Building Area OSM Entities. Splitting the created GeoDataframes to multiple files. Each file
     contain 100K row"""

    def __init__(self, osm_feature: OSMObject, key_tag: str, count: int = None) -> None:
        self.dataframe = MyGeoDataFrame(osm_feature, key_tag)
        super(OSMAreaBuilding, self).__init__(dataframe=self.dataframe)
        super().create_geometry()
        self.dataframe.gpdf = self.manipulate_dataframe()
        file_number: int = (count // 100000) + 1
        super().export_data(filename=f"building_{file_number}")
        print(f"building_{file_number} as {count} exported")

    def manipulate_dataframe(self) -> gpd.GeoDataFrame:
        self.dataframe.gpdf = super().set_dataframe()
        self.dataframe.gpdf = self.dataframe.extra_columns(attributes=["amenity", "shop", "tourism", "leisure",
                                                                       "man_made", "historic"])
        self.dataframe.gpdf.loc[0, "type"] = str("")
        self.dataframe.gpdf = self.dataframe.reduce_columns(
            attributes=[self.dataframe.key_tag, "amenity", "shop", "tourism", "leisure", "man_made",
                        "historic", "type"])
        return self.dataframe.gpdf
