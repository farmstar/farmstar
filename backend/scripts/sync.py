import serial
import com




def getCom():
    global comport
    comport = com.scanSerial()[0]


def readSerial():
    ser = serial.Serial(comport,9600,timeout=1.5)
    line = ser.readline().decode('utf-8')
    sentence = line.rstrip('\n\r').split(',')
    return(sentence)


def setTime():
    #Get system in seperate .py?

    
    os.system('time %s' % (time))



def run():
    getCom()
    readSerial()

run()
