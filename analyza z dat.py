import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score

file_path = r"C:\Users\ranoc\OneDrive\Desktop\projekt počasí\pocasi_data.csv"
data = pd.read_csv(file_path)

print("Ukázka nasbíraných dat:")
print(data.head())

print(f"\nPočet nasbíraných záznamů: {len(data)}")

avg_temp = data['temp'].mean()
min_temp = data['temp'].min()
max_temp = data['temp'].max()

print(f"\nPrůměrná teplota: {avg_temp:.2f}°C")
print(f"Minimální teplota: {min_temp}°C")
print(f"Maximální teplota: {max_temp}°C")

weather_counts = data['weather_desc'].value_counts()
print("\nČetnost typů počasí:")
print(weather_counts)

min_temp_record = data.loc[data['temp'].idxmin()]
max_temp_record = data.loc[data['temp'].idxmax()]

print(f"\nNejnižší teplota byla naměřena v čase: {min_temp_record['timestamp']} a byla {min_temp_record['temp']}°C")
print(f"Nejvyšší teplota byla naměřena v čase: {max_temp_record['timestamp']} a byla {max_temp_record['temp']}°C")

label_encoder = LabelEncoder()
data['weather_encoded'] = label_encoder.fit_transform(data['weather_desc'])

X = data[['wind_speed', 'weather_encoded']]
y = data['temp']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Střední kvadratická chyba (MSE): {mse:.2f}")
print(f"R2 skóre: {r2:.2f}")

new_data = pd.DataFrame({'wind_speed': [3.5], 'weather_encoded': [label_encoder.transform(['overcast clouds'])[0]]})
predicted_temp = model.predict(new_data)
print(f"Předpovězená teplota: {predicted_temp[0]:.2f}°C")
