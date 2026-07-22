import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter

# --- 1. Model Mimarisinin Tanımlanması ---
class SimpleMLP(nn.Module):
    def __init__(self, input_size, hidden1_size, hidden2_size, output_size):
        super(SimpleMLP, self).__init__()
        
        # Tam Bağlı (Linear) Katmanlar
        self.fc1 = nn.Linear(input_size, hidden1_size)
        self.fc2 = nn.Linear(hidden1_size, hidden2_size)
        self.fc3 = nn.Linear(hidden2_size, output_size)
        
        # Aktivasyon fonksiyonu
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.fc3(x) # Çıktı katmanında aktivasyon kullanmıyoruz
        return x

# --- 2. Modelin Başlatılması ve Test Edilmesi ---
input_dim = 784
hidden_dim1 = 128
hidden_dim2 = 64
output_dim = 10

model = SimpleMLP(input_dim, hidden_dim1, hidden_dim2, output_dim)
print("--- Model Mimarisi ---")
print(model)

total_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
print(f"\n--- Modeldeki Toplam Eğitilebilir Parametre Sayısı: {total_params} ---")

# (Opsiyonel) İleri Yayılım Testi
dummy_input = torch.randn(1, 784)
output = model(dummy_input)
print("\n--- Boyut Kontrolü (Dummy Veri) ---")
print("Girdi Boyutu:", dummy_input.shape)
print("Çıktı Boyutu:", output.shape)


# --- 3. MNIST Veri Setinin Hazırlanması ---
print("\n--- MNIST Veri Seti İndiriliyor ve Hazırlanıyor ---")
transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))])

# Eğitim veri setini indirip yüklüyoruz (İndirme işlemi ilk çalışmada biraz sürebilir)
train_dataset = datasets.MNIST(root='./data', train=True, transform=transform, download=True)
train_loader = DataLoader(dataset=train_dataset, batch_size=64, shuffle=True)


# --- 4. Kayıp Fonksiyonu, Optimizer ve TensorBoard ---
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# TensorBoard başlatma
writer = SummaryWriter('runs/mnist_egitim_1')
epochs = 5 

# --- 5. Eğitim Döngüsü (Training Loop) ---
print("\n--- Eğitim Başlıyor ---\n")

for epoch in range(epochs):
    running_loss = 0.0
    correct = 0
    total = 0
    
    for images, labels in train_loader:
        # Görselleri (Batch Size, 28, 28) boyutundan (Batch Size, 784) boyutuna düzleştiriyoruz
        images = images.view(images.size(0), -1)
        
        # İleri yayılım (Forward pass)
        outputs = model(images)
        loss = criterion(outputs, labels)
        
        # Geri yayılım (Backward pass) ve ağırlıkların güncellenmesi
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        # Metrikleri hesaplama
        running_loss += loss.item()
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()
    
    # Epoch sonu hesaplamaları
    epoch_loss = running_loss / len(train_loader)
    epoch_acc = 100 * correct / total
    
    # Terminale yazdırma
    print(f"Epoch [{epoch+1}/{epochs}] | Loss: {epoch_loss:.4f} | Accuracy: %{epoch_acc:.2f}")
    
    # TensorBoard'a kaydetme
    writer.add_scalar('Egitim/Loss', epoch_loss, epoch)
    writer.add_scalar('Egitim/Accuracy', epoch_acc, epoch)

writer.close()
print("\n--- Eğitim Tamamlandı ---")
print("Grafikleri görmek için terminalde şu komutu çalıştır: tensorboard --logdir=runs")
