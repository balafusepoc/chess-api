import sqlite3

champions = [
    {"name": "1.Wilhelm Steinitz", "year": "1886", "country": "Austria"},
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

# 1. Connect (creates db file if not exists)
conn = sqlite3.connect("chess_app.db")
cursor = conn.cursor()

# 2. Create champions table
cursor.execute("""
CREATE TABLE IF NOT EXISTS champions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    year TEXT,
    country TEXT
)
""")

# 3. Insert data only if table is empty
cursor.execute("SELECT COUNT(*) FROM champions")
if cursor.fetchone()[0] == 0:
    for champ in champions:
        cursor.execute(
            "INSERT INTO champions (name, year, country) VALUES (?, ?, ?)",
            (champ["name"], champ["year"], champ["country"])
        )

# 4. Save & close
conn.commit()
conn.close()

print("✅ Database setup complete. Champions inserted!")
