from flask import Flask, render_template, request
import sqlite3
import requests
import json
import time
import pandas as pd
from pprint import pprint

import os
RECIPE_CATEGORYLIST_API_KEY = os.getenv('RECIPE_CATEGORYLIST_API_KEY')
RECIPE_CATEGORYRANKING_API_KEY = os.getenv('RECIPE_CATEGORYRANKING_API_KEY')

app = Flask(__name__)

def get_list_of_categories():
    #レシピカテゴリ一覧を取得する
    res = requests.get(RECIPE_CATEGORYLIST_API_KEY)

    json_data = json.loads(res.text)

    # mediumカテゴリの親カテゴリの辞書
    parent_dict = {}

    df = pd.DataFrame(columns=['category1','category2','category3','categoryId','categoryName'])

    # 大カテゴリ
    for category in json_data['result']['large']:
        new_row = pd.DataFrame([{'category1': category['categoryId'], 'category2': '', 'category3': '', 'categoryId': category['categoryId'], 'categoryName': category['categoryName']}])
        df = pd.concat([df, new_row], ignore_index=True)

    # 中カテゴリ
    for category in json_data['result']['medium']:
        new_row = pd.DataFrame([{'category1': category['parentCategoryId'], 'category2': category['categoryId'], 'category3': '', 'categoryId': str(category['parentCategoryId']) + "-" + str(category['categoryId']), 'categoryName': category['categoryName']}])
        df = pd.concat([df, new_row], ignore_index=True)
        parent_dict[str(category['categoryId'])] = category['parentCategoryId']

    # 小カテゴリ
    for category in json_data['result']['small']:
        new_row = pd.DataFrame([{'category1': parent_dict[category['parentCategoryId']], 'category2': category['parentCategoryId'], 'category3': category['categoryId'], 'categoryId': parent_dict[category['parentCategoryId']] + "-" + str(category['parentCategoryId']) + "-" + str(category['categoryId']), 'categoryName': category['categoryName']}])
        df = pd.concat([df, new_row], ignore_index=True)

    return df 

def get_recipe(df, target_category):
    # キーワードからカテゴリを抽出する
    df_keyword = df.query('categoryName.str.contains("{0}")'.format(target_category), engine='python')

    # 人気レシピを取得する
    df_recipe = pd.DataFrame(columns=['recipeId', 'recipeTitle', 'foodImageUrl', 'recipeMaterial', 'recipeCost', 'recipeIndication', 'categoryId', 'categoryName', 'recipeUrl', 'recipeDescription'])

    for index, row in df_keyword.iterrows():
        time.sleep(1) # 連続でアクセスすると先方のサーバに負荷がかかるので少し待つ

        url = RECIPE_CATEGORYRANKING_API_KEY + '&categoryId=' + row['categoryId']
        res = requests.get(url)

        json_data = json.loads(res.text)
        recipes = json_data['result']

        for recipe in recipes:
            new_row = pd.DataFrame([{
            'recipeId': recipe['recipeId'],
            'recipeTitle': recipe['recipeTitle'],
            'foodImageUrl': recipe['foodImageUrl'],
            'recipeMaterial': recipe['recipeMaterial'],
            'recipeCost': recipe['recipeCost'],
            'recipeIndication': recipe['recipeIndication'],
            'categoryId': row['categoryId'],
            'categoryName': row['categoryName'],
            'recipeUrl':recipe['recipeUrl'],
            'recipeDescription':recipe['recipeDescription']
            }])

            df_recipe = pd.concat([df_recipe, new_row], ignore_index=True)
    return df_recipe

# レシピページのルート
@app.route('/recipe', methods=['GET', 'POST'])
def recipe_top():
    df_recipe=None

    if request.method == 'POST':
        df = get_list_of_categories()
        input = request.form.get('recipe')
        df_recipe = get_recipe(df, input)

    return render_template('recipe.html', df_recipe=df_recipe)

if __name__ == '__main__':
    app.run(debug=True)