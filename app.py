
from flask import Flask, render_template, request
from spatial import Spatial
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():

    # global conn

    is_btree = request.args.get('tree')

    if is_btree == None:
        is_btree = True
    else:
        is_btree = False

    # conn = sqlite3.connect('location_btree.db', check_same_thread=False)

    conn = None

    if is_btree:
        conn = sqlite3.connect('restaurants.db', check_same_thread=False)
    else:
        conn = sqlite3.connect('restaurants_rtree.db', check_same_thread=False)


    radius = request.args.get('radius')

    if radius == None:
        radius = 1
    else:
        radius = int(radius)

    lat = request.args.get('lat')
    lon = request.args.get('long')

    if lat == None or lon == None:
        # Use Kennesaw state university latitude and longitude.
        lat =33.94188717711815
        lon = -84.51962762334004

    spatial = Spatial(10, 10, 50, is_btree=is_btree)

    center = [float(lat), float(lon)]

    nearby_data = spatial.get_nearby_locations(conn, center, radius)

    return render_template('index.html', nearby_data=nearby_data, center=center, radius=radius, spatial=spatial)

if __name__ == '__main__':

    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run()

