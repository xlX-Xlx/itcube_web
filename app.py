from flask import Flask, render_template, request, g, redirect, flash
import sqlite3
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

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

def calculate_similarity(expected_answer, user_answer):
    vectorizer = CountVectorizer().fit_transform([expected_answer, user_answer])
    similarity_matrix = cosine_similarity(vectorizer)
    return similarity_matrix[0, 1]

def create_table():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS user_answers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    answer1 TEXT,
                    answer2 TEXT,
                    answer3 TEXT,
                    answer4 TEXT,
                    answer5 TEXT,
                    answer6 TEXT,
                    answer7 TEXT,
                    answer8 TEXT,
                    answer9 TEXT,
                    answer10 TEXT,
                    answer11 TEXT,
                    answer12 TEXT
                 )''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/submit', methods=['POST'])
def submit():
    answers = {
        'answer1': request.form.get('answer1', ''),
        'answer2': request.form.get('answer2', ''),
        'answer3': request.form.getlist('answer3'),  
        'answer4': request.form.get('answer4', ''),
        'answer5': request.form.get('answer5', ''),
        'answer6': request.form.get('answer6', ''),
        'answer7': request.form.get('answer7', ''),
        'answer8': request.form.get('answer8', ''),
        'answer9': request.form.get('answer9', ''),
        'answer10': request.form.get('answer10', ''),
        'answer11': request.form.get('answer11', ''),
        'answer12': request.form.get('answer12', '')
    }

    if '' in answers.values():
        flash('Вы ответили не на все вопросы.')
        return redirect('/test')

    save_answers(answers)
    results = check_answers(answers)
    return render_template('results.html', results=results)

def save_answers(answers):
    db = get_db()
    c = db.cursor()
    c.execute('''INSERT INTO user_answers (answer1, answer2, answer3, answer4, answer5, answer6, answer7, answer8, answer9, answer10, answer11, answer12)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (answers['answer1'], answers['answer2'], ', '.join(answers['answer3']), answers['answer4'],
                 ', '.join(answers['answer5']), answers['answer6'], answers['answer7'], answers['answer8'],
                 ', '.join(answers['answer9']), ', '.join(answers['answer10']), answers['answer11'], answers['answer12']))
    db.commit()
    
def check_answers(answers):
    correct_answers = {
        'answer1': '1941',
        'answer2': 'цифровом виде',
        'answer3': ['бизнес', 'образование', 'медицина', 'ритейл', 'искусство и развлечения', 'производство', 'общепит'],
        'answer4': "это технология, которая позволяет объединять сенсоры, гаджеты, бытовую технику и даже автомобили в единую сеть при помощи беспроводной связи", 
        'answer5': 'iphone',
        'answer6': '1991',
        'answer7': "под «искусственным интеллектом» подразумевают любые алгоритмы, которые решают какие-либо задачи независимо от человека: производят сложные вычисления, распознают изображения и речь, собирают и обрабатывают массивы данных.",
        'answer8': 'XIX',
        'answer9': 'blockchain1',
        'answer10': 'cryptocurrency1',
        'answer11': '1980',
        'answer12': "Аббревиатура AR может означать 'дополненную реальность' (Augmented Reality), технологию добавления виртуальных объектов в реальное окружение."
    }

    results = {}
    for question, user_answer in answers.items():
        if question == 'answer4':
            similarity_score = calculate_similarity(correct_answers['answer4'], user_answer)
            results[question] = similarity_score > 0.7
        elif question == 'answer7':
            similarity_score = calculate_similarity(correct_answers['answer7'], user_answer)
            results[question] = similarity_score > 0.7
        elif question == 'answer12':
            similarity_score = calculate_similarity(correct_answers['answer12'], user_answer)
            results[question] = similarity_score > 0.7
        elif correct_answers[question] is None:
            results[question] = None
        elif isinstance(correct_answers[question], list):
            user_answer_list = request.form.getlist(question)
            results[question] = all(answer in user_answer_list for answer in correct_answers[question])
        else:
            results[question] = user_answer == correct_answers[question]

    return results



    return results


if __name__ == '__main__':
    create_table()
    app.run(debug=True)