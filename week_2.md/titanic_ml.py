import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

# 1. Veri setini yükleme
df = pd.read_csv("train_and_test2.csv")

# 2. Gereksiz sütunları silme
df = df.loc[:, ~df.columns.str.contains('zero')]

# 3. Eksikleri doldurma
df['Embarked'] = df['Embarked'].fillna(df['Embarked'].mode()[0])

# 4. 'Sex' sütununu sayısal değerlere çevirme
if df['Sex'].dtype == 'object':
    df['Sex'] = df['Sex'].map({'male': 0, 'female': 1})

# 5. Özellikleri ve hedef değişkeni ayırma
X = df.drop('2urvived', axis=1)
y = df['2urvived']

# 6. Veri setini eğitim ve test olarak ayırma
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 7. Modeli oluşturma
model = DecisionTreeClassifier(random_state=42)

# 8. Modeli eğitme
model.fit(X_train, y_train)

# 9. Tahmin yaptırma
y_pred = model.predict(X_test)

# 10. Başarıyı ölçme
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)