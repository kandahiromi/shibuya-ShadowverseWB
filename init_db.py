import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE matches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        my_deck TEXT NOT NULL,
        opponent_deck TEXT NOT NULL,
        turn_order TEXT NOT NULL,
        result TEXT NOT NULL,
        turns INTEGER NOT NULL,
        stream_num INTEGER NOT NULL,
        memo TEXT
    )
''')

conn.commit()
conn.close()
print("✅ DB初期化完了")
