'''
Blank GSA dictionary for storing processed nmea data
'''

GSA = {'string':'',
       'sentence':'',
       'talker':'',
       'message':'',
       'nmea':'',
       'a/m':'',
       'selection':'',
       'type':'',
       'mode':'',
       'PRNs':(),
       'PDOP':'',
       'HDOP':'',
       'VDOP':'',
       'Checksum':'',
       'Calculated':'',
       'Check':'',
       'Count_total':0,
       'Count_bad':0,
       'Count_good':0,
       }

ALL = {'list':[],
       'count':0,
       'GSA':{},
       'GPGSA':{},
       'GLGSA':{},
       'GNGSA':{},
       }
