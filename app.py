from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

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
            error = "Non-Number"
            score = 0
        

        try:
            month = int(date[:2])
            day = int(date[3:5])
            year = int(date[6:])
        except ValueError:
            error = "Invalid date"
            date = 0

        try:
            if month > 12 or month < 00:
                error = "Invalid date"
            elif day >= 31 or day < 0:
                error = "Invalid date"
            elif year < 2000:
                error = "Invalid date"
        except UnboundLocalError:
            error = "Invalid date"

        if not (name.isalpha()) or len(name) > 20:
            error = "Invalid name"
        
        if score > max_scores.get(game) or score < 0:
            error = "Bad Score"
        
        form_values = apply_form_values(name, game, score, date)
        # only append score if no errors
        if error == None:
            scores.append(form_values)
        
    return render_template('forms.html', name=name, error=error, form_values=apply_form_values(name, game, score, date), options=games)

def apply_form_values(name='', game='', score='', date=''):

    return {'player': name, 'game': game, 'score': score, 'date': date}

@app.route('/leaderboard_base')
def lead_base():
    page_title = "Game"
    return render_template(
    'leaderboard_base.html', 
    score_count = len(scores),
    title = page_title,
    scores = scores
    )


if __name__ == "__main__":
    app.run(debug=True)
