from flask import Flask
from flask import render_template,g
import sqlite3

import weather
import recipe

DATABASE="flaskmemo.db"

app = Flask(__name__)

# memo_list = [{'title':"test01",'body':'ぐり主任です。'}, {'title':"test02",'body':'ぐらです。'}]

@app.route('/')
def top():
    memo_list = get_db().execute("select id, title, body from memo").fetchall()
    return render_template('memo.html', memo_list=memo_list)

# 天気ページのルート
@app.route('/weather', methods=['GET', 'POST'])
def weather_():
    return weather.weather_top()

# レシピページのルート
@app.route('/recipe', methods=['GET', 'POST'])
def recipe_():
    return recipe.recipe_top()

#database
def connect_db():
    rv = sqlite3.connect(DATABASE)
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db 

if __name__ == "__main__":
    app.run(debug=True)