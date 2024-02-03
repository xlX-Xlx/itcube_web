from flask import Flask, render_template, request, g
import sqlite3

app = Flask(__name__)

DATABASE = 'answers.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/submit', methods=['POST'])
def submit():
    answers = {
        'answer1': request.form['answer1'],
        'answer2': request.form['answer2'],
        'answer3': request.form.getlist('answer3'),
        'answer4': request.form['answer4'],
        'answer5': request.form.getlist('answer5'),
        'answer6': request.form['answer6'],
        'answer7': request.form['answer7'],
        'answer8': request.form['answer8'],
        'answer9': request.form['answer9'],
        'answer10': request.form['answer10'],
        'answer11': request.form['answer11']
    }

    save_answers(answers)

    # Проверка ответов
    results = check_answers(answers)

    return render_template('results.html', results=results)

def save_answers(answers):
    db = get_db()
    c = db.cursor()
    c.execute('''INSERT INTO user_answers (answer1, answer2, answer3, answer4, answer5, answer6, answer7, answer8, answer9, answer10, answer11)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (answers['answer1'], answers['answer2'], ', '.join(answers['answer3']), answers['answer4'],
                 ', '.join(answers['answer5']), answers['answer6'], answers['answer7'], answers['answer8'],
                 ', '.join(answers['answer9']), ', '.join(answers['answer10']), answers['answer11']))
    db.commit()

def check_answers(answers):
    # Здесь происходит проверка ответов
    correct_answers = {
        'answer1': '1941',
        'answer2': 'цифровом виде',
        'answer3': ['бизнес', 'образование', 'медицина', 'ритейл', 'искусство и развлечения', 'производство', 'общепит'],
        'answer4': None,  # Не проверяем
        'answer5': ['iphone'],
        'answer6': '1991',
        'answer7': None,  # Не проверяем
        'answer8': 'XIX',
        'answer9': 'blockchain1',
        'answer10': 'cryptocurrency1',
        'answer11': '1980'
    }

    results = {}
    for question, user_answer in answers.items():
        if question == 'answer4' or question == 'answer7':
            results[question] = user_answer  # Просто сохраняем ответ пользователя
        elif correct_answers[question] is None:  # Пропускаем вопросы, не требующие проверки
            results[question] = None
        elif isinstance(correct_answers[question], list):
            # Проверяем, что все элементы из correct_answers[question] есть в user_answer
            results[question] = all(answer in user_answer for answer in correct_answers[question])
        else:
            results[question] = user_answer == correct_answers[question]

    return results


if __name__ == '__main__':
    app.run(debug=True)
