import json
import sqlite3
import re
import copy
from dicts import FEATURES



con = sqlite3.connect('xim.db')
c = con.cursor()

collection = FEATURES.COLLECTION
feature = FEATURES.FEATURE


#Final json not correct, has single quotes rather than double quotes.

def getData():
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = c.fetchall()
    collection['features'] = []
    feature_list = []
    for table in tables:
        match = re.search('''(?<=')\s*[^']+?\s*(?=')''',str(table))
        name = match.group().strip()
        c.execute("SELECT * FROM %s ORDER BY UNIX DESC LIMIT 1" % (name))
        result = c.fetchone()
        if result != None:
            lat = result[6]
            lon = result[7]
            name = result[1]
            feature['geometry']['coordinates'] = [lon,lat]
            feature['properties']['title'] = name
            dup = copy.deepcopy(feature)
            feature_list.append(dup)
    collection['features'] = feature_list
    collect = json.dumps(collection)
    return(collect)


if __name__ == '__main__':
    print(getData())
