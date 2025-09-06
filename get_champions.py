import sqlite3

conn = sqlite3.connect("chess_app.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM champions WHERE country = 'Soviet Union'")
for row in cursor.fetchall():
    print(row)

conn.close()
