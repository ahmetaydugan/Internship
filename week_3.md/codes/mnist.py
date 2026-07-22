# 1. Gerekli kütüphaneleri çağırıyoruz
from tensorflow.keras.datasets import mnist
import matplotlib.pyplot as plt

# 2. Veriyi indirip eğitim ve test kümelerine ayırıyoruz
print("MNIST verisi indiriliyor...")
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# 3. Veri setinin boyutlarını (shape) ve yapısını raporluyoruz
print("\n--- Veri Seti Boyutları ---")
print("Eğitim görselleri (x_train):", x_train.shape)
print("Eğitim etiketleri (y_train):", y_train.shape)
print("Test görselleri (x_test):", x_test.shape)
print("Test etiketleri (y_test):", y_test.shape)

# 4. İlk 5 görseli Matplotlib ile ekrana çizdiriyoruz
print("\nİlk 5 örnek görsel ekrana basılıyor...")
plt.figure(figsize=(10, 2))

for i in range(5):
    plt.subplot(1, 5, i + 1)
    plt.imshow(x_train[i], cmap='gray')
    plt.title(f"Etiket: {y_train[i]}")
    plt.axis('off')

# Çizimi gösteriyoruz
plt.show()
