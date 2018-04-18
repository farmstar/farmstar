import sqlite3
import os
import sys

'''
Temporary database thing
Logging lat, lon, alt for now
Database in the project root folder \ data
Only supporting one at this stage
'''



class logging():
    
    def __init__(self):
        self.project_root = os.path.abspath(os.path.join('..\..'))
        self.user_data = os.path.join(self.project_root, 'data')
        print(self.user_data)
        self.count = 0
        try:
            if os.path.exists(os.path.join(self.project_root, 'data')):
                print("Launched from backend")
                sys.path.append(self.project_root)
                from data import config
            elif os.path.exists('data'):
                print("Launched from project root")
                sys.path.append(os.path.dirname(os.path.join('..')))
                import data.config
            self.test()
        except:
            print('Failed')
        

    def test(self):
        db_exists = 0
        print("Scanning for existing databases.....")
        for file in os.listdir(self.user_data):
            if file.endswith(".db"):
                print("Found database {}...".format(file))
                self.db = os.path.join(self.user_data,file)
                db_exists = True
        if db_exists == True:
            self.connect()
            print(self.db)
        else:
            print('no database exists')
            self.db = 'fsdb.db'

    def connect(self):
        self.conn = sqlite3.connect(self.db)
        self.c = self.conn.cursor()
        print("Connected to database OK!")
        self.tables()

    def tables(self):
        self.c.execute("CREATE TABLE IF NOT EXISTS LOCATION (unix INT)")
        print('Created tables OK!')
        self.columns()

    def columns(self):
        self.column_names = ['lat','lon','alt']
        try:
            for i in self.column_names:
                self.c.execute("ALTER TABLE LOCATION ADD COLUMN %s" % (i))
        except:
            print('Columns already exist')
        print('Created columns OK!')


    def data(self, data):

        self.c.execute('INSERT INTO LOCATION VALUES (?,?,?,?)' ,data)
        self.c.execute("DELETE FROM LOCATION WHERE unix IS NULL OR trim(unix) = ''")
        self.count += 1
        if self.count > 10:
            self.conn.commit()
            self.count = 0
        



if __name__ == '__main__':
    db = logging()
    GPS = {'SPACETIME':{'unix':123},
           'GGA':{'Latitude':456,
                  'Longitude':789,
                  'Altitude':101}
           }

                    
    for x in range(11):
        db.data(GPS)
