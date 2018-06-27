import fs_database
import time
import datetime
import json
from dicts import *


class geojson():
    
    def __init__(self, cursor, seconds):
        self.GEOJSON = GEO.JSON
        self.seconds = seconds
        now = time.time()
        self.start = now-self.seconds
        self.cursor = cursor
        self.longList = []

    def getData(self):
        self.now = time.time()
        if self.longList == []:
            self.cursor.execute("SELECT * FROM LOCATION WHERE UNIX BETWEEN {} AND {}".format(self.start, self.now))
        else:
            try:
                self.last = self.result[-1][0]
                self.cursor.execute("SELECT * FROM LOCATION WHERE UNIX BETWEEN {} AND {}".format(self.last, self.now))
            except:
                pass
        self.result = self.cursor.fetchall()
        for i in self.result:
            self.lon = i[2]
            self.lat = i[1]
            self.lonLat = [self.lon,self.lat]
            self.longList.append(self.lonLat)
        print(len(self.longList))
        self.GEOJSON['geometry']['coordinates'] = self.longList
        j = json.dumps(self.GEOJSON)
        return(j)



if __name__ == '__main__':
    cursor = fs_database.logging().c
    geoline = geojson(cursor, 600)
    while True:
        geojson = geoline.getData()
        time.sleep(1)
