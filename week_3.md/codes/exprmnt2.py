import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter

# --- 1. Veri Setinin Hazırlanması ---
transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))])
train_dataset = datasets.MNIST(root='./data', train=True, transform=transform, download=True)
train_loader = DataLoader(dataset=train_dataset, batch_size=64, shuffle=True)

# --- 2. Model Mimarilerinin Tanımlanması ---

# Model 1: Orijinal 3 Katmanlı 
class Orijinal_3_Katman(nn.Module):
    def __init__(self):
        super(Orijinal_3_Katman, self).__init__()
        self.fc1 = nn.Linear(784, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 10)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        return self.fc3(x)

# Model 2: Derin 4 Katmanlı (Görev gereği 1 katman eklenmiş model)
class Derin_4_Katman(nn.Module):
    def __init__(self):
        super(Derin_4_Katman, self).__init__()
        self.fc1 = nn.Linear(784, 256)
        self.fc2 = nn.Linear(256, 128)
        self.fc3 = nn.Linear(128, 64)
        self.fc4 = nn.Linear(64, 10)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.relu(self.fc3(x))
        return self.fc4(x)

# --- 3. Eğitim ve TensorBoard Loglama Fonksiyonu ---
def train_and_log(model, run_name):
    print(f"\n>>> Eğitiliyor: {run_name} <<<")
    
    # TensorBoard Writer'ı başlatıyoruz
    writer = SummaryWriter(f'runs/deney2/{run_name}')
    
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    epochs = 5

    for epoch in range(epochs):
        running_loss = 0.0
        
        for images, labels in train_loader:
            images = images.view(images.size(0), -1) # Flatten işlemi
            
            outputs = model(images)
            loss = criterion(outputs, labels)
            
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item()
            
        epoch_loss = running_loss / len(train_loader)
        print(f"Epoch [{epoch+1}/{epochs}] | Loss: {epoch_loss:.4f}")
        
        writer.add_scalar('Karsilastirma/Loss', epoch_loss, epoch)
        
    writer.close()
    print(f"--- {run_name} Eğitimi Tamamlandı ---")

# --- 4. Deneyin Çalıştırılması ---
if __name__ == "__main__":
    print("--- Katman Sayısı Karşılaştırma Deneyi Başlıyor ---")
    
    # 3 Katmanlı Modelin Eğitimi
    model_3 = Orijinal_3_Katman()
    train_and_log(model_3, "Orijinal_3_Katman")
    
    # 4 Katmanlı Modelin Eğitimi
    model_4 = Derin_4_Katman()
    train_and_log(model_4, "Derin_4_Katman")
    
    print("\n--- Tüm Eğitimler Tamamlandı ---")
    print("Colab'de yeni bir hücre açıp şu komutu çalıştırarak grafikleri gör:")
    print("%load_ext tensorboard")
    print("%tensorboard --logdir runs/deney2")
