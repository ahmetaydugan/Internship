from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

# 1. İris veri seti yükleme
iris = load_iris()
X = iris.data    # Çiçeklerin özellikleri (taç yaprak uzunluğu vb.)
y = iris.target  # Çiçek türleri 

# 2. Veriyi eğitim ve test olarak ayırma (%80 eğitim, %20 test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Decision Tree modelini oluşturma
clf = DecisionTreeClassifier(random_state=42)

# 4. Modeli eğitim verisiyle eğitme 
clf.fit(X_train, y_train)

# 5. Test verisi üzerinde tahmin yapma
y_pred = clf.predict(X_test)

# 6. Modelin doğruluğunu (accuracy) hesaplama
dogruluk = accuracy_score(y_test, y_pred)
print(f"Model Doğruluğu: {dogruluk * 100:.2f}%")