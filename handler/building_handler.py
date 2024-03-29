import osmium as o
from osmium.osm import Area
from osm_features.abstract.factory import OSMFactory


class OSMHandlerBuilding(o.SimpleHandler):
    """OSM Area Buildings Handler"""

    def __init__(self) -> None:
        super(OSMHandlerBuilding, self).__init__()
        self.count: int = 1

    def area(self, a: Area) -> None:
        """Osmium Area callback, only to process the Building Areas
        :param a: osmium.osm.Area | Immutable class object to process
        """
        if "building" in a.tags:
            OSMFactory.create_factory(osm_feature=a, key_tag="building", count = self.count)
            self.count += 1
