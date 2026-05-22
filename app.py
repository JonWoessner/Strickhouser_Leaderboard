from flask import Flask, render_template, request, redirect, url_for
import datetime
import sqlite3
import os, time


app = Flask(__name__)
DATABASEPATH = 'leaderboard.db' #path to database
NUMGAMES = 10

def get_current_game():
    '''divide current time to 45s windows to cycle through game titles'''
    game_num = int(time.time() / 15) % NUMGAMES 
    return game_num + 1 ##db starts indexing at 1, mod starts at 0

game_images = [
    "/static/images/Pacman.jpg"
    "/static/images/Frogger.jpg"
    "/static/images/Ms. Pacman.jpg"
    "/static/images/Digdug.jpg"
    "/static/images/BurgerTime.jpg"
    "/static/images/1942.jpg"
    "/static/images/Donkey Kong.jpg"
    "/static/images/Galaga.jpg"
    "/static/images/Mappy.jpg"
    "/static/images/Rompers.jpg"
]

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


@app.route('/')
def home():
    page_title = "Strickhouser Arcade"
    return render_template('index.html', title=page_title)




@app.route('/leaderboard_base')
def lead_base():
    #sorted_scores = sorted(scores, key= lambda entry: entry == {'score'}, reverse = True)
    ## TODO change SELECT to grab 1 game at a time

    conn = get_db_connection()
    gamenum = get_current_game()   #get current game via time
    print("gamenum=",gamenum)
    dbscores = conn.execute(f'''
        SELECT  main.player, 
                main.score, 
                games.game AS game_id,
                main.date
        FROM main
        INNER JOIN games ON main.game_id = games.id
        WHERE main.game_id = {gamenum}
        ORDER BY main.score DESC;
    ''').fetchall()
    conn.close()

    if len(dbscores) > 0:
        page_title = dbscores[0]["game_id"]
    else:
        page_title = "TBD"


    ## TODO pass in color codes for background and text based on game selected.
    ##      also pass in link to image for game?
    ##
    ##      OR, pass in just game as the title, use as css class in html and customize colors in css
    return render_template(
    'leaderboard_base.html', 
    score_count = len(dbscores),
    title = page_title,
    scores = dbscores,
    count=2
    #game_title_name = gname
    )


#def new_score_highlight(date):
#    current_time = datetime.datetime.now().strftime("%m/%d/%Y")
#    if int(date[3:5]) > int(current_time[3:5]) and int(date[:2]) + 1 == int(current_time[:2]):
#        highlight = True
#    elif int(date[:2]) == int(current_time[:2]):
#        highlight = True
#    else:
#        highlight = False
#    print(highlight)
#    return highlight



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
        name = request.form['pname'].strip()        #score = int(request.form['score'])
        date = request.form['pgradyear']


        #if new_score_highlight(date):
        #    highlight = True
        #else:
        #    highlight = False


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
            error = f"Score saved for {name}"
        
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
