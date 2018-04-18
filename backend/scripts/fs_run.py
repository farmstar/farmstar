from dicts import *
import fs_nmea
import fs_screen
import fs_checksum
import fs_com
import fs_serial
import fs_database
import fs_server
import os


'''
Farmstar backend run script
The 'main' running script
Needs to be initiated from shell for screen to work
'''


class backend():

    def __init__(self,comports=''):
        self.comports = comports
        self.comport()
        self.run()
        
    def comport(self):
        if self.comports == '':
            print("No serial port specified")
            self.comports = com.Ports().valid
            if self.comports == []:
                print("Unable to find valid gps port")
            else:
                self.comport_1 = self.comports[0]
        else:
            self.comport_1 = self.comports[0]

    def run(self):
        self.serial_stream_1 = fs_serial.stream(self.comport_1)
        self.display = fs_screen.display()
        self.db = fs_database.logging()
        self.data = ['','','','']
        if os.name == 'nt':
            os.system('start cmd /K python fs_server.py')

        while True:
            self.serial_stream_1.data()
            self.line_1 = self.serial_stream_1.line
            self.status_1 = self.serial_stream_1.status
            self.GPS_1 = fs_nmea.parse(self.line_1).GPS
            self.display.screen(self.GPS_1)
        
            self.SPACETIME = self.GPS_1['SPACETIME']
            self.GGA = self.GPS_1['GGA']

            #This is a stupid way of doing this, the normal way isn't working.
            for key in self.SPACETIME:
                if key == 'unix':
                    self.data[0] = self.SPACETIME[key]
            for key in self.GGA:
                if key == 'Latitude':
                    self.data[1] = self.GGA[key]
                elif key == 'Longitude':
                    self.data[2] = self.GGA[key]
                elif key == 'Altitude':
                    self.data[3] = self.GGA[key]

            self.db.data(self.data)






if __name__ == '__main__':
    backend(['COM5'])
