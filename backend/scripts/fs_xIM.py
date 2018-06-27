import bs4 as bs
import requests
from multiprocessing import Pool
import utm
import sqlite3
import time
from dicts import IPLIST, XIM




utmnum = 50
utmlet = 'K'
iplist = IPLIST.XIM
ximinfo = XIM.INFO
ximlist = {}


def scrape(ip):
    url = ''.join(['http://', ip, ':3785/getinfocore'])

    try:
        resp = requests.get(url, timeout=1)
        soup = bs.BeautifulSoup(resp.text, 'lxml')
        device = soup.find("td", text='Device ID:').find_next_sibling('td').text
        easting = soup.find("td", text='Easting (m):').find_next_sibling('td').text
        northing = soup.find("td", text='Northing (m):').find_next_sibling('td').text
        elevation = soup.find("td", text='Elevation (m):').find_next_sibling('td').text
        latlon = utm.to_latlon(float(easting),float(northing),utmnum,utmlet)

        ximinfo['device'] = device
        ximinfo['ip'] = ip
        ximinfo['easting'] = easting
        ximinfo['northing'] = northing
        ximinfo['elevation'] = elevation
        ximinfo['latitude'] = latlon[0]
        ximinfo['longitude'] = latlon[1]

        return(ximinfo)
        
    except:
        pass






if __name__ == '__main__':
    iplist = IPLIST.XIM
    how_many = len(iplist)
    p = Pool(processes=how_many)
    conn = sqlite3.connect('xim.db')
    c = conn.cursor()
    while True:
        results = [p.apply_async(scrape, args=(ip,)) for ip in iplist]
        output = [p.get() for p in results]
        for i in output:
            data = []
            if i != None:
                dev = i['device']
                ximlist[dev] = i
                c.execute(("CREATE TABLE IF NOT EXISTS {} (unix INT)").format(dev))
                for key in i:
                    try:
                        c.execute(("ALTER TABLE {} ADD COLUMN {}").format(dev,key))
                    except:
                        data.append(i[key])
                unix = [time.time()]
                final_data = unix+data
                print(final_data)
                if len(final_data) == 8:
                    c.execute(('INSERT INTO {} VALUES (?,?,?,?,?,?,?,?)').format(dev) ,final_data)
                conn.commit()
    
    
