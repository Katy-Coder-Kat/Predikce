import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

file_path = 'pocasi_data_prepared.csv'
data = pd.read_csv(file_path)

label_encoder = LabelEncoder()
data['weather_desc_encoded'] = label_encoder.fit_transform(data['weather_desc'])

period_mapping = {'Morning': 0, 'Afternoon': 1, 'Evening': 2, 'Night': 3}
data['period_of_day'] = data['period_of_day'].map(period_mapping)

X = data[['temp', 'feels_like', 'wind_speed', 'period_of_day']]
y = data['weather_desc_encoded']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

conf_matrix = confusion_matrix(y_test, y_pred)

actual_vs_pred = pd.DataFrame({
    'Actual': label_encoder.inverse_transform(y_test),
    'Predicted': label_encoder.inverse_transform(y_pred)
})

comparison = actual_vs_pred.groupby(['Actual', 'Predicted']).size().reset_index(name='Count')
comparison_pivot = comparison.pivot(index='Actual', columns='Predicted', values='Count').fillna(0)

plt.figure(figsize=(12, 8))
comparison_pivot.plot(kind='bar', stacked=True, figsize=(12, 8))
plt.title('Porovnání skutečných a predikovaných hodnot')
plt.xlabel('Skutečné hodnoty')
plt.ylabel('Počet')
plt.xticks(rotation=45)
plt.legend(title='Predikované hodnoty')
plt.show()

plt.figure(figsize=(10, 8))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='coolwarm', xticklabels=label_encoder.classes_, yticklabels=label_encoder.classes_)
plt.title('Heatmapa distribuce chyb modelu')
plt.xlabel('Predikované hodnoty')
plt.ylabel('Skutečné hodnoty')
plt.show()

part_of_day_weather = data.groupby(['period_of_day', 'weather_desc']).size().reset_index(name='Count')
part_of_day_weather['period_of_day'] = part_of_day_weather['period_of_day'].map({0: 'Ráno', 1: 'Odpoledne', 2: 'Večer', 3: 'Noc'})

fig = px.bar(part_of_day_weather, x='period_of_day', y='Count', color='weather_desc',
             title='Rozdělení počasí podle části dne', labels={'period_of_day': 'Část dne', 'Count': 'Počet'})
fig.show()
