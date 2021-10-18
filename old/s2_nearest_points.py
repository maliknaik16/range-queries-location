
import pywraps2 as s2

min_level = 15
max_level = 20

data = [
    {
        'name': 'Kennesaw State University Marietta Campus',
        'point': (33.94188717711815, -84.51962762334004),
        'cell_id': ''
    },
    {
        'name': 'Kennesaw State University Kennesaw Campus',
        'point': (34.04572992022793, -84.58347099361183),
        'cell_id': ''
    }
]

coverer = s2.S2RegionCoverer()

coverer.set_max_cells(50)
coverer.set_min_level(min_level)
coverer.set_max_level(max_level)


def near(pos, radius):
    global coverer

    angle = s2.S1Angle.Radians(float(radius) / 6371000)

    point = s2.S2LatLng.FromDegrees(pos[0], pos[1]).ToPoint()

    sphere_cap = s2.S2Cap(point, angle)

    # r = sphere_cap.GetBound()

    covering = coverer.GetCovering(sphere_cap)
    print(angle)

    print(len(covering))
    for cell in covering:
        print(cell.ToToken())

for i in range(len(data)):
    data[i]['cell_id'] = s2.S2CellId(s2.S2LatLng.FromDegrees(data[i]['point'][0], data[i]['point'][1])).ToToken()

near((34.04572992022793, -84.58347099361183), 100)
print(data)