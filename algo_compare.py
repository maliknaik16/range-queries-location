
from flask import Flask, render_template, request
from spatial import Spatial
import matplotlib.pyplot as plt
import sqlite3
import time

conn = None

trees = [True, False]

lat = 33.94188717711815
lon = -84.51962762334004

print('Using Coordinates (Lat, Lng) as (%f, %f)' % (lat, lon))

fig, ax = plt.subplots(figsize=(20, 15))

data = []

def plot(ax, x, y, label):
    """
    Plots the score over time after the model has been fitted.
    :return: None if the model isn't fitted yet
    """

    ax.plot(x, y, label=label)
    ax.set_xlabel("Radius (in miles)")
    ax.set_ylabel("Response Time (in ms)")
    ax.legend()


for is_btree in trees:

    performance_data_x = []
    performance_data_y = []

    tree_str = 'B-Tree' if is_btree else 'R-Tree'

    if is_btree:
        conn = sqlite3.connect('restaurants.db', check_same_thread=False)
    else:
        conn = sqlite3.connect('restaurants_rtree.db', check_same_thread=False)

    print('Using', tree_str)

    for radius in range(1, 250):

        print('With Radius = %d' % (radius, ))

        spatial = Spatial(10, 10, 50, is_btree=is_btree)

        center = [float(lat), float(lon)]

        # Get the initial time.
        initial_time = time.time()

        # Get the nearby locations.
        nearby_data = spatial.get_nearby_locations(conn, center, radius)

        # Calculate the time.
        diff = (time.time() - initial_time) * 1000

        print('It took %.3f milliseconds to return the response [with %s]' % (diff, tree_str))

        performance_data_x.append(radius)
        performance_data_y.append(diff)

    # print(performance_data_x)
    # print(performance_data_y)

    plot(ax, performance_data_x, performance_data_y, label="B-Tree" if is_btree else "Radix-Tree (Trie)")

plt.title("Algorithm Performance Comparison")
plt.savefig('algorithm_comparison.eps', format = 'eps')
plt.show()
