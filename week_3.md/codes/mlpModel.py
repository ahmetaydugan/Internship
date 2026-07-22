import torch
import torch.nn as nn

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

# --- 2. Modelin Başlatılması ---
input_dim = 784
hidden_dim1 = 128
hidden_dim2 = 64
output_dim = 10

model = SimpleMLP(input_dim, hidden_dim1, hidden_dim2, output_dim)
print("--- Model Mimarisi ---")
print(model)

# --- 3. Parametre Sayısının Hesaplanması ---
total_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
print(f"\n--- Modeldeki Toplam Eğitilebilir Parametre Sayısı: {total_params} ---")

# --- 4. İleri Yayılım (Forward Pass) Testi ---
# 1 adet, 784 özellikli sahte (dummy) veri oluşturuyoruz (Örn: 1 adet 28x28 piksel görsel)
dummy_input = torch.randn(1, 784)

# Veriyi modele verip tahminde bulunmasını sağlıyoruz
output = model(dummy_input)

print("\n--- Boyut Kontrolü ---")
print("Girdi Boyutu (Batch Size, Özellik):", dummy_input.shape)
print("Çıktı Boyutu (Batch Size, Sınıf Sayısı):", output.shape)
print("\nModelin Ürettiği Ham Çıktılar (Logits):")
print(output)