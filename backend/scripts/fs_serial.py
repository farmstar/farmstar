import serial
import time
from dicts import *
       
'''
Farmstar serial module
Call stream once then call data in a loop
(see main)

'''
        

class stream():
    def __init__(self, port):
        self.serial = SERIAL.SERIAL
        self.port = port
        self.ser = None
        self.line = ''
        self.status = "Initializing"
        self.serial['status'] = self.status

    def data(self):
        self.status = "Starting"
        try:
            if(self.ser == None or self.line == ''):
                self.ser = serial.Serial(self.port,9600,timeout=1.5)
                self.status = "Reconnecting"
            self.line = self.ser.readline().decode("utf-8").rstrip("\n\r") # Read the entire string
            self.status = "Running"
        except:
            if(not(self.ser == None)):
                self.ser.close()
                self.ser = None
                self.status = "Disconnecting"
            self.status = "No Connection to {}".format(self.port)
            time.sleep(2)
        self.serial['status'] = self.status
        self.serial['port'] = self.port
        self.serial['line'] = self.line
        return(self.serial)




if __name__ == '__main__':
    Stream = stream('COM5')
    while True:
        print(Stream.data())
        
