from flask import Flask
from flask import render_template,g

import weather
import recipe
import memo

app = Flask(__name__)

# メモページのルート
@app.route('/')
def memo_top():
    return memo.memo_top()

# リクエストが終わったらデータベース接続を閉じる
@app.teardown_appcontext
def close_db(error):
    memo.close_db(error)

# メモを追加するルート
@app.route('/add', methods=['POST'])
def add_memo():
    return memo.add_memo()

# メモを削除するルート
@app.route('/delete/<int:memo_id>', methods=['POST'])
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