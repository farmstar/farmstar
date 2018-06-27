from dicts import *
import fs_nmea
import fs_screen
import fs_checksum
import fs_com
import fs_serial
import fs_database
import fs_server
import os
import json


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
        self.parseLine = fs_nmea.parse()
        self.data = ['','','','']
        self.timer = 0
        if os.name == 'nt':
           os.system('start cmd /K python fs_server.py')
           os.system('start cmd /K python fs_xIM.py')

        while True:
            self.serial_data = self.serial_stream_1.data()
            self.line_1 = self.serial_data['line']
            self.status_1 = self.serial_data['status']
            self.GPS_1 = self.parseLine.parseLine(self.line_1)
            self.display.screen(self.GPS_1)
            self.SPACETIME = self.GPS_1['SPACETIME']
            self.STATUS = self.GPS_1['STATUS']
            self.message = self.STATUS['message']

            
            #Have to do 'if dict', won't work otherwise
            if type(self.SPACETIME) is dict:
                self.data[0] = self.SPACETIME['unix']
            else:
                pass
            if self.message == 'GGA':
                self.GGA = self.GPS_1['GGA']
                if type(self.GGA) is dict:
                    self.data[1] = self.GGA['Latitude']
                    self.data[2] = self.GGA['Longitude']
                    self.data[3] = self.GGA['Altitude']
                else:
                    pass
            
            try:
                if self.data[0] > self.timer:
                    self.timer = self.data[0]
                    self.db.data(self.data)
            except:
                pass



if __name__ == '__main__':
    backend(['COM5'])
