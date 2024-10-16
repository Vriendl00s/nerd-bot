import sqlite3
from db_connection import db_conn

conn = sqlite3.connect('bot.db')

cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS moderation
               (user_id INTEGER NOT NULL, server_id INTEGER NOT NULL, type TEXT NOT NULL, until TEXT, reason TEXT NOT NULL)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS online_channel
               (channel_id INTEGER NOT NULL, guild_id INTEGER NOT NULL)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS reminders
               (user_id INTEGER NOT NULL, message TEXT NOT NULL, time TEXT NOT NULL)''')

conn.close()

# clear_db = "DELETE FROM moderation"
# db_conn(clear_db, commit=True)