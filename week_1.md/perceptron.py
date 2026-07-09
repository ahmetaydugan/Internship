import numpy as np

class Perceptron:
    def __init__(self, learning_rate=0.01, n_iters=1000):
        self.lr = learning_rate
        self.n_iters = n_iters
        self.weights = None
        self.bias = None

    def _unit_step_func(self, x):
        return np.where(x >= 0, 1, 0)

    def fit(self, X, y):
        n_samples, n_features = X.shape

        self.weights = np.zeros(n_features)
        self.bias = 0

        y_ = np.array([1 if i > 0 else 0 for i in y])

        for _ in range(self.n_iters):
            for idx, x_i in enumerate(X):
                
                linear_output = np.dot(x_i, self.weights) + self.bias
                
                y_predicted = self._unit_step_func(linear_output)

                update = self.lr * (y_[idx] - y_predicted)
                
                self.weights += update * x_i
                self.bias += update

    def predict(self, X):
        linear_output = np.dot(X, self.weights) + self.bias
        y_predicted = self._unit_step_func(linear_output)
        return y_predicted

        
X_veri = np.array([
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
])

y_and = np.array([0, 0, 0, 1])

model_and = Perceptron(learning_rate=0.1, n_iters=10)

model_and.fit(X_veri, y_and)

tahminler_and = model_and.predict(X_veri)

print("--- AND Kapısı Sonuçları ---")
print("Gerçek Değerler :", y_and)
print("Modelin Tahmini :", tahminler_and)

y_or = np.array([0, 1, 1, 1])

model_or = Perceptron(learning_rate=0.1, n_iters=10)

model_or.fit(X_veri, y_or)

tahminler_or = model_or.predict(X_veri)

print("\n--- OR Kapısı Sonuçları ---")
print("Gerçek Değerler :", y_or)
print("Modelin Tahmini :", tahminler_or)        

y_xor = np.array([0, 1, 1, 0])

model_xor = Perceptron(learning_rate=0.1, n_iters=100)
model_xor.fit(X_veri, y_xor)

tahminler_xor = model_xor.predict(X_veri)

print("--- XOR Kapısı Sonuçları ---")
print("Gerçek Değerler :", y_xor)
print("Modelin Tahmini :", tahminler_xor)
