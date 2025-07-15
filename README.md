# Flask Project

このリポジトリは Flask を利用した Web アプリケーションの開発を想定した雛形です。MIT ライセンスで公開されています。

## 前提条件
- Python 3.10 以上がインストールされていること

## セットアップ
1. リポジトリをクローンします。
2. 仮想環境を作成します。
   ```bash
   python3 -m venv venv
   ```
3. 仮想環境を有効化します。
   ```bash
   source venv/bin/activate  # Windows の場合は venv\Scripts\activate
   ```
4. 依存パッケージをインストールします。
   ```bash
   pip install flask
   ```

## 使い方
1. `app.py` などを作成して Flask アプリケーションを実装します。
2. 以下のコマンドで開発サーバを起動します。
   ```bash
   FLASK_APP=app.py flask run
   ```

## ディレクトリ構成
- `LICENSE` - MIT ライセンス文書
- （必要に応じて作成してください）`app.py`, `requirements.txt`, `templates/`, `static/` など

## テスト
現時点ではテストコードは含まれていませんが、`pytest` を利用して追加することができます。

## ライセンス
このプロジェクトは MIT License の下で公開されています。詳細は LICENSE ファイルを参照してください。
