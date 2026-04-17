from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    page_title = "Title of thou Home"
    return render_template('index.html', title=page_title)


@app.route('/leaderboard_base')
def lead_base():
    page_title = "Game"
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
    noscores = []
    return render_template(
    'leaderboard_base.html', 
    score_count = len(scores),
    title = page_title,
    scores = scores
    )

if __name__ == "__main__":
    app.run(debug=True)
