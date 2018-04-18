import serial
import sys
import glob
import fs_checksum

class Ports():
    """
    Scans for active serial ports and then checks those for GPS data, returning a list of valid ports.
    Optionally pass a list of serial ports to test. eg ["COM1","COM5"]
    """
    
    def __init__(self, ports=None):
        self.ports = ports
        self.active = []
        self.valid = []
        
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
        print("Scanning port %s for GPS data..." % (port))
        ser = serial.Serial(port,9600,timeout=1.5) #open serial port
        count = 0
        for _ in range(5): #read 5 lines only (loop code 5 times)
            line = ser.readline().decode("utf-8") #read serial line
            valid = fs_checksum.parse(line)
            if valid == True:
                print("Checksum.....[OK]")
                count += 1
            else:
                print("Checksum.....[Fail]")
        if count == 5:
            self.valid.append(port)
            print("GPS Data Found on Port: {}".format(port))
        else:
            print("Invalid data on port %s" % (port))
        ser.close()
        


if __name__ == '__main__':
    Ports()
    #Ports(["COM1","COM3","COM5"])
