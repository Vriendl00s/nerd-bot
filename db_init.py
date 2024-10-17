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

cursor.execute('''CREATE TABLE IF NOT EXISTS levels 
                (user_id INTEGER NOT NULL, server_id INTEGER NOT NULL, xp INTEGER NOT NULL, level INTEGER NOT NULL)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS leveling_roles
                (server_id INTEGER NOT NULL, role_id INTEGER NOT NULL, level INTEGER NOT NULL)''')

conn.close()

# clear_db = "DELETE FROM moderation"
#ik db_conn(clear_db, commit=True)

query = "UPDATE levels SET xp = 350, level = 1 WHERE user_id = 1026491248904785970 AND server_id = 1288971299909144648"
db_conn(query, commit=True)