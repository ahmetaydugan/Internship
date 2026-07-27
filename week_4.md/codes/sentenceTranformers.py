from sentence_transformers import SentenceTransformer, util

# Türkçe destekli, hafif bir çok dilli model yüklüyoruz
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# Test edeceğimiz kelimeler
words = ["bilgisayar", "mouse", "monitör", "kedi"]

# Kelimeleri matematiksel vektörlere (embedding) çeviriyoruz
embeddings = model.encode(words)

# "bilgisayar" kelimesinin vektörünü referans olarak alalım (0. indeks)
bilgisayar_embedding = embeddings[0]

print("Kosinüs Benzerliği Sonuçları ('bilgisayar' kelimesine göre):\n")

# "bilgisayar" ile diğer kelimeler arasındaki benzerliği hesaplıyoruz
for i in range(1, len(words)):
    similarity = util.cos_sim(bilgisayar_embedding, embeddings[i])
    print(f"'bilgisayar' ve '{words[i]}' benzerliği: {similarity.item():.4f}")

    
