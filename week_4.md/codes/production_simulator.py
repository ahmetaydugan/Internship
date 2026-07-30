import time
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

def main():
    print("Model eğitiliyor... Lütfen bekleyin.")
    # 1. Model Eğitimi (Bu işlem production'da sadece bir kere yapılır, döngüye girmez)
    data = fetch_20newsgroups(subset='train', categories=['sci.space', 'comp.graphics', 'rec.autos'])
    model = make_pipeline(TfidfVectorizer(), MultinomialNB())
    model.fit(data.data, data.target)
    print("Model eğitimi tamamlandı!\n")

    # 2. 15 Örnek Cümle (Test Veriseti)
    test_sentences = [
        # sci.space (Uzay)
        "The Hubble telescope captured a stunning image of a nebula.",
        "NASA is planning a new mission to Mars next year.",
        "Astronauts perform spacewalks to repair the orbital station.",
        "Deep space exploration requires advanced rocket propulsion.",
        "The lunar rover gathered soil samples from the moon's surface.",
        # comp.graphics (Grafik/Teknoloji)
        "High resolution texture mapping is key for 3D games.",
        "Graphics rendering speed depends heavily on your GPU.",
        "Photoshop is widely used for pixel editing and image manipulation.",
        "The new monitor supports 4K resolution and a 144Hz refresh rate.",
        "Vector graphics scale perfectly without losing any quality.",
        # rec.autos (Otomotiv)
        "My car's transmission needs a fluid change as soon as possible.",
        "The V8 engine produces a lot of horsepower and torque.",
        "Electric vehicles are becoming more popular due to battery improvements.",
        "I need to replace the brake pads and tires on my truck.",
        "The steering wheel vibrates when I drive over 60 miles per hour."
    ]

    total_latency_ms = 0
    total_tokens = 0
    
    # Tablo başlığı
    print(f"{'Metin (İlk 30 Karakter)':<35} | {'Kategori':<15} | {'Süre (ms)':<10} | {'Token'}")
    print("-" * 75)

    # 3. Otomatik Test ve Loglama Döngüsü
    for sentence in test_sentences:
        start_time = time.perf_counter()
        
        # Modele tahmin yaptırıyoruz
        prediction_idx = model.predict([sentence])[0]
        category = data.target_names[prediction_idx]
        
        end_time = time.perf_counter()
        
        # Metrikleri hesaplıyoruz
        latency_ms = (end_time - start_time) * 1000
        token_count = len(sentence.split()) # Basit token yaklaşımı (kelime sayısı)
        
        total_latency_ms += latency_ms
        total_tokens += token_count
        
        # Terminale o anki işlemin logunu basıyoruz
        short_text = sentence[:30] + "..."
        print(f"{short_text:<35} | {category:<15} | {latency_ms:>7.4f} | {token_count}")

    # 4. Production Metrikleri ve Maliyet Analizi Özet Ekranı
    avg_latency = total_latency_ms / len(test_sentences)
    avg_tokens = total_tokens / len(test_sentences)
    
    # 1 Milyon istek için senaryo (Örnek: 1 Milyon token = ~$0.15 baz alınmıştır)
    daily_requests = 1_000_000
    cost_per_million_tokens = 0.15 
    estimated_daily_tokens = avg_tokens * daily_requests
    estimated_daily_cost = (estimated_daily_tokens / 1_000_000) * cost_per_million_tokens

    print("\n" + "="*45)
    print("       PRODUCTION METRİKLERİ ÖZETİ")
    print("="*45)
    print(f"Toplam Test Edilen İstek : {len(test_sentences)}")
    print(f"Ortalama Yanıt Süresi    : {avg_latency:.4f} ms")
    print(f"Ortalama Token / İstek   : {avg_tokens:.1f} token")
    print("-" * 45)
    print("SİMÜLE EDİLMİŞ MALİYET ANALİZİ (Günde 1M İstek)")
    print(f"Tahmini Günlük Token     : {estimated_daily_tokens:,.0f}")
    print(f"Tahmini Günlük Maliyet   : ${estimated_daily_cost:.2f} (Örnek LLM API)")
    print("="*45)

if __name__ == "__main__":
    main()
