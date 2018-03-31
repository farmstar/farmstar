import os
import platform
import com
import serial
import nmea
from multiprocessing import Process
import fs_time



'''
Farmstar backend setup (v2.0)
Gathers info to save to config and sets up databases:
(need to verify time before commencing)

#01 - Scan for active serial ports
#02 - Scans serial ports for GPS data
#03 - Get GPS time
#04 - Get local time
#05 - Test for NTP server
#06 - sync time if necessary
#07 - create backup folder
#08 - backup any existing config
#09 - backup any existing database(s)
#10 - ...
#11 - profit?



    


'''

#Config dictionary
config = {'comports':[],
          'ser': None,
          'line': '',
          }
          
          

def getCom():
    '''
    Runs 'com.py' script
    Returns list of active GPS serial ports
    Returns None if no valid gps data received
    '''
    comports = com.Ports().valid
    if comports == []:
        config['comports'] = None
    else:
        config['comports'] = comports
     

def syncTime():
    comports = config['comports']
    print("Running time sync...")
    fs_time.run(comports)


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
    syncTime()


if __name__ == '__main__':
    run()
            
        
        
