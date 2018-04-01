import time
from dateutil import tz
from datetime import datetime
from dicts import *
import fs_checksum


'''
Farmstar nmea data parser
Converts GPS data into a list of dictionaries
Returns the dictionary list
'''


class parse():

    #parse raw nmea data (one line at a time)
    #Currently only GGA
    
    def __init__(self, line=None):
        self.GGA = GGA.GGA
        self.line = line
        self.fix = 000000
    
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

    def parseTime(self, fix=None):
        #Takes a 6 digit gps fix integer and saves time values to a dictionary
        self.TIME = TIME.TIME
        

    def parseGGA(self):
        #Send to checksum parser
        self.check = fs_checksum.parse(self.line)
        #Count the total/good/bad strings
        self.GGA['Count_total'] += 1
        if self.check == True:
            self.GGA['Count_good'] += 1
        else:
            self.GGA['Count_bad'] += 1
            

        
        GGA['Fix'] = fixlocal
        GGA['Local_time'] = localtime
        GGA['Age'] = age
        
        GGA['String'] = stripped
        GGA['Sentence'] = sentence[0][1:]
        GGA['Checksum'] = hex_checksum
        GGA['Calculated'] = hex_data
        GGA['Check'] = check

        lat = sentence[2][:2].lstrip('0') + "." + "%.7s" % str(float(sentence[2][2:])*1.0/60.0).lstrip("0.")
        if sentence[3] == 'S':
            GGA['Latitude'] = float(lat)*-1
        else:
            GGA['Latitude'] = float(lat)
        GGA['North/South'] = sentence[3]

        lon = sentence[4][:3].lstrip('0') + "." + "%.7s" % str(float(sentence[4][3:])*1.0/60.0).lstrip("0.")
        GGA['Longitude'] = float(lon)
        GGA['East/West'] = sentence[5]

if __name__ == '__main__':
    parse('$GPGGA,024106,3321.9308,S,11537.59819,E,1,21,1.0,-8.313,M,-30.9,M,,*63')


