import serial
import time
       
        
def stream(port = None):
    ser = None
    if port == None:
        print("No port specified")
    while True: 
        try:
            if(ser == None or line == ''):
                ser = serial.Serial(port,9600,timeout=1.5)
                comstatus = "Reconnecting"
            line = ser.readline().decode("utf-8").rstrip("\n\r") # Read the entire string
            print(line)
        except:
            if(not(ser == None)):
                ser.close()
                ser = None
                print("Disconnecting")
            print("No Connection to {}".format(port))
            time.sleep(2)




if __name__ == '__main__':
    stream("COM5")
