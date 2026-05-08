"""
connect to database, example conn = sqlite.connect('dbname')
create curson obj - interact w/ db
execute commands, curson.execute("", val)
fetch results, cursor.fetchall() or fetchone() from SELECT
commit w/ conn.commit()
close connection w/ conn.close()

"""

import sqlite3

#connect to db file, or create if not exist
conn = sqlite3.connect('leaderboard.db')

#Row Factory
#row['player'] instead of row[0]
conn.row_factory = sqlite3.Row

# create cursor to interact w/ db
cursor = conn.cursor()

#create tables if not already there
cursor.execute(''' 
CREATE TABLE IF NOT EXISTS main (
	id					INTEGER PRIMARY KEY AUTOINCREMENT,
	player  			TEXT NOT NULL,
	score				INTEGER NOT NULL,
	game_id				INTEGER NOT NULL,
    date				INTEGER NOT NULL
);
''')

cursor.execute(''' 
CREATE TABLE IF NOT EXISTS games (
	id					INTEGER PRIMARY KEY AUTOINCREMENT,
	game      			TEXT NOT NULL,
    maxscore			INTEGER NOT NULL
);
''')


#bob = 'PacMan'
#rob = 'Donkey Kong'
# bob = 'Robert"); DROP TABLE games; --'     sql injection attack
# insert a game
#cursor.execute('''INSERT INTO games (game) VALUES ('Tetris') ''')

#Wrong way to do this, sql injection attack possible
#cursor.execute('INSERT INTO games (game) VALUES ("' + bob + '")')

#cursor.execute('''INSERT INTO games (game) VALUES (?) ''', (rob,))  #tuple w/ only 1 val
#cursor.execute('''INSERT INTO games (game, maxscore) VALUES (?,?) ''', ('ROMPERS',545160))
#cursor.execute('''INSERT INTO testB (player, score, game_id) VALUES (?,?,?) ''', ('Yeva', 272913, 1))

#conn.commit()

cursor.execute('''
SELECT main.player, main.score, games.game as game_id
FROM main
INNER JOIN games ON main.game_id = game_id
ORDER BY game_ID, score DESC;
''')

rows = cursor.fetchall()
#print(rows[1]['player'])

for row in rows:
    print(f"{row['player']}, {row['score']}, {row['game_id']}")

#always cose connection when done
conn.close()