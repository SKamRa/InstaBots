import datetime
import sqlite3
import os.path

def new(fullname, username, email, password):
    print("[*] Connection to the database")
    
    today = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    data = (fullname, username, email, password, today)
    
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    conn = sqlite3.connect(f'{BASE_DIR}/db/creds.db')
    print("[*] Successfully connected!")
    
    cursor = conn.cursor()
    
    insertion = '''INSERT INTO LOGINS(ID, FULLNAME, USERNAME, EMAIL, PASSWORD, DATE)'''
    insertion += f'''VALUES(NULL, ?, ?, ?, ?, ?);'''

    cursor.execute(insertion, data)
    conn.commit()
    conn.close()