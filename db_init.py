import sqlite3
from db_connection import db_conn

conn = sqlite3.connect('bot.db')

cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS moderation
               (UID INTEGER NOT NULL, server_ID INTEGER NOT NULL, type TEXT NOT NULL, until TEXT, reason TEXT NOT NULL)''')


conn.close()

clear_db = "DELETE FROM moderation"
db_conn(clear_db, commit=True)