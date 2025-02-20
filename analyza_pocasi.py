import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

file_path = r"C:\Users\ranoc\OneDrive\Desktop\projekt počasí\pocasi_data.csv"
data = pd.read_csv(file_path)

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

plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred, color='blue', label='Predikce', alpha=0.7)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', label='Ideální predikce')
plt.title('Skutečné vs. predikované hodnoty teplot')
plt.xlabel('Skutečné teploty (°C)')
plt.ylabel('Predikované teploty (°C)')
plt.legend()
plt.grid()
plt.show()
