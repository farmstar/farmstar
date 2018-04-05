from dicts import *


'''
Parses a serial line with a checksum value at the end
Returns dictionary with status, valid, calculated, checksum
Returns valid = False if checksum bad
'''


class parse():
    def __init__(self,line=''):
        self.CHECKSUM = CHECK.SUM
        self.line = line
        self.check()


    def check(self):
        #Remvove newline
        self.sentence = self.line.rstrip('\n\r')
        #Retrieve data excluding checksum
        self.data = self.sentence[1:-3]
        #Retreive checksum value
        self.checksum = self.sentence[-2:]
        #Start xor checksum calculation at 0
        self.data_check = 0
        #For each character do a xor with previous
        for c in self.data:
            self.data_check ^= ord(c)
        #Add a '0x' to the front of the checksum
        self.hex_checksum = '0x'+self.checksum.lower()
        #Convert to hex
        self.hex_data = format(self.data_check, '#04x')
        if self.hex_data == self.hex_checksum:
            self.CHECKSUM['valid'] = True
            self.CHECKSUM['status'] = '[OK]'
        else:
            self.CHECKSUM['valid'] = False
            self.CHECKSUM['status'] = '[Fail]'
        self.CHECKSUM['calculated'] = self.hex_data
        self.CHECKSUM['checksum'] = self.hex_checksum
    

if __name__ == '__main__':
    CHECKSUM = parse('$GPGGA,024106,3321.9308,S,11537.59819,E,1,21,1.0,-8.313,M,-30.9,M,,*63').CHECKSUM
    print(CHECKSUM['valid'])
    print(CHECKSUM['status'])
    print(CHECKSUM['calculated'])
    print(CHECKSUM['checksum'])
