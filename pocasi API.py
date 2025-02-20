import requests
import csv
from datetime import datetime
import schedule
import time
import pandas as pd

def fetch_and_save_weather():
    url = "https://api.openweathermap.org/data/2.5/weather?q=Prague&appid=072dc4a34b5ffe5fce085884866c252b&units=metric"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        city = data['name']
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        weather_desc = data['weather'][0]['description']
        wind_speed = data['wind']['speed']
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        file_path = r"C:\Users\ranoc\OneDrive\Desktop\projekt počasí\pocasi_data.csv"
        with open(file_path, mode="a", newline="") as file:
            writer = csv.writer(file)
            if file.tell() == 0:
                writer.writerow(["timestamp", "city", "temp", "feels_like", "weather_desc", "wind_speed"])
            writer.writerow([timestamp, city, temp, feels_like, weather_desc, wind_speed])
        
        print(f"Data uložena: {timestamp} | Teplota: {temp}°C | Popis: {weather_desc}")

        data = pd.read_csv(file_path)
        print(f"Počet záznamů v souboru: {len(data)}")
    else:
        print(f"Chyba při načítání dat: {response.status_code}")

schedule.every(1).minutes.do(fetch_and_save_weather)

print("Automatický sběr dat je spuštěn (každou minutu).")

while True:
    schedule.run_pending()
    print(f"Plánovač běží v čase: {datetime.now().strftime('%H:%M:%S')}")
    time.sleep(1)
