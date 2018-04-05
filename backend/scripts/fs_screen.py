import serial
import fs_nmea
import time
import curses
import subprocess
import sys
import com

'''
Farmstar screen module
Takes a dictionary of dictionaries with processed nmea data (from fs_nmea)
{'gga':{'fix':'012345','age':'3'},'rmc':{key:val}}
Prints to a terminal screen statically, i.e. not scrolling
needs to be initiated from a terminal not IDE
'''


class display():

    def __init__(self,GPS={}):
        self.GPS = GPS
        self.STATUS = self.GPS['STATUS']
        self.SPACETIME = self.GPS['SPACETIME']
        self.GGA = self.GPS['GGA']
        self.GSA = self.GPS['GSA']
        self.screen()

        '''
        try:
            stdscr = curses.initscr()
        except:
            raise Exception("Run from cmd or bash")

        try:
            subprocess.Popen([sys.executable, 'server.py'],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        except:
            raise Exception("Failed to start server")    
        '''





    def screen(self):

        try:
            #Box 1
            box1.addstr(1,1,' '*78)
            box1.addstr(1,1,self.STATUS['string'].center(78, ' '))
            
            #Box 2
            check = '{}/{} - {}'.format(self.STATUS['checksum'],self.STATUS['calculated'],self.STATUS['check'])
            box2.addstr(1,1,str(' '*16))
            box2.addstr(1,1,check)

            #Box 3
            errper = int(round((int(self.STATUS['count_bad'])/int(self.STATUS['count_total']))*100))
            errors = '{}/{} - {}%'.format(self.STATUS['count_bad'],self.STATUS['count_total'],errper)
            box3.addstr(1,1,str(' '*18))
            box3.addstr(1,1,errors.center(18, ' '))

            #Box 4
            box4.addstr(1,1,str(' '*20))
            box4.addstr(1,1,'Lat: {} {}'.format(self.GGA['Latitude'],self.GGA['North/South']))
            box4.addstr(2,1,str(' '*20))
            box4.addstr(2,1,'Lon: {} {}'.format(self.GGA['Longitude'],self.GGA['East/West']))
            box4.addstr(3,1,str(' '*20))
            box4.addstr(3,1,'Alt: {} {}'.format(self.GGA['Altitude'],self.GGA['Altitude_Units']))
            box4.addstr(4,1,str(' '*20))
            box4.addstr(4,1,'Sat: {}'.format(self.GGA['Satellites']))
            box4.addstr(5,1,str(' '*20))
            box4.addstr(5,1,'Qua: {} - {}'.format(self.GGA['Quality'],self.GGA['Type']))
            box4.addstr(6,1,str(' '*20))
            box4.addstr(6,1,'Acc: {}'.format(self.GGA['Accuracy']))
            box4.addstr(7,1,str(' '*20))
            box4.addstr(7,1,'Geo: {} {}'.format(self.GGA['GeoID_Height'],self.GGA['GeoID_Units']))
            box4.addstr(8,1,str(' '*20))
            box4.addstr(8,1,'Fix: {} UTC'.format(self.GGA['Fix']))
            
            
            
            stdscr.refresh()
            box1.refresh()
            box2.refresh()
            box3.refresh()
            box4.refresh()
        except:
            curses.endwin()
            print("Screen Failed")

        

class main():
    #main for testing this module

    def __init__(self, comports=''):
        self.comports = comports
        self.line = ''
        self.ser = None

        if self.comports == '':
            print("No serial port specified")
            self.getPorts()
        self.initScreen()
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
            

    def initScreen(self):
        global stdscr
        global box1
        global box2
        global box3
        global box4
        
        print("Initiating screen...")
        stdscr = curses.initscr()
        stdscr.border(0)
        box1 = curses.newwin(3, 80, 1, 1)
        box2 = curses.newwin(3, 18, 1, 81)
        box3 = curses.newwin(3, 20, 1, 99)
        box4 = curses.newwin(10, 22, 4, 1)
        box1.box()
        box2.box()
        box3.box()
        box4.box()
        stdscr.addstr(0,50,"Farmstar Boiiii")
        box1.addstr(0,40,"Sentence")
        box2.addstr(0,5,"Checksum")
        box3.addstr(0,7,"Errors")
        box4.addstr(0,10,"GGA")
        print("Stating GPS...")

    
    def run(self):
        self.comport = self.comports[0]
        while True:
            try:
                if(self.ser == None or self.line == ''):
                    self.ser = serial.Serial(self.comport,9600,timeout=1.5)
                self.line = self.ser.readline().decode("utf-8") # Read the entire string
                try:
                    self.GPS = fs_nmea.parse(self.line).GPS
                    display(self.GPS)
                except:
                    print("Display fail")
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

