from flask import Flask
from flask import render_template,g
import sqlite3
import psycopg2
import os

import weather
import recipe
import memo

app = Flask(__name__)

# メモページのルート
@app.route('/')
def memo_():
    return memo.memo_top()

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