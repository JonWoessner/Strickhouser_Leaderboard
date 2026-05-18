from flask import Flask, render_template, request, redirect, url_for
import datetime
import sqlite3
import os, time


app = Flask(__name__)
DATABASEPATH = 'leaderboard.db' #path to database

def get_current_game():
    '''divide current time to 45s windows to cycle through game titles'''
    game_num = int(time.time() / 45) % 10 ##replace 3 with number of games in db
    return game_num + 1 ##db starts indexing at 1, mod starts at 0

def get_db_connection():
    '''Setup db connection and return conn obj'''
    conn = sqlite3.connect(DATABASEPATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    '''Inits a db if not already exist'''
    conn = get_db_connection()
    ##TODO Finish using code from example
    conn.close()
    pass


scores = [
    {'player': 'Ada', 'score': 9800, 'year': '20XX'},
    {'player': 'Grace', 'score': 8750, 'year': '20XX'},
    {'player': 'Alan', 'score': 7200, 'year': '20XX'},
    {'player': 'Linus', 'score': 6500, 'year': '20XX'},
    {'player': 'Bjarne', 'score': 5900, 'year': '20XX'},
    {'player': 'Kevin', 'score': 4000, 'year': '20XX'},
    {'player': 'Luke', 'score': 10450, 'year': '20XX'},
    {'player': 'Ava', 'score': 7780, 'year': '20XX'}
    ]

valid_games = [
    {'game': 'PACMAN', 'max_score': 10000},
    {'game': 'DIGDUG', 'max_score': 10000},
    {'game': 'FROGGER', 'max_score': 10000},
    {'game': 'GALAGA', 'max_score': 10000},
    {'game': 'MAPPY', 'max_score': 10000},
    {'game': 'MS.PACMAN', 'max_score': 10000},
    {'game': 'TETRIS', 'max_score': 10000},
    {'game': '1970', 'max_score': 10000},
    {'game': 'UNKNOWN', 'max_score': 10000},
    {'game': 'UNKNOWN', 'max_score': 10000}
]

valid_game = {'PACMAN': 10000,
              'DIGDUG': 10000,
              'FROGGER': 10000,
              'GALAGA': 10000,
              'MAPPY': 10000,
              'MS.PACMAN': 10000,
              'TETRIS': 10000,
              '1970': 10000,
              'UNKNOWN1': 10000,
              'UNKNOWN2': 10000}


@app.route('/')
def home():
    page_title = "Strickhouser Arcade"
    return render_template('index.html', title=page_title)




@app.route('/leaderboard_base')
def lead_base():
    page_title = "Game"
    #sorted_scores = sorted(scores, key= lambda entry: entry == {'score'}, reverse = True)
    ## TODO change SELECT to grab 1 game at a time

    conn = get_db_connection()
    dbscores = conn.execute('''
        SELECT  main.player, 
                main.score, 
                games.game AS game_id,
                main.date
        FROM main
        INNER JOIN games ON main.game_id = games.id
        ORDER BY main.score DESC;
    ''').fetchall()
    conn.close()

    return render_template(
    'leaderboard_base.html', 
    score_count = len(dbscores),
    title = page_title,
    scores = dbscores,
    count=2
    )


def new_score_highlight(date):
    current_time = datetime.datetime.now().strftime("%m/%d/%Y")
    if int(date[3:5]) > int(current_time[3:5]) and int(date[:2]) + 1 == int(current_time[:2]):
        highlight = True
    elif int(date[:2]) == int(current_time[:2]):
        highlight = True
    else:
        highlight = False
    print(highlight)
    return highlight



@app.route('/newentry', methods=['GET', 'POST'])
def submit():
    game = None
    name = None
    score = None
    date = None

    error = None

    form_values = {'player': '','game': '','score': '','date': ''}



    # this runs when user 1st enters form submission page
    conn = get_db_connection()
    game_list = conn.execute('''SELECT id, game FROM games ORDER BY game''').fetchall()
    
    


    if request.method == 'POST':
        game = request.form['game_id'].strip().upper()
        name = request.form['pname'].strip().capitalize()
        #score = int(request.form['score'])
        date = request.form['pgradyear']


        if new_score_highlight(date):
            highlight = True
        else:
            highlight = False


        if not name or not game:
            error = 'Blank Field'
            print('Are you sure there is anything there')
        
        try:
            score = int(request.form['score'])
        except:
            error = "What kinda number is that"
            print('Are you sure thats a number')
            score=0

        #try:
        #    request.form['gameid'].strip().upper() == valid_game.keys()
        #except:
        #    error = "Invalid Game ID"
        #    print('Are you sure thats a real game')
            #print('Input', request.form['gameid'].upper().strip())
            #print('Pair', valid_game.keys())
        #    game=''
            
            #if request.form['gameid'].strip().upper() == valid_game.keys('PACMAN'):
            #    pass



        form_values = {'player': name,'game': game,'score': score,'date': date}


        if error == None:
            #scores.append({'player': name, 'score': score, 'year': date})
            conn.execute('''
                INSERT INTO main (player, score, game_id, date) VALUES (?,?,?,?)
            ''', (name, score, game, date))
            conn.commit()
        
    conn.close()
    return render_template(
        'form.html', 
        game=game, 
        name=name, 
        score=score, 
        date=date, 
        error=error, 
        form_values=form_values,
        games=game_list
        )


#setup db if not done
init_db()

if __name__ == "__main__":
    app.run(debug=True)
