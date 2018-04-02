import time
from dateutil import tz
from datetime import datetime
from dicts import *
import fs_checksum
import fs_time


'''
Farmstar nmea data parser
Converts GPS data into a bunch of dictionaries
'''


class parse():

    #parse raw nmea data (one line at a time)
    #Currently only GGA
    
    def __init__(self, line=None):
        self.GGA = GGA.GGA
        self.line = line
    
        if self.line == None:
            print("No data recieved")
        else:
            #Remove newline
            self.stripped = self.line.rstrip('\n\r')
            #Split into a list format
            self.sentence = self.stripped.split(",")
            #Get the sentence type
            self.NMEA = self.sentence[0][3:]
            if self.NMEA == 'GGA':
                self.parseGGA()
            else:
                pass
        

    def parseGGA(self):
        #Send to checksum parser
        self.check = fs_checksum.parse(self.line)
        #Count the total/good/bad strings
        self.GGA['Count_total'] += 1
        if self.check == True:
            self.GGA['Count_good'] += 1
        else:
            self.GGA['Count_bad'] += 1

        self.SPACETIME = fs_time.parse(self.sentence[1]).SPACETIME  
        
        self.GGA['Fix'] = self.SPACETIME['fixlocal']
        self.GGA['Local_time'] = self.SPACETIME['localtime']
        self.GGA['Age'] = self.SPACETIME['age']    
        self.GGA['String'] = self.stripped
        self.GGA['Sentence'] = self.sentence[0][1:]
        self.GGA['Check'] = self.check

        self.lat = self.sentence[2][:2].lstrip('0') + "." + "%.7s" % str(float(self.sentence[2][2:])*1.0/60.0).lstrip("0.")
        if self.sentence[3] == 'S':
            self.GGA['Latitude'] = float(self.lat)*-1
        else:
            self.GGA['Latitude'] = float(self.lat)
        self.GGA['North/South'] = self.sentence[3]

        self.lon = self.sentence[4][:3].lstrip('0') + "." + "%.7s" % str(float(self.sentence[4][3:])*1.0/60.0).lstrip("0.")
        self.GGA['Longitude'] = float(self.lon)
        self.GGA['East/West'] = self.sentence[5]

if __name__ == '__main__':
    #Script test
    GGA = parse('$GPGGA,024106,3321.9308,S,11537.59819,E,1,21,1.0,-8.313,M,-30.9,M,,*63').GGA
    for i in GGA:
        print('{} : {}'.format(i,GGA[i]))


