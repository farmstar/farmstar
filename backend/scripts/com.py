import serial
import sys
import glob

class Ports():
    """
    Scans for active serial ports and then checks those for GPS data, returning a list of valid ports.
    Optionally pass a list of serial ports to test. eg ["COM1","COM5"]
    """
    
    def __init__(self, ports=None):
        self.ports = ports
        self.valid = []
        self.active = []
        
        if self.ports is None:
            self.scan()
            if self.active == None:
                print("No active serial ports")
            else:
                for port in self.active:
                    self.test(port)
                print("Valid GPS ports = {}".format(self.valid))
        else:
            for port in self.ports:
                self.test(port)
            print("Valid GPS ports = {}".format(self.valid))        
    
    def scan(self):
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')
        for port in ports:
            try:
                print("Testing port %s" % (port))
                ser = serial.Serial(port,9600,timeout=1.5)
                for _ in range(5):
                    ser.readline().decode("utf-8")
                ser.close()
                self.active.append(port)
            except (OSError, serial.SerialException):
                pass
        print("Active ports = {}".format(self.active))

    def test(self, port):
        try:
            print("Scanning port %s for GPS data..." % (port))
            ser = serial.Serial(port,9600,timeout=1.5) #open serial port
            count = 0
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
                    count += 1
                else:
                    print("%s != %s.....[Fail]" % (hex_checksum, hex_data))
            if count == 5:
                self.valid.append(port)
                print("GPS Data Found on Port: {}" % ', '.format(port))
            else:
                print("Invalid data on port %s" % (port))
            ser.close()
        except:
            pass

        


if __name__ == '__main__':
    Ports()
    #Ports(["COM1","COM3","COM5"])
