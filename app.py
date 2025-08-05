from flask import Flask, request, render_template, redirect, url_for, session
import os
import random

app = Flask(__name__)
app.secret_key = 'секрет_будь_який'
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Роут головної сторінки
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Зберігаємо файл
        file = request.files['file']
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            session['filename'] = file.filename

        # Ціна
        price = request.form['price']
        session['price'] = price

        # Генерація математичного прикладу
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        op = random.choice(['+', '-', '*', '/'])

        # Вираховуємо правильну відповідь
        if op == '+':
            answer = num1 + num2
        elif op == '-':
            answer = num1 - num2
        elif op == '*':
            answer = num1 * num2
        else:
            answer = round(num1 / num2, 2)

        session['correct_answer'] = answer
        session['num1'] = num1
        session['num2'] = num2
        session['op'] = op

        return render_template('index.html', num1=num1, num2=num2, op=op, stage='math')

    return render_template('index.html', stage='upload')

# Перевірка математичної відповіді
@app.route('/check', methods=['POST'])
def check():
    user_answer = request.form['answer']
    try:
        if float(user_answer) == float(session['correct_answer']):
            return redirect(url_for('success'))
        else:
            return "Неправильна відповідь. <a href='/'>Спробуй знову</a>"
    except ValueError:
        return "Помилка. Введи число. <a href='/'>Спробуй знову</a>"


# Перенаправлення на Payeer
@app.route('/success')
def success():
    price = session.get('price')
    payeer_id = 'P1131106201'  # твій ID гаманця
    desc = 'Купівля файлу'
    payeer_link = f"https://payeer.com/ru/account/send/?ps={payeer_id}&sum={price}&cur=USD&desc={desc}"
    return render_template('success.html', link=payeer_link)

if __name__ == '__main__':
    app.run(debug=True)
