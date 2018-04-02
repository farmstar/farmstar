import com
import serial
import time
import nmea


'''
INCOMPLETE
Farmstar time sync module
gets time from NTP, GPS, local device
Compares and syncronises local device time
(In theory)
'''

class lord():

    def __init__(self, comport=None, line='', NTPserver='',fix=000000):
        self.comport = comport
        self.line = line
        self.NTPserver = NTPserver
        self.NTPstatus = False
        self.status = 'Initializing'
        self.fix = fix
        self.ser = None

        



    
    def gpsTime(self):
        
        while True:
            try:
                if(self.ser == None or self.line == ''):
                    self.ser = serial.Serial(self.comport,9600,timeout=1.5)
                self.line = ser.readline().decode("utf-8") # Read the entire string
                self.gps_time = nmea.parse(line).GGA['Fix']
            except:
                if(not(ser == None)):
                    ser.close()
                    ser = None
                    self.comstatus = "Disconnecting"
                self.comstatus = "No Connection to {}".format(self.comport)
                time.sleep(2)

    def getPorts(self):
        print("Scanning for active ports...")
        self.comports = com.Ports().valid
        if self.comports == []:
            print("No active ports")
            self.comport = None
        else:
            self.comport = self.comports[0]
            
    
    def gpsTime(self, line):
        print("Parsing GPS time...")
        self.gps_time = nmea.parse(line).GGA['Fix']


    def getNTP():
        #Attempts to retrieve system NTP server
        #Tests NTP server or tries default
        #Returns NTP time
        print("Polling NTP server...")
        pass


    def setTime(time):
        #Sets the system time
        os.system('time %s' % (time))



if __name__ == '__main__':
    lord()
