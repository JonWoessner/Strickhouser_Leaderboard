from flask import Flask, render_template, request, redirect, url_for
import datetime
import sqlite3
import os, time


app = Flask(__name__)

DATABASEPATH = '/home/lhoak/Projects/Strickhouser_Leaderboard/leaderboard.db'

def get_current_game():
    game_num = int(time.time() / 30) % 3 # replace 3 with number of game titles in the database
    return game_num + 1
def get_db_connection():
    conn = sqlite3.connect(DATABASEPATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    ## TODO finish out using code from our examples
    conn.close()

scores = [
    {'player': 'Ada', 'game': 'Snake', 'score': 9800, 'date': '02/11/2008'},
    {'player': 'Grace',  'game': 'DK', 'score': 8750, 'date': '02/11/2008' },
    {'player': 'Alan', 'game': 'Digdug', 'score': 7200, 'date': '02/11/2008' },
    {'player': 'Linus', 'game': 'DK', 'score': 6500, 'date': '02/11/2008' },
    {'player': 'Bjarne', 'game': 'Mappy',  'score': 5900, 'date': '02/11/2008' },
    {'player': 'Kevin', 'game': 'Pacman',  'score': 4000, 'date': '02/11/2008' },
    {'player': 'Luke', 'game': 'Pacman',  'score': 10450, 'date': '02/11/2008' },
    {'player': 'Ava', 'game': 'Digdug',  'score': 7780, 'date': '02/11/2008' }
    ]

@app.route('/')
def home():
    page_title = "Title of thou Home"
    return render_template('index.html', title=page_title)



@app.route('/submit', methods=['GET', 'POST'])

def submit():

    name = ''
    game = ''
    score = ''
    date = ''
    error = ''
    form_values = apply_form_values()
    games = ['pacman', 'dk', 'snake', 'digdug']
    max_scores = {
    'pacman': 100000, 'dk': 12345, 'snake': 100, 'digdug': 1000
    }


    conn = get_db_connection()
    games_list = conn.execute(''' 
    SELECT id, game_name FROM games ORDER BY game_name;
    ''').fetchall()
    conn.close()

    if request.method == 'POST':
        name = request.form['name'].strip()
        game = request.form['game'].strip()
        date = request.form['date'].strip()

        if not name or not game:
            error = "Blank Fields"
            print('user left fields blank!')
        

        try:
            score = int(request.form['score'].strip())
        except ValueError:
            error = "score"
            score = 0
        

        try:
            month = int(date[:2])
            day = int(date[3:5])
            year = int(date[6:])
            formatted_date = datetime.date.today().strftime("%m/%d/%Y")
        except ValueError:
            error = "date"
            date = 0
        try:
            if month > 12 or month < 00:
                error = "Invalid date"
            elif day >= 31 or day < 0:
                error = "Invalid date"
            elif year < 2000 or year > int(formatted_date[6:]):
                error = "date"
        except UnboundLocalError:
            error = "date"

        if not (name.isalpha()) or len(name) > 20:
            error = "name"
        
        
        form_values = apply_form_values(name, game, score, date)
        # only append score if no errors
        if error == None:
            scores.append(form_values)
        
        if error == None:
            conn.execute('''
        INSERT INTO scores (player_name, score, game_id) VALUES (?,?,?)
        ''', (name, score, game))
        conn.commit()

    return render_template('forms.html', name=name, error=error, form_values=apply_form_values(name, game, score, date), options=games_list)

def apply_form_values(name='', game='', score='', date=''):

    return {'player': name, 'game': game, 'score': score, 'date': date}

@app.route('/leaderboard_base')
def lead_base():
    page_title = "Game"
    conn = get_db_connection()
    ## TODO change select to grab one game at a time, using the current time func we built
    dbscores = conn.execute(''' 
        SELECT  scores.player_name,
                scores.score,
                games.game_name AS game_name
        FROM scores
        INNER JOIN games ON scores.game_id = games.id
        ORDER BY scores.score DESC
''').fetchall()
    return render_template(
    'leaderboard_base.html', 
    score_count = len(scores),
    title = page_title,
    scores = dbscores,
    count=2
    )


if __name__ == "__main__":
    app.run(debug=True)
