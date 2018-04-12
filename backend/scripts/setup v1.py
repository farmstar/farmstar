import sqlite3
import time
import serial
import sys
import platform
import os
import shutil
import socket
import tzlocal
import glob
from collections import defaultdict
import pathlib
import errno
from datetime import datetime

config = os.path.join(os.path.dirname(__file__),'config.py')
oldconfig = 'config.py.old'
timezone = tzlocal.get_localzone()
epocoffset = time.timezone
comportlist = []
comport = 'x'
sentencetypes = []
db = 'x'
sentencelengths = []
openserial = 'x'
maxlist = []
maxitems = []
mydir = os.path.join(os.path.dirname(__file__),
                     'backup',
                     datetime.now().strftime('%Y'),
                     datetime.now().strftime('%m'),
                     datetime.now().strftime('%H%M%S'))

def backupFolder():
    try:
        os.makedirs(mydir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise  # This was not a "directory exist" error..


def configBackup():
    print("This script will automatically generate a config file 'config.py'")
    print("If any files exists, they will be moved to a backup folder")
    if os.path.exists(config)==False:
        print("No config file exists, attempting to create one...")
        try:
            open(config,'w')
            open(config,'w').close
        except IOError:
            print("Unable to create config file")
        print("Blank config file created OK!")
    else:
        try:
            backupFolder()
            shutil.copyfile(config, "%s/%s" % (mydir, oldconfig))
            print("Existing config backed up.")
            open(config,'w')
            print("Config now blank.\n")
        except IOError:
            print("Unable to read file.")

def databaseBackup():
    db_exists = 0
    print("Scanning for existing databases.....")
    for file in os.listdir("."):
        if file.endswith(".db"):
            print("Database %s exists, backing up....." % (file))
            shutil.copyfile(config, "%s/%s" % (mydir, file))
            db_exists =+ 1
    if db_exists == 0:
        print("No existing databases found")
    
            
            

def timeNow():
    epoc = time.time()
    timenow = str(datetime.fromtimestamp(epoc).strftime('%d/%m/%Y %H:%M:%S'))
    return(epoc,timenow)


    
def checkTime():
    global timezone
    global epocoffset
    global config
    while True:
        timenow = timeNow()
        datetime = timenow[1]
        print(datetime)
        print(timezone)
        t = input("Is this the correct time and zone? (y/n):\n")
        if t == 'y':
            with open(config,'a') as f:
                f.write("created = '%s'\n"
                        "timezone = '%s'\n"
                        'epocoffset = %s\n'
                        % (datetime, timezone, epocoffset))
            
            print("OK!\n")
            return
        if t == 'n':
            while True:
                c = input("Please set your machine to the correct time and press 'c':\n")
                if c == 'c':
                    break
                else:
                    print("Please press 'c' only.")
        else:
            print("Please press either 'y' or 'n'")
        
def getSystem():
    global config
    arch = platform.machine()
    ver = platform.version()
    plat = platform.platform()
    host = platform.node()
    sys = platform.system()
    proc = platform.processor()
    print("Architecture: ", arch)
    print("Version: ", ver)
    print("Platform: ", plat)
    print("Hostname: ", host)
    print("System: ", sys)
    print("Processor: ", proc)
    with open(config,'a') as f:
        f.write("architecture = '%s'\n" % arch +
                "version = '%s'\n" % ver +
                "platform = '%s'\n" % plat +
                "hostname = '%s'\n" % host +
                "system = '%s'\n" % sys +
                "processor = '%s'\n" % proc)
    print("Attributes written to config file.\n")

def checkSerial():
    while True:
        g = input("Do you have a GPS device connected to a serial port? (y/n):\n")
        if g == 'y':
            print("Now going to scan for active serial ports...\n")
            return
        if g == 'n':
            print("Please connect a GPS device.")
            break
        else:
            print("Please press either 'y' or 'n'")

def scanSerial():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')
    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            ser = serial.Serial(comport,9600,timeout=1.5)
            ser.readline().decode("utf-8")
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    comportlist = result

def testSerial():
    for port in comportlist:
        try:
            ser = serial.Serial(comport,9600,timeout=1.5)
            ser.readline().decode("utf-8")
        except:
            return(False)
    

def saveSerial():
    print("Found active serial ports:")
    print(comportlist)
    c = input("Please choose a COM port as displayed above:\n")
    open(config,'a').write("comport = '%s'\n" % c)

def openComport():
    global comport
    global config
    global openserial
    with open(config) as f:
        for line in f:
            if "comport" in line:
                port = line.split("= '",1)[1]
                comport = port.rstrip("'\n\r")
                openserial = serial.Serial(comport,9600,timeout=1) # Open Serial port
                f.close

def serialStream():
    global openserial
    while True:
        while openserial.read().decode("utf-8") != '$': # Wait for the begging of the string
            pass # Do nothing
        serialstream = openserial.readline().decode("utf-8") # Read the entire string
        return(serialstream)

def verifySerial():
    print("Now going to verify GPS data...")
    print("Waiting for a valid GPS string...")
    print(serialStream())

def serialStreamList():
    string = serialStream()
    line = string.rstrip('\n\r')
    lines = line.split(",")
    return(lines)
    
def saveSentenceTypes():
    global config
    global sentencetypes
    types = []
    x = 0
    print("Scanning for unique GPS sentences...")
    while x < 20:
        lines = serialStreamList()
        sentence = lines[0]
        types.append(sentence)
        unique = set(types)
        x += 1
        sentencetypes = unique
        #print(sentencetypes)

def sentenceLengths():
    lengths = []
    x = 0
    global sentencelengths
    while x < 20:
        lines = serialStreamList()
        segment = lines[0],len(lines)
        lengths.append(segment)
        unique = set(lengths)
        x += 1
    sentencelengths = unique   

def tupleToList():
    global sentencelengths
    a = sentencelengths
    b = [list(x) for x in a]
    return(b)

def groupItems():
    global sentencelengths
    global groupitems
    list_ = sentencelengths
    group = defaultdict(list)
    for vs in list_:
        group[vs[0]] += vs[1:]
    groupitems = group.items()
    groupitems = [list(x) for x in groupitems]
    print(groupitems)

def saveNumberSentences():
    global config
    global sentencetypes
    numbSent = len(sentencetypes)
    with open(config,'a') as f:
        f.write('totalSentences = %s\n' % numbSent)
    print("There are %s different sentences" % numbSent)

def maxOnly():
    global groupitems
    global maxlist
    global maxitems
    global finallist
    templist = []
    for list_ in groupitems:
        for item in list_:
            for length in item:
                try:
                    templist.append(int(length))
                except ValueError:
                    pass
        maxlength = max(templist)
        maxitems = list_[0], maxlength
        maxlist.append(maxitems)
        templist = []
    maxlist = [list(x) for x in maxlist]
    print(maxlist)  

def saveValues():
    global maxlist
    global groupitems
    global sentencetypes
    with open(config, 'a') as f:
        f.write("groupitems = %s\n" % groupitems)
        f.write("sentencetypes = %s\n" % sentencetypes)
        f.write("maxlist = %s\n" % maxlist)
        for i in maxlist:
            f.write("%smax = %s\n" %(i[0], i[1]))
        for i in groupitems:
            f.write("%s = %s\n" %(i[0], i[1]))

def createDatabase():
    global sentencetypes
    global db
    global conn
    global c
    global config
    i = input("Do you wish to manually specify database name? (y/n)\n")
    while True:
        if i == 'y':
            d = input("Please enter desired database name exluding '.db'")
            db = os.path.join(os.path.dirname(__file__),d+'.db')
            if os.path.exists(db)==False:
                print("Database '"+db+"' not found, creating one now...")
                break
            else:
                print("Found existing database '"+db+"', connecting...")
                break
        elif i == 'n':
            d = platform.node()
            db_file = d+'.db'
            db = os.path.join(os.path.dirname(__file__),db_file)
            if os.path.exists(db)==False:
                print("Database '"+db+"' not found, creating one now...")
                break
            else:
                print("Database '"+db+"' exists, connecting...")
                break
    conn = sqlite3.connect(db)
    c = conn.cursor()
    print("Connected to '"+db+"' OK!")
    c.execute("CREATE TABLE IF NOT EXISTS %s (unix INT)" % ('STATUS'))
    for i in sentencetypes:
        c.execute("CREATE TABLE IF NOT EXISTS %s (unix INT)" % (i))
        conn.commit()
    with open(config,'a') as f:
        f.write("db = r'%s'" % db)
        f.close
    print("Tables created OK!")

#This is some mozart script right here:
def populateTables():
    global db
    global sentencelengths
    conn = sqlite3.connect(db)
    c = conn.cursor()
    print("Populating tables in db %s" % (db))
    #c.execute("ALTER TABLE %s ADD COLUMN '%s'" % ('STATUS', 'STATUS'))
    for i in sentencelengths:
        sentence = i[0]
        length = i[1]
        print("%s = %s" %(sentence, length))
        x = 1
        while x <= length:
            try:
                c.execute("ALTER TABLE %s ADD COLUMN '%s'" % (sentence, x))
                x += 1
            except:
                x += 1
                pass
    conn.commit()
    conn.close()
    print("Wow! Such script! Much completion!")


#Probably won't do this, too taxing on storage?
def raw_log():
    log_raw = 'log_raw.txt'
    log_raw_old = 'log_raw.txt.old'
    print("Looking for log_raw.txt file...")
    if os.path.exists(log_raw)==False:
        print("No existing raw gps log file, attempting to create one...")
        try:
            open(log_raw,'w')
            open(log_raw,'w').close
        except IOError:
            print("Unable to create file")
        print("Raw GPS log file created OK!")
    else:
        d = input("Raw GPS log file already exists, do you wish to backup and delete contents? (y/n)\n")
        if d == 'y':
            try:
                shutil.copyfile(log_raw,log_raw_old)
                print("Existing GPS raw log backed up.")
                open(log_raw,'w')
                print("GPS raw log now blank.\n")
            except IOError:
                print("Unable to read file.")
        elif d == 'n':
            input("No worries, raw gps log file left alone ;)")

def start():
    print("Starting gps logging.....")
    openserial.close()
    time.sleep(2)
    try:
        import gps
    except:
        print("Unable to start gps.py")
    
def run(): 
    configBackup()
    databaseBackup()
    #checkTime()
    getSystem()
    #checkSerial()
    scanSerial()
    saveSerial()
    openComport()
    verifySerial()
    saveSentenceTypes()
    print(sentencetypes)
    sentenceLengths()
    print(sentencelengths)
    tupleToList()
    groupItems()
    saveNumberSentences()
    maxOnly()
    saveValues()
    createDatabase()
    populateTables()
    start()
    #raw_log()

run()
