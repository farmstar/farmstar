


'''
Parses a serial line with a checksum value at the end
Returns True if checksum good
Returns False if checksum bad
'''


def parse(line):
    #Remvove newline
    sentence = line.rstrip('\n\r')
    #Retrieve data excluding checksum
    data = sentence[1:-3]
    #Retreive checksum value
    checksum = sentence[-2:]
    #Start xor checksum calculation at 0
    data_check = 0
    #For each character do a xor with previous
    for c in data:
        data_check ^= ord(c)
    #Add a '0x' to the front of the checksum
    hex_checksum = '0x'+checksum.lower()
    #Convert to hex
    hex_data = format(data_check, '#04x')
    if hex_data == hex_checksum:
        return(True)
    else:
        return(False)

if __name__ == '__main__':
    valid = parse('$GPGGA,024106,3321.9308,S,11537.59819,E,1,21,1.0,-8.313,M,-30.9,M,,*63')
    print(valid)
