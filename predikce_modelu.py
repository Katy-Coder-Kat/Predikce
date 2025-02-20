import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import seaborn as sns
import matplotlib.pyplot as plt

file_path = 'pocasi_data_prepared.csv'
data = pd.read_csv(file_path)

data['period_of_day'] = data['period_of_day'].astype('category').cat.codes
label_encoder = LabelEncoder()
data['weather_desc_encoded'] = label_encoder.fit_transfor(data['weather_desc'])

X = data[['temp', 'feels_like', 'wind_speed', 'period_of_day']]
y = data['weather_desc_encoded']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print(f"Přesnost modelu: {accuracy * 100:.2f}%\n")
print("Matice záměn:")
conf_matrix = confusion_matrix(y_test, y_pred)
print(conf_matrix)

plt.figure(figsize=(10, 8))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues',
            xticklabels=label_encoder.classes_, yticklabels=label_encoder.classes_)
plt.xlabel('Predikce')
plt.ylabel('Skutečné hodnoty')
plt.title('Matice záměn')
plt.show()

print("\nReport klasifikace:")
unique_labels = sorted(set(y_test) | set(y_pred))
target_names = [label_encoder.inverse_transform([label])[0] for label in unique_labels]
print(classification_report(y_test, y_pred, target_names=target_names))
