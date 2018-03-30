import os
import platform
import com
import serial
import nmea
from multiprocessing import Process


'''
#1 - Get GPS com port
#2 - Get GPS time
#3 - Get NTP time (try)
#4 - Compare times
#5 - sync time if necessary
#6 - set path variables
#7 - create backup folder
#8 - backup config
#9 - backup database(s)



    


'''
config = {'comports':[],
          'ser': None,
          'line': '',
          }
          
          

def getCom():
    comports = com.Ports()
    config

     

def readSerial():
    global ser
    ser = None
    global line
    line = ''
    comport = comports[0]
    while True:
        try:
            if(ser == None or line == ''):
                ser = serial.Serial(comport,9600,timeout=1.5)
            line = ser.readline().decode("utf-8") # Read the entire string
        except:
            if(not(ser == None)):
                ser.close()
                ser = None
                comstatus = "Disconnecting"
            comstatus = str("No Connection to %s" % (comport))
            time.sleep(2)


def gpsTime():
    while True:
        sentence = readSerial()
        if sentence[0] == 'GGA':
            fixtime = sentence[1]
            



def setPaths():
    backdir = os.path.join(os.path.dirname(__file__),
                           'backup',
                           datetime.now().strftime('%Y'),
                           datetime.now().strftime('%m'),
                           datetime.now().strftime('%H%M%S'))

    config = os.path.join(os.path.dirname(__file__),
                          'config.py')

    dicdir = os.path.join(os.path.dirname(__file__),
                          'dictionaries')



def backupFolder():
    try:
        os.makedirs(backdir)
    except:
        return(False)



def configBackup():
    if os.path.exists(config) == False:
        try:
            with open(config, 'w') as f:
                f.close
        except:
            return(False)
    else:
        try:
            backupFolder()
            shutil.copyfile(config, "%s/%s" % (backdir, 'config.py'))
            with open(config,'w') as f:
                f.close
        except:
            return(False)

def run():
    getCom()
    readSerial()


if __name__ == '__main__':
    run()
            
        
        
