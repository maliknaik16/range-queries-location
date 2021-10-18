
from math import radians, cos, sin, asin, sqrt

def distance(lat1, lat2, long1, long2):
    """
    Returns the distance between two points on earth.

    Example:
    ---------
        (Lat1, Long1): (33.93839803572918, -84.51988511540549)

        (Lat2, Long2): (33.972998296381995, -84.55318742253527)

    """

    # Get the radians from the degrees.
    long1 = radians(long1)
    long2 = radians(long2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    # Haversine formula
    diff_long = long2 - long1
    diff_lat = lat2 - lat1

    a = sin(diff_lat / 2)**2 + cos(lat1) * cos(lat2) * sin(diff_long / 2)**2

    c = 2 * asin(sqrt(a))

    # Radius of earth in kilometers. Use 6371 for kilometers\
    result = c * 3956

    return result

def cell_stats():
    """
    @source: https://s2geometry.io/resources/s2cell_statistics.html
    """

# lat1 = 33.93839803572918
# lat2 = 33.972998296381995
# lon1 = -84.51988511540549
# lon2 =  -84.55318742253527
# print(distance(lat1, lat2, lon1, lon2), "miles")
