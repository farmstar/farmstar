import serial
import time
import os
import sys
import sqlite3
import datetime


'''
Farmstar backend tests script
Runs setup if necessary
Launches GPS logging once tests pass
'''

#Import Config
def getConfig():
    project_root = os.path.abspath(os.path.join('..\..'))
    try:
        if os.path.exists(os.path.join(project_root, 'data')):
            print("Launched from backend")
            sys.path.append(project_root)
            from data import config
        elif os.path.exists('data'):
            print("Launched from project root")
            sys.path.append(os.path.dirname(os.path.join('..')))
            import data.config
    except:
        return(False)


#Database name from config check
def getDB():
    try:
        global db
        db = config.db
    except:
        return(False)


#Database file check
def DBfile():
    try:
        if os.path.exists(db)==False:
            return(False)
    except:
        return(False)


#Serial Port config
def getComport():
    try:
        global comport
        comport = config.comport
    except:
        return(False)


#Serial port connection
def testComport():    
    try:
        ser = serial.Serial(comport,9600,timeout=1.5)
        ser.readline().decode("utf-8")
    except:
        return(False)


#Test the GPS data stream using the checksum value
def serialTest():
    print("Validating GPS data.....")
    try:
        ser = serial.Serial(comport,9600,timeout=1.5) #open serial port
        for _ in range(5): #read 5 lines only (loop code 5 times)
            line = ser.readline().decode("utf-8") #read serial line 
            sentence = line.rstrip('\n\r') #remove the newline
            data = sentence[1:-3] #Gets 2nd to 4th last character in sentence to get nmea data
            checksum = sentence[-2:] #Gets last 2 characters (checksum)
            data_check = 0 #Start the xor operation at 0
            for c in data: #For each character in the nmea sentence
                data_check ^= ord(c) #Does a xor operation between previous character and current character
            hex_checksum = '0x'+checksum.lower() #adds '0x' to the front of the device checksum and makes it lowercase
            hex_data = format(data_check, '#04x')#converts to hex
            if hex_data == hex_checksum:
                print("%s = %s.....[OK]" % (hex_checksum, hex_data))
            else:
                print("%s != %s.....[Fail]" % (hex_checksum, hex_data))
                return(False)        
    except:
        return(False)


    

#List of functions and description (checks)
checklist = [[getConfig, "Get config"],
             [getDB, "Get database name"],
             [DBfile, "Database file"],
             [getComport, "Get comport"],
             [testComport, "Testing comport"],
             [serialTest, "Validate gps data"],
             ]

# running through checks and printing result
def main():
    test_fails = 0
    try:
        for each_check in checklist:
            check_function = each_check[0]
            check_name = each_check[1]
            if check_function() == False:
                print("%s.....[Fail]" %(check_name))
                test_fails += 1
            else:
                print("%s.....[OK]" %(check_name))
    except:
        print("Self checks.....[Fail]")
        print("Initiating setup.....")
        runSetup()
    if test_fails > 0:
        runSetup()
    else:
        print("Starting GPS.....")
        time.sleep(2)
        try:
            import gps
        except:
            print("GPS Processing.....[Fail]")
        
            
def runSetup():
    print("Initiating setup.....")
    try:
        import setup
        setup.run()
        #import gps
    except:
        print("Run setup.....[Fail]")
        
if __name__ == "__main__":
    main()
