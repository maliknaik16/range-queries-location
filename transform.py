
import pywraps2 as s2
import pandas as pd
import sqlite3

btree = False

if btree:
    conn = sqlite3.connect('restaurants.db')
    df = pd.read_csv('restaurants.csv')

    table = """
    CREATE TABLE IF NOT EXISTS Location (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        CellId CHAR(17) NOT NULL,
        LocationName TEXT NOT NULL,
        Lat REAL NOT NULL,
        Long REAL NOT NULL,
        Level INTEGER NOT NUll
    );
    """

    if conn:
        print('Connection successfully established.')

    # Create table.
    conn.execute(table)

    # Create B-Tree index on CellId
    if conn.execute("CREATE INDEX IF NOT EXISTS cellid_btree ON Location(CellId);"):
        print('Index successfully Created.')

    for i in range(len(df)):
        name = df.iloc[i, 6]

        lat = df.iloc[i, 4]
        lng = df.iloc[i, 5]

        level = 10
        cell_id = s2.S2CellId(s2.S2LatLng.FromDegrees(lat, lng)).parent(level).ToToken()

        conn.execute("INSERT INTO Location (CellId, LocationName, Lat, Long, Level) VALUES(?, ?, ?, ?, ?)", (cell_id, name, lat, lng, level))

        # Commit the database transaction
        conn.commit()

        # print(name, lat, lng)

    conn.close()
else:
    conn = sqlite3.connect('restaurants_rtree.db')
    df = pd.read_csv('restaurants.csv')

    table = """
    CREATE VIRTUAL TABLE Location_rtree USING FTS5(CellId, LocationName, Lat, Long, Level);
    """

    if conn:
        print('Connection successfully established.')

    # Create table.
    conn.execute(table)


    for i in range(len(df)):
        name = df.iloc[i, 6]

        lat = df.iloc[i, 4]
        lng = df.iloc[i, 5]

        level = 10
        cell_id = s2.S2CellId(s2.S2LatLng.FromDegrees(lat, lng)).parent(level).ToToken()

        conn.execute("INSERT INTO Location (CellId, LocationName, Lat, Long, Level) VALUES(?, ?, ?, ?, ?)", (cell_id, name, lat, lng, level))

        # Commit the database transaction
        conn.commit()

    conn.close()
