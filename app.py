from flask import Flask, render_template, request

app = Flask(__name__)

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
    page_title = "Title of thou Home"
    return render_template('index.html', title=page_title)




@app.route('/leaderboard_base')
def lead_base():
    page_title = "Game"
    sorted_scores = sorted(scores, key= lambda entry: entry == {'score'}, reverse = True)
    
    return render_template(
    'leaderboard_base.html', 
    score_count = len(sorted_scores),
    title = page_title,
    scores = sorted_scores
    )




@app.route('/newentry', methods=['GET', 'POST'])
def submit():
    game = None
    name = None
    score = None
    date = None

    error = None

    form_values = {'player': '','game': '','score': '','date': ''}


    if request.method == 'POST':
        game = request.form['gameid'].strip().upper()
        name = request.form['pname'].strip().capitalize()
        #score = int(request.form['score'])
        date = request.form['pgradyear']

        
        
        if not name or not game:
            error = 'Blank Field'
            print('Are you sure there is anything there')
        
        try:
            score = int(request.form['score'])
        except:
            error = "What kinda number is that"
            print('Are you sure thats a number')
            score=0
        

        try:
            request.form['gameid'].strip().upper() == valid_game.keys()
        except:
            error = "Invalid Game ID"
            print('Are you sure thats a real game')
            #print('Input', request.form['gameid'].upper().strip())
            #print('Pair', valid_game.keys())
            game=''
            
            if request.form['gameid'].strip().upper() == valid_game.keys('PACMAN'):
                pass



        form_values = {'player': name,'game': game,'score': score,'date': date}


        if error == None:
            scores.append({'player': name, 'score': score, 'year': date})
        
    return render_template(
        'form.html', 
        game=game, 
        name=name, 
        score=score, 
        date=date, 
        error=error, 
        form_values=form_values
        )




if __name__ == "__main__":
    app.run(debug=True)
