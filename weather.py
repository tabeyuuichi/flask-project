from flask import Flask, render_template, request
import sqlite3
import requests

import os

DATABASE_PATH = os.getenv('DATABASE_PATH')

app = Flask(__name__)

# データベースから地域リストを取得する関数
def fetch_regions_from_db(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT region FROM weather_regions')
    regions = cursor.fetchall()
    conn.close()
    return [region[0] for region in regions]

# データベースからエリアリストを取得する関数
def fetch_areas_from_db(db_name, region_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT area FROM weather_regions WHERE region = ?', (region_name,))
    areas = cursor.fetchall()
    conn.close()
    return [area[0] for area in areas]

# 指定された地域とエリアに対応するコードを取得する関数
def fetch_code_by_region_and_area(db_name, region_name, area_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT code FROM weather_regions 
        WHERE region = ? AND area = ?
    ''', (region_name, area_name))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def get_point(weather_data):
    area_names = []
    for series in weather_data[0]['timeSeries']:
        for area in series['areas']:
            area_name = area['area']['name']
            if 'weathers' in area:
                area_names.append(area_name)
    return area_names

# 天気ページのルート
@app.route('/weather', methods=['GET', 'POST'])
def weather_top():
    db_path = DATABASE_PATH
    regions = fetch_regions_from_db(db_path)
    areas = []
    weather_info = None
    points = None
    point_name = None
    
    if request.method == 'POST':
        region_name = request.form.get('region')
        area_name = request.form.get('area')
        point_name = request.form.get('point')
        if region_name:
            areas = fetch_areas_from_db(db_path, region_name)
        if area_name:
            code = fetch_code_by_region_and_area(db_path, region_name, area_name)
            weather_info = get_weather_info(code)
            if weather_info is not None:
                points = get_point(weather_info)

    return render_template('weather.html', regions=regions, areas=areas, points=points, point_name=point_name, weather_info=weather_info)

# 天気情報を取得する関数
def get_weather_info(code):
    weather_api_url = f'https://www.jma.go.jp/bosai/forecast/data/forecast/{code}.json'
    response = requests.get(weather_api_url)

    if response.status_code == 200:
        weather_data = response.json()
        return weather_data
    else:
        return None

if __name__ == '__main__':
    app.run(debug=True)
