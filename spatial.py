
import pywraps2 as s2
import time

class Spatial:

    def __init__(self, min_level=10, max_level=10, max_cells=50, is_btree=True):
        """
        Initialize the object.
        """

        self.min_level = min_level
        self.max_level = max_level
        self.max_cells = max_cells
        self.is_btree = is_btree

    def get_coverer(self):
        """
        Returns the s2.S2RegionCoverer instance.
        """

        coverer = s2.S2RegionCoverer()

        coverer.set_max_cells(self.max_cells)
        coverer.set_min_level(self.min_level)
        coverer.set_max_level(self.max_level)

        return coverer

    def near(self, point, radius, return_tokens=False, units='mi'):
        """
        Returns the nearby CellIds from the given point around the given radius.
        """

        # Get the Coverer.
        coverer = self.get_coverer()

        if units == 'mi':
            radius = 1609.34 * radius
        elif units == 'km':
            radius = 1000 * radius
        else:
            pass

        # Get the angle in radians.
        angle = s2.S1Angle.Radians(float(radius) / 6371000)

        # Convert the Latitude and Longitude to S2Point.
        point = s2.S2LatLng.FromDegrees(point[0], point[1]).ToPoint()

        # Get the S2Cap from the given point.
        sphere_cap = s2.S2Cap(point, angle)

        # Get the covering around the region.
        covering = coverer.GetCovering(sphere_cap)

        if return_tokens:
            return list(map(lambda x: x.ToToken(), covering))

        return covering

    def get_nearby_locations(self, db, point, radius):
        """
        Returns the records of the nearby locations.
        """

        # Get the nearby cells.
        cells = self.near((point[0], point[1]), radius, return_tokens=True)

        cursor = None

        if self.is_btree:

            time.sleep(0.01)

            # Get the cursor.
            cursor = db.execute("SELECT * FROM Location WHERE CellId IN (%s)" % ("?," * len(cells))[:-1], cells)
        else:
            # x = '%s OR ' * len(cells)
            # x = x[:-4]

            # y = "SELECT * FROM Location WHERE CellId IN '%s';" % (x, )
            # z = y % tuple(cells)

            # # w = "SELECT * FROM Location"
            # cursor = db.execute(z)

            cursor = db.execute("SELECT * FROM Location WHERE CellId IN (%s)" % ("?," * len(cells))[:-1], cells)

        return cursor.fetchall()

    def get_bounding_rect(self, token):
        """
        Returns the bounding latitudes and longitues for the given cellId.
        """

        bounds = []

        # Get the bounding rect from the token.
        rect = s2.S2Polygon(s2.S2Cell(s2.S2CellId.FromToken(token))).GetRectBound()

        for i in range(4):
            vertex = []
            v = rect.GetVertex(i)
            vertex.append(v.lat().degrees())
            vertex.append(v.lng().degrees())

            bounds.append(vertex)

        return bounds
