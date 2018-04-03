import serial
import fs_nmea
import time
import curses
import subprocess
import sys
import com

'''
Farmstar screen module
Takes a dictionary of dictionaries with processed nmea data
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
        global stdscr
        stdscr.clear()
        '''
        stdscr.addstr(1,1,"   COM Port: %s" % (comport))
        
        stdscr.addstr(2,1," COM Status: %s" % (comstatus))
        stdscr.addstr(2,1,"   Database: %s" % (comstatus))
        
        '''
        stdscr.addstr(4,1,"     String: {}".format(self.GGA['String']))
        '''
        stdscr.addstr(4,1,"   Sentence: %s" % (nmea.GGA['Sentence']))
        stdscr.addstr(5,1,"   Checksum: %s" % (nmea.GGA['Checksum']))
        stdscr.addstr(6,1," Calculated: %s" % (nmea.GGA['Calculated']))
        stdscr.addstr(7,1,"      Check: %s" % (nmea.GGA['Check']))
        stdscr.addstr(8,1,"      Total: %s" % (nmea.GGA['Count_total']))
        stdscr.addstr(9,1,"       Good: %s" % (nmea.GGA['Count_good']))
        stdscr.addstr(10,1,"        Bad: %s" % (nmea.GGA['Count_bad']))

        stdscr.addstr(12,1,"  Last Fix: %s" % (nmea.GGA['Fix']))
        stdscr.addstr(13,1,"Local Time: %s" % (nmea.GGA['Local_time']))
        stdscr.addstr(14,1,"       Age: %s" % (nmea.GGA['Age']))
        stdscr.addstr(15,1,"  Latitude: %s %s" % (nmea.GGA['Latitude'],nmea.GGA['North/South']))
        stdscr.addstr(16,1," Longitude: %s %s" % (nmea.GGA['Longitude'], nmea.GGA['East/West']))
        '''
        stdscr.refresh()

        

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
    global stdscr
    print("Initiating screen")
    stdscr = curses.initscr()
    print("Running main")
    main(['COM5'])

