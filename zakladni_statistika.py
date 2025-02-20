import pandas as pd

# Načtení dat
file_path = r"C:\Users\ranoc\OneDrive\Desktop\projekt počasí\pocasi_data.csv"
data = pd.read_csv(file_path)

# Zobrazení prvních několika záznamů
print("Ukázka dat:")
print(data.head())

# Základní statistiky
print("\nZákladní statistiky:")
print(data.describe())

# Přidání sloupce s částí dne
def get_period_of_day(hour):
    if 6 <= hour < 12:
        return "Morning"
    elif 12 <= hour < 18:
        return "Afternoon"
    elif 18 <= hour < 24:
        return "Evening"
    else:
        return "Night"

data['period_of_day'] = pd.to_datetime(data['timestamp']).dt.hour.apply(get_period_of_day)

# Zobrazení rozdělení na části dne
print("\nRozdělení na části dne:")
print(data['period_of_day'].value_counts())

# Uložení upravených dat
data.to_csv(r"C:\Users\ranoc\OneDrive\Desktop\projekt počasí\pocasi_data_prepared.csv", index=False)
print("\nUpravená data byla uložena do souboru 'pocasi_data_prepared.csv'.")

# Vyber pouze číselné sloupce pro průměrování
grouped = data.groupby('period_of_day')[['temp', 'feels_like', 'wind_speed']].mean()
print("\nPrůměrné hodnoty podle části dne:")
print(grouped)


# Četnost typů počasí
weather_counts = data['weather_desc'].value_counts()
print("\nČetnost typů počasí:")
print(weather_counts)

import matplotlib.pyplot as plt

# Převod timestamp na datetime
data['timestamp'] = pd.to_datetime(data['timestamp'])

# Časová osa teplot
plt.figure(figsize=(10, 6))
plt.plot(data['timestamp'], data['temp'], label='Teplota')
plt.xlabel('Čas')
plt.ylabel('Teplota (°C)')
plt.title('Vývoj teploty během dne')
plt.legend()
plt.grid()
plt.show()
