from flask import Flask, render_template, request, redirect, url_for, g
import psycopg2
import os

# 環境変数からデータベースURLを取得
MEMO_DATABASE_URL = os.getenv("DATABASE_URL")

app = Flask(__name__)

# データベースに接続する関数
def connect_db():
    return psycopg2.connect(MEMO_DATABASE_URL)

# リクエストごとにデータベース接続を取得する関数
def get_db():
    if not hasattr(g, 'postgres_db'):
        g.postgres_db = connect_db()
    return g.postgres_db

# リクエストが終わったらデータベース接続を閉じる
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'postgres_db'):
        g.postgres_db.close()

# トップページを表示するルート
@app.route('/')
def top():
    cur = get_db().cursor()
    cur.execute("SELECT id, title, body FROM memo")
    memo_list = cur.fetchall()
    cur.close()
    return render_template('memo.html', memo_list=memo_list)

# メモを追加するルート
@app.route('/add', methods=['POST'])
def add_memo():
    title = request.form['title']
    body = request.form['body']
    cur = get_db().cursor()
    cur.execute("INSERT INTO memo (title, body) VALUES (%s, %s)", (title, body))
    get_db().commit()
    cur.close()
    return redirect(url_for('top'))

# メモを削除するルート
@app.route('/delete/<int:memo_id>', methods=['POST'])
def delete_memo(memo_id):
    cur = get_db().cursor()
    cur.execute("DELETE FROM memo WHERE id = %s", (memo_id,))
    get_db().commit()
    cur.close()
    return redirect(url_for('top'))

# アプリケーションを実行
if __name__ == "__main__":
    app.run(debug=True)
