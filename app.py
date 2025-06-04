from flask import Flask, render_template, g, session, redirect, url_for, request
from functools import wraps
import os

import weather
import recipe
import memo


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return view(*args, **kwargs)

    return wrapped_view

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "changeme")

# ログインページ
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if (
            username == os.getenv("APP_USERNAME")
            and password == os.getenv("APP_PASSWORD")
        ):
            session['logged_in'] = True
            return redirect(url_for('memo_top'))
        return render_template('login.html', error='Invalid credentials')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))


# メモページのルート
@app.route('/')
@login_required
def memo_top():
    return memo.memo_top()

# リクエストが終わったらデータベース接続を閉じる
@app.teardown_appcontext
def close_db(error):
    memo.close_db(error)

# メモを追加するルート
@app.route('/add', methods=['POST'])
@login_required
def add_memo():
    return memo.add_memo()

# メモを削除するルート
@app.route('/delete/<int:memo_id>', methods=['POST'])
@login_required
def delete_memo(memo_id):
    return memo.delete_memo(memo_id)

# 天気ページのルート
@app.route('/weather', methods=['GET', 'POST'])
def weather_():
    return weather.weather_top()

# レシピページのルート
@app.route('/recipe', methods=['GET', 'POST'])
def recipe_():
    return recipe.recipe_top()

if __name__ == "__main__":
    app.run(debug=True)