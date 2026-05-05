"""
connect to the database, example conn = sqlite3.connect('dbname')
create a cursor object - used to interact with database
execute commands and SQL operations, looks like cursor.execute("string of commands", values tuple)
fetch results with cursor.fetchall() or .fetchone() from a SELECT query
commit changes with conn.commit()
close the connection with conn.close()

"""

import sqlite3

#connect to the database, or create if doesn't exist
conn = sqlite3.connect('leaderboard.db')


conn.row_factory = sqlite3.Row
# create cursor to interact with db
cursor = conn.cursor()

#create some tables if not already there
cursor.execute(""" 
CREATE TABLE IF NOT EXISTS scores (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    player_name     TEXT NOT NULL,
    score           INTEGER NOT NULL,
    game_id         INTEGER NOT NULL      
);
""")

cursor.execute(""" 
CREATE TABLE IF NOT EXISTS games (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    game_name       TEXT NOT NULL    
);
""")

bob = 'Robert"); DROP TABLE games; --'
alice = "DK"
cursor.execute(''' INSERT INTO games (game_name) VALUES ('Pac-Man') ''')

#below is the wrong way to do this, vulnerable to sql injection
#cursor.execute(' INSERT INTO games (game_name) VALUES ("' + bob + '") ')

cursor.execute(''' INSERT INTO games (game_name) VALUES (?) ''', (alice,))
cursor.execute(''' INSERT INTO scores (player_name, score, game_id) VALUES (?,?,?) ''', ("string1", 46, 3))

conn.commit()

cursor.execute(''' 
SELECT scores.player_name, scores.score, games.game_name AS game_name
FROM scores
INNER JOIN games ON scores.game_id = games.id
ORDER BY game_name, score DESC;
''')

rows = cursor.fetchall()

for row in rows:
    print(f"{row['player_name']}, {row['score']}, {row['game_name']}")

# Always close when done
conn.close()