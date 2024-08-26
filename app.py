from flask import Flask
from flask import render_template,g
import sqlite3
import psycopg2
import os

import weather
import recipe

app = Flask(__name__)

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