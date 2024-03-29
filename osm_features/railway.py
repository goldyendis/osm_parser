import geopandas
from osmium.osm import OSMObject

from manipulation.manipulate_geodataframe import MyGeoDataFrame
from osm_features.abstract.super_osm_feature import AbstractOSM


class OSMWayRailway(AbstractOSM):
    """Processor of the Railway Line OSM Entities"""
    def __init__(self, osm_feature: OSMObject, key_tag: str) -> None:
        self.dataframe = MyGeoDataFrame(osm_feature, key_tag)
        super(OSMWayRailway, self).__init__(dataframe=self.dataframe)
        super().create_geometry()
        self.dataframe.gpdf = self.manipulate_dataframe()
        super().export_data()
        self.dataframe.gpdf = self.dataframe.reduce_columns(attributes=[self.dataframe.key_tag, "service", "usage"])
        super().export_data(filename="railway_egyben")

    def manipulate_dataframe(self) -> geopandas.GeoDataFrame:
        self.dataframe.gpdf = super().set_dataframe()
        self.dataframe.gpdf = self.dataframe.extra_columns(
            attributes=["bridge", "tunnel", "service", "usage", "station"])
        self.dataframe.gpdf = self.dataframe.reduce_columns(
            attributes=[self.dataframe.key_tag, "tunnel", "bridge", "service", "usage", "station"])
        return self.dataframe.gpdf


class OSMNodeRailway(AbstractOSM):
    """Processor of the Railway Point OSM Entities"""
    def __init__(self, osm_feature: OSMObject, key_tag: str) -> None:
        self.dataframe = MyGeoDataFrame(osm_feature, key_tag)
        super(OSMNodeRailway, self).__init__(dataframe=self.dataframe)
        super().create_geometry()
        self.dataframe.gpdf = self.manipulate_dataframe()
        super().export_data()

    def manipulate_dataframe(self) -> geopandas.GeoDataFrame:
        self.dataframe.gpdf = super().set_dataframe()
        self.dataframe.gpdf = self.dataframe.extra_columns(attributes=["station"])
        self.dataframe.gpdf = self.dataframe.reduce_columns(
            attributes=[self.dataframe.key_tag, "station"])
        return self.dataframe.gpdf
