import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import time

# --- 1. Model Mimarisinin Tanımlanması ---
class SimpleMLP(nn.Module):
    def __init__(self, input_size, hidden1_size, hidden2_size, output_size):
        super(SimpleMLP, self).__init__()
        
        # Tam Bağlı (Linear) Katmanlar
        self.fc1 = nn.Linear(input_size, hidden1_size)
        self.fc2 = nn.Linear(hidden1_size, hidden2_size)
        self.fc3 = nn.Linear(hidden2_size, output_size)
        
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.fc3(x) # Çıktı katmanında aktivasyon kullanılmaz
        return x

# --- 2. MNIST Veri Setinin Hazırlanması ---
# Veriyi tensöre çevirip -1 ile 1 arasına normalize ediyoruz
transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))])

# Eğitim veri setini indiriyoruz
train_dataset = datasets.MNIST(root='./data', train=True, transform=transform, download=True)
train_loader = DataLoader(dataset=train_dataset, batch_size=64, shuffle=True)

# --- 3. Eğitim ve Süre Ölçüm Fonksiyonu ---
def train_model(device_name):
    # Cihazı belirliyoruz ("cpu" veya "cuda")
    device = torch.device(device_name)
    print(f"\n>>> Eğitim Başlıyor: [{device_name.upper()}] <<<")
    
    # Model ve parametrelerin tanımlanması ve seçilen cihaza (RAM veya VRAM) taşınması
    model = SimpleMLP(784, 128, 64, 10).to(device) 
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    epochs = 5

    # Kronometreyi başlatıyoruz
    start_time = time.time()

    for epoch in range(epochs):
        running_loss = 0.0
        for images, labels in train_loader:
            # Görselleri düzleştiriyoruz (28x28 -> 784) ve işlem yapılacak cihaza taşıyoruz
            images = images.view(images.size(0), -1).to(device)
            labels = labels.to(device)

            # İleri yayılım, kayıp hesaplama ve geri yayılım
            outputs = model(images)
            loss = criterion(outputs, labels)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            running_loss += loss.item()

    # Kronometreyi durduruyoruz
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"[{device_name.upper()}] Eğitimi Tamamlandı! Toplam Süre: {total_time:.2f} saniye")
    return total_time

# --- 4. Karşılaştırmalı Deneyin Çalıştırılması ---
if __name__ == "__main__":
    print("Donanım Performans Deneyi Başlıyor...")
    
    # 1. CPU Eğitimi
    cpu_time = train_model("cpu")

    # 2. GPU (CUDA) Eğitimi (Sadece CUDA destekli bir makinede/Colab'de çalışır)
    if torch.cuda.is_available():
        gpu_time = train_model("cuda")
        
        # --- 5. Sonuç Özet Grafiği ---
        print("\n" + "="*40)
        print(f" CPU Eğitim Süresi : {cpu_time:.2f} s")
        print(f" GPU Eğitim Süresi : {gpu_time:.2f} s")
        speedup = cpu_time / gpu_time
        print(f" Hız Farkı         : GPU, CPU'dan yaklaşık {speedup:.1f} kat daha hızlı!")
        print("="*40)
    else:
        print("\nSistemde aktif bir GPU bulunamadı. Sadece CPU testi tamamlandı.")
