import sqlite3
import json

# JSON Data: First 10 World Chess Champions
champions = [
    {"name": "Wilhelm Steinitz", "year": "1886", "country": "Austria"},
    {"name": "Emanuel Lasker", "year": "1894", "country": "Germany"},
    {"name": "José Raúl Capablanca", "year": "1921", "country": "Cuba"},
    {"name": "Alexander Alekhine", "year": "1927", "country": "Russia"},
    {"name": "Max Euwe", "year": "1935", "country": "Netherlands"},
    {"name": "Mikhail Botvinnik", "year": "1948", "country": "Soviet Union"},
    {"name": "Vasily Smyslov", "year": "1957", "country": "Soviet Union"},
    {"name": "Mikhail Tal", "year": "1960", "country": "Soviet Union"},
    {"name": "Tigran Petrosian", "year": "1963", "country": "Soviet Union"},
    {"name": "Boris Spassky", "year": "1969", "country": "Soviet Union"}
]

# 1. Connect (or create) database file
conn = sqlite3.connect("chess_app.db")
cursor = conn.cursor()

# 2. Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS champions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    year TEXT,
    country TEXT
)
""")

# 3. Insert data (only if table is empty)
cursor.execute("SELECT COUNT(*) FROM champions")
if cursor.fetchone()[0] == 0:
    for champ in champions:
        cursor.execute(
            "INSERT INTO champions (name, year, country) VALUES (?, ?, ?)",
            (champ["name"], champ["year"], champ["country"])
        )

# 4. Query Example: All champions from Soviet Union
cursor.execute("SELECT name, year FROM champions WHERE country = 'Soviet Union'")
results = cursor.fetchall()

print("Soviet Union Champions:")
for row in results:
    print(f"- {row[0]} ({row[1]})")

# Save and close
conn.commit()
conn.close()