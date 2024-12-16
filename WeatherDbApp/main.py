import datetime
import flet as ft
import requests
import sqlite3

# 気象庁のAPIのエンドポイント
AREA_CODE_URL = "https://www.jma.go.jp/bosai/common/const/area.json"
FORECAST_URL = "https://www.jma.go.jp/bosai/forecast/data/forecast/{}.json"


def get_area_list():
    """地域の一覧を取得する関数"""
    try:
        response = requests.get(AREA_CODE_URL)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as err:
        print(f"エリア情報の取得中にエラーが発生しました: {err}")
        return None


def get_weather_forecast(area_code):
    """指定したエリアコードの天気予報を取得する関数"""
    try:
        url = FORECAST_URL.format(area_code)
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as err:
        print(f"天気予報の取得中にエラーが発生しました: {err}")
        return None


def create_database():
    conn = sqlite3.connect('weather.db')
    cursor = conn.cursor()
    # 天気情報を保存するテーブルを作成します
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            area_code TEXT,
            date TEXT,
            weather TEXT,
            wind TEXT,
            max_temp TEXT,
            min_temp TEXT
        )
    ''')
    conn.commit()
    conn.close()


def save_weather_to_db(area_code, weather_list):
    conn = sqlite3.connect('weather.db')
    cursor = conn.cursor()
    # 既存の同じエリアコードのデータを削除
    cursor.execute('DELETE FROM weather WHERE area_code = ?', (area_code,))
    # 天気情報を挿入
    for weather_data in weather_list:
        cursor.execute('''
            INSERT INTO weather (area_code, date, weather, wind, max_temp, min_temp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            area_code,
            weather_data['date'],
            weather_data['weather'],
            weather_data['wind'],
            weather_data['max_temp'],
            weather_data['min_temp']
        ))
    conn.commit()
    conn.close()


def load_weather_from_db(area_code):
    conn = sqlite3.connect('weather.db')
    cursor = conn.cursor()
    cursor.execute('SELECT date, weather, wind, max_temp, min_temp FROM weather WHERE area_code = ?', (area_code,))
    rows = cursor.fetchall()
    conn.close()

    weather_container.controls.clear()

    if rows:
        for row in rows:
            date_str, weather, wind, max_temp, min_temp = row
            # 日付ごとのカードを作成します
            daily_card = ft.Card(
                content=ft.Container(
                    ft.Column(
                        [
                            ft.Text(f"日付: {date_str}", weight="bold"),
                            ft.Text(f"天気: {weather}"),
                            ft.Text(f"風: {wind}"),
                            ft.Text(f"最高気温: {max_temp} ℃"),
                            ft.Text(f"最低気温: {min_temp} ℃"),
                        ],
                        spacing=5,
                    ),
                    padding=10,
                ),
                elevation=2,
            )
            weather_container.controls.append(daily_card)
    else:
        weather_container.controls.append(ft.Text("データベースに天気情報がありません。"))


def main(page: ft.Page):
    global weather_container
    page.title = "天気予報アプリ"
    page.padding = 10
    page.spacing = 20

    create_database()

    # 天気情報表示エリア
    weather_container = ft.Column(
        controls=[],
        spacing=10,
        width=400,
        height=400,
        scroll="auto",
    )

    def display_weather(area_code):
        """天気情報を表示する関数"""
        weather_data = get_weather_forecast(area_code)
        if weather_data and len(weather_data) > 0:
            try:
                weather_list = []
                # 日付情報を取得
                dates = weather_data[0]["timeSeries"][0]["timeDefines"]
                # 天気情報を取得
                weather_info = weather_data[0]["timeSeries"][0]["areas"][0]
                weathers = weather_info.get("weathers", [])
                winds = weather_info.get("winds", [])

                # 温度情報を取得
                temp_info_section = next((ts for ts in weather_data[0]["timeSeries"] if 'temps' in ts["areas"][0]), None)
                max_temps = min_temps = ["データ未取得"] * len(dates)
                if temp_info_section:
                    temps = temp_info_section["areas"][0]["temps"]
                    max_temps = temps[1::2]
                    min_temps = temps[0::2]

                # 天気情報をリストとしてまとめる
                for i in range(min(len(dates), 4)):
                    date_str = datetime.datetime.fromisoformat(dates[i]).strftime('%Y-%m-%d')
                    weather = weathers[i] if i < len(weathers) else "N/A"
                    wind = winds[i] if i < len(winds) else "N/A"
                    max_temp = max_temps[i] if i < len(max_temps) else "N/A"
                    min_temp = min_temps[i] if i < len(min_temps) else "N/A"

                    weather_list.append({
                        'date': date_str,
                        'weather': weather,
                        'wind': wind,
                        'max_temp': max_temp,
                        'min_temp': min_temp
                    })

                # データベースに保存
                save_weather_to_db(area_code, weather_list)

                # データベースから読み込み表示
                load_weather_from_db(area_code)

            except (IndexError, KeyError, TypeError) as e:
                weather_container.controls.clear()
                weather_container.controls.append(ft.Text(f"天気情報の解析中にエラーが発生しました: {e}"))
        else:
            weather_container.controls.clear()
            weather_container.controls.append(ft.Text("天気情報が取得できませんでした。"))

        page.update()

    def on_area_change(e):
        """地域が選択されたときの処理"""
        area_code = e.control.value
        display_weather(area_code)

    # 地域リストの取得
    area_list = get_area_list()
    if not area_list:
        page.add(ft.Text("地域情報が取得できませんでした。"))
        return

    # 地域オプションの作成
    area_options = []
    offices = area_list.get("offices", {})
    for code, info in offices.items():
        area_options.append(ft.dropdown.Option(key=str(code), text=info["name"]))

    # 地域選択用ドロップダウンリスト
    area_dropdown = ft.Dropdown(
        options=area_options,
        label="地域を選択",
        on_change=on_area_change,
    )

    # ページにコンポーネントを追加
    page.add(
        ft.Row(
            [
                ft.Column([area_dropdown], expand=False),
                weather_container,
            ],
            expand=True,
        )
    )

if __name__ == "__main__":
    ft.app(target=main)