import time
from dateutil import tz
from datetime import datetime
from dicts import *
import fs_checksum
import fs_time
import serial


'''
Farmstar nmea data parser
Converts GPS data into a bunch of dictionaries
Creates a dictionary of all dictionaries
REMEMBER TO PUT NEW DICTIONARIES IN THE __init__.py
Amount of time wasted forgetting that... about 3
'''


class parse():

    #parse raw nmea data (one line at a time)
    #Currently only GGA
    
    def __init__(self, line=None):
        self.GPS = GPS.GPS
        self.STATUS = STATUS.STATUS
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

        #Latitude conversion
        self.lat = self.sentence[2][:2].lstrip('0') + "." + "%.7s" % str(float(self.sentence[2][2:])*1.0/60.0).lstrip("0.")
        if self.sentence[3] == 'S':
            self.GGA['Latitude'] = float(self.lat)*-1
        else:
            self.GGA['Latitude'] = float(self.lat)
        self.GGA['North/South'] = self.sentence[3]

        #Lonitude conversion
        self.lon = self.sentence[4][:3].lstrip('0') + "." + "%.7s" % str(float(self.sentence[4][3:])*1.0/60.0).lstrip("0.")
        self.GGA['Longitude'] = float(self.lon)
        self.GGA['East/West'] = self.sentence[5]
        
        #Pack SPACETIME and GGA dictionaries into GPS dictionary
        self.GPS['SPACETIME'] = self.SPACETIME
        self.GPS['GGA'] = self.GGA


class main():
    #main for testing this module

    def __init__(self, comports=''):
        self.comports = comports
        self.line = ''
        self.ser = None


        if self.comports == '':
            self.getPorts()
        else:
            self.run()


    def getPorts(self):
        print("Scanning for active ports...")
        self.comports = com.Ports().valid
        if self.comports == []:
            print("Unable to find valid gps port")
            self.comport = None
        else:
            self.comport = self.comports[0]
            self.run()
    

    def run(self):
        self.comport = self.comports[0]
        while True:
            try:
                if(self.ser == None or self.line == ''):
                    self.ser = serial.Serial(self.comport,9600,timeout=1.5)
                self.line = self.ser.readline().decode("utf-8") # Read the entire string
                try:
                    #send line to parse
                    parse(self.line)
                except:
                    print("NMEA Parse Fail")
            except:
                if(not(self.ser == None)):
                    self.ser.close()
                    self.ser = None
                    print("Disconnecting")
                print("No Connection to {}".format(self.comport))
                time.sleep(2)






if __name__ == '__main__':
    #Uses com module to scan for valid ports if a port isn't specified
    #main()
    main(['COM5'])


