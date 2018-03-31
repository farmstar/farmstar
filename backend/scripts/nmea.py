import time
from dateutil import tz
from datetime import datetime
from dicts import *
import fs_checksum


GGA = GGA.GGA


'''
Farmstar nmea data parser
Converts GPS data into a list of dictionaries
Returns the dictionary list
'''

#parse raw nmea data (one line at a time):
def parse(line):
    #Remove newline
    stripped = line.rstrip('\n\r')
    #Split into a list format
    sentence = stripped.split(",")
    #Get the sentence type
    NMEA = sentence[0][3:]
     if NMEA == 'GGA':
        GGA(sentence)  
    else:
        pass

def GGA(sentence):
        #Send to checksum parser
        check = fs_checksum.parse(line)
        #Count the total/good/bad strings
        GGA['Count_total'] += 1
        if check == True:
            GGA['Count_good'] += 1
        else:
           GGA['Count_bad'] += 1
        #Timezone calculations and conversions:
        #(Assuming local time is precise)
        #(I know this is messy)
        #Get UTC timezone object:
        from_zone = tz.tzutc()
        #Get local timezone object:
        to_zone = tz.tzlocal()
        #Convert GPS fix to a datetime object:
        fixtime = datetime.strptime(sentence[1], '%H%M%S')
        #Formats the GPS fix time:
        fixutc = fixtime.strftime('%H:%M:%S')
        #Get the local time in UTC:
        localutc = datetime.utcnow()
        #Get the local date converted to UTC:
        #(UTC date will be different to local date at certain times)
        utcdate = localutc.strftime('%Y-%m-%d')
        #Prepend local utc date to the gps fix time:
        gpsutcdatetime = str("%s %s" % (utcdate, fixutc))
        #Convert back to a datetime object
        fixutcdatetime = datetime.strptime(gpsutcdatetime, '%Y-%m-%d %H:%M:%S')
        #Tell datetime it is in the UTC timezone
        gpsdatetime = fixutcdatetime.replace(tzinfo=from_zone)
        #Convert the GPS fix datetime from UTC to local timezone
        gpslocal = gpsdatetime.astimezone(to_zone)
        #Extract the time only
        fixlocal = gpslocal.strftime('%H:%M:%S')
        #Get local datetime
        localdatetime = datetime.now()
        #Tell datetime the local timezone
        localdatetimezone = localdatetime.replace(tzinfo=to_zone)
        #Local time to compare with GPS fix time
        localtime = localdatetime.strftime('%H:%M:%S')
        #Calculate the fix age
        age = (localdatetimezone-gpslocal).total_seconds()
        
        GGA['Fix'] = fixlocal
        GGA['Local_time'] = localtime
        GGA['Age'] = age
        
        GGA['String'] = stripped
        GGA['Sentence'] = sentence[0][1:]
        GGA['Checksum'] = hex_checksum
        GGA['Calculated'] = hex_data
        GGA['Check'] = check

        lat = sentence[2][:2].lstrip('0') + "." + "%.7s" % str(float(sentence[2][2:])*1.0/60.0).lstrip("0.")
        if sentence[3] == 'S':
            GGA['Latitude'] = float(lat)*-1
        else:
            GGA['Latitude'] = float(lat)
        GGA['North/South'] = sentence[3]

        lon = sentence[4][:3].lstrip('0') + "." + "%.7s" % str(float(sentence[4][3:])*1.0/60.0).lstrip("0.")
        GGA['Longitude'] = float(lon)
        GGA['East/West'] = sentence[5]

if __name__ == '__main__':
    parse('$GPGGA,024106,3321.9308,S,11537.59819,E,1,21,1.0,-8.313,M,-30.9,M,,*63')


