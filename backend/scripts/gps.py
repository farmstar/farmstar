import serial
import nmea
import time
import curses
import subprocess
import sys


comport = 'COM5'

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
    

def serialStream():

    ser = None
    line = ''
    global comstatus
    comstatus = "Initializing..."
    while True:
        try:
            screen()
        except:
            print("Screen Error")
        try:
            if(ser == None or line == ''):
                ser = serial.Serial(comport,9600,timeout=1.5)
                comstatus = "Reconnecting"
            line = ser.readline().decode("utf-8") # Read the entire string
            try:
                comstatus = "[OK]"
                nmea.parse(line)
            except:
                comstatus = "NMEA Parse Error"
        except:
            if(not(ser == None)):
                ser.close()
                ser = None
                comstatus = "Disconnecting"
            comstatus = str("No Connection to %s" % (comport))
            time.sleep(2)



def screen():
    stdscr.clear()
    stdscr.addstr(1,1,"   COM Port: %s" % (comport))    
    stdscr.addstr(2,1," COM Status: %s" % (comstatus))
    stdscr.addstr(2,1,"   Database: %s" % (comstatus))
    

    stdscr.addstr(4,1,"     String: %s" % (nmea.GGA['String']))
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
    

    
    stdscr.refresh()
    


serialStream()
