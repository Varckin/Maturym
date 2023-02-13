import sqlite3 as data_base

class Data_base():

        db = data_base.connect('db_station.db')
        cursor = db.cursor()

        def create_table(self):

            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS STATION (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    link TEXT
                    );
                """)
            self.db.commit()

        def first_station(self):

            add_command = 'INSERT INTO STATION (name, link) VALUES(?, ?)'
            first_data_station = [
                ('Record', 'https://radiorecord.hostingradio.ru/rr_main96.aacp'),
                ('Chill House', 'http://radio-srv1.11one.ru/record192k.mp3'),
                ('Innocence', 'https://radiorecord.hostingradio.ru/ibiza96.aacp'),
                ('VIP House', 'https://radiorecord.hostingradio.ru/vip96.aacp'),
                ('Progressive', 'https://radiorecord.hostingradio.ru/progr96.aacp'),
                ('Future House', 'https://radiorecord.hostingradio.ru/fut96.aacp'),
                ('Radio None', 'http://uk2.internet-radio.com:8024/')
            ]

            self.cursor.executemany(add_command, first_data_station)
            self.db.commit()

DB = Data_base()
DB.create_table()

request = DB.cursor.execute('SELECT * FROM STATION').fetchall()
if request == []:
    DB.first_station()