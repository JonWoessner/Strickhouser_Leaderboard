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

def get_score(entry):
    return entry['score']

sorted_scores = sorted(scores, key=get_score, reverse = True)
print(sorted_scores)


try:
    #Code that might not work?
    result = int("banana")
except ValueError:
    print("Oops, that's not a number")
else:
    #Executes only if Try was successful
    pass
finally:
    #Executes no matter if try was successful
    pass