import com
import serial
import time
from dateutil import tz
from datetime import datetime
import tzlocal
from dicts import *
import fs_checksum


'''
Farmstar gps time parser
Takes a 6 digit integer (HHMMSS) and does stuff
Uses local device OS date and timezone
Returns a dictionary (SPACETIME) regardless if a gps fix is given

TODO:
Remove unnessary info from dictionary
Calculate time since last GPS update
'''

class parse():

    def __init__(self, fix=000000):
        self.fix = fix
        print("Fix: {}".format(self.fix))
        self.SPACETIME = SPACE.TIME
        self.gpsTime()

    def gpsTime(self):
        #Timezone calculations and conversions:
        #Requires local device date to be correct (gps only supplies time)

        #Previous fix value (last iteration)
        self.SPACETIME['prevfix'] = self.SPACETIME['fix']
       
        #GPS fix time raw 6 digit integer
        self.SPACETIME['fix'] = self.fix

        #Get UTC timezone object:
        self.SPACETIME['from_zone'] = tz.tzutc()

        #Get local timezone object:
        self.SPACETIME['to_zone'] = tz.tzlocal()

        #Local timezone name
        self.SPACETIME['tzLocal'] = tzlocal.get_localzone().zone
       
        #Convert GPS fix to a datetime object:
        self.SPACETIME['fixtime'] = datetime.strptime(self.fix, '%H%M%S')
        
        #Formats the GPS fix time:
        self.SPACETIME['fixutc'] = self.SPACETIME['fixtime'].strftime('%H:%M:%S')
       
        #Get the local time in UTC:
        self.SPACETIME['localutc'] = datetime.utcnow()
       
        #Get the local date converted to UTC:
        #(UTC date will be different to local date at certain times)
        self.SPACETIME['utcdate'] = self.SPACETIME['localutc'].strftime('%Y-%m-%d')
        
        #Prepend local utc date to the gps fix time:
        self.SPACETIME['gpsutcdatetime'] = str("%s %s" % (self.SPACETIME['utcdate'], self.SPACETIME['fixutc']))
        
        #Convert back to a datetime object
        self.SPACETIME['fixutcdatetime'] = datetime.strptime( self.SPACETIME['gpsutcdatetime'], '%Y-%m-%d %H:%M:%S')
        
        #Tell datetime it is in the UTC timezone
        self.SPACETIME['gpsdatetime'] = self.SPACETIME['fixutcdatetime'].replace(tzinfo=self.SPACETIME['from_zone'])
        
        #Convert the GPS fix datetime from UTC to local timezone
        self.SPACETIME['gpslocal'] = self.SPACETIME['gpsdatetime'].astimezone(self.SPACETIME['to_zone'])
       
        #Extract the time only
        self.SPACETIME['fixlocal'] = self.SPACETIME['gpslocal'].strftime('%H:%M:%S')
        
        #Get local datetime
        self.SPACETIME['localdatetime'] = datetime.now()
        
        #Tell datetime the local timezone
        self.SPACETIME['localdatetimezone'] = self.SPACETIME['localdatetime'].replace(tzinfo=self.SPACETIME['to_zone'])
      
        #Local time to compare with GPS fix time
        self.SPACETIME['localtime'] = self.SPACETIME['localdatetime'].strftime('%H:%M:%S')
        
        #Calculate the local and gps fix time difference
        self.SPACETIME['timediff'] = (self.SPACETIME['localdatetimezone']-self.SPACETIME['gpslocal']).total_seconds()

        for i in self.SPACETIME:
            print('{} : {}'.format(i,self.SPACETIME[i]))

'''           
        #Calculate the fix age (time since last fix)
        if self.fix > self.prevfix:
            age = 0
        elif self.fix == self.prevfix:
            age = self.fix - self.prevfix
        elif self.fix < self.prevfix:
            print("It's bigger on the inside!?")
        else:
            print("I got no ting bro")
'''

            










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
                    self.gpsTime()
                except:
                    print("Time parse fail")
            except:
                if(not(self.ser == None)):
                    self.ser.close()
                    self.ser = None
                    print("Disconnecting")
                print("No Connection to {}".format(self.comport))
                time.sleep(2)


    def gpsTime(self):
        self.stripped = self.line.rstrip('\n\r')
        self.sentence = self.stripped.split(",")
        self.NMEA = self.sentence[0][3:]
        if self.NMEA == 'GGA':
            print("GGA")
            self.fix = self.sentence[1]
            parse(self.fix)



if __name__ == '__main__':
    #Uses com module to scan for valid ports if a port isn't specified
    #main()
    main(['COM5'])
