import sqlite3
import os.path

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

conn = sqlite3.connect(f'{BASE_DIR}/db/creds.db')
cursor = conn.cursor()

print("Opened database successfully")

cursor.execute('''DROP TABLE LOGINS;''')
cursor.execute('''CREATE TABLE LOGINS(
         ID                         INTEGER PRIMARY KEY         ,
         FULLNAME                   TEXT                NOT NULL,
         USERNAME                   VARCHAR(30)         NOT NULL,
         EMAIL                      EMAIL               NOT NULL,
         PASSWORD                   VARCHAR(16)         NOT NULL,
         DATE                       TEXT                NOT NULL);''')
conn.commit()

print("Table created successfully")

conn.close()