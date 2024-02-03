import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

# Создание базы данных и таблицы
conn = sqlite3.connect('answers.db')
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
                answer11 TEXT
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
    if request.method == 'POST':
        answers = [request.form['answer{}'.format(i)] for i in range(1, 12)]
        save_answers(answers)
        return 'Спасибо за участие в тесте!'

def save_answers(answers):
    conn = sqlite3.connect('answers.db')
    c = conn.cursor()
    c.execute('''INSERT INTO user_answers (answer1, answer2, answer3, answer4, answer5, answer6, answer7, answer8, answer9, answer10, answer11)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', answers)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    app.run(debug=True)
