import sqlite3

def db_conn(query, commit=False):
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute(query)
    if commit:
        conn.commit()
    else:
        result = cursor.fetchall()
        conn.close()
        return result
    conn.close()

    return None

