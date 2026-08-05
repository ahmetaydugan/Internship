import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from groq import Groq

# --- 0. GÜVENLİK VE YAPILANDIRMA ---
# .env dosyasını belleğe yükle
load_dotenv()

# API anahtarını .env dosyasından çekiyoruz
api_key_from_env = os.getenv("GROQ_API_KEY")

# Eğer .env dosyası okunamazsa sistemi uyararak durdurur
if not api_key_from_env:
    raise ValueError("API anahtarı bulunamadı! Lütfen .env dosyasını kontrol edin.")

# İstemciyi güvenli anahtarla başlat
client = Groq(api_key=api_key_from_env)

# --- 1. BİLGİ TABANI (KNOWLEDGE BASE) ---
documents = [
    "Yapay zeka, makinelerin insan zekasına benzer bilişsel işlevleri yerine getirme yeteneğidir. Alanın temelleri 1956 yılında düzenlenen Dartmouth Konferansı'nda atılmış olup, bu etkinlikte alanın ismi resmi olarak kabul edilmiştir. O günden bu yana yapay zeka araştırmaları birçok iniş ve çıkış yaşamıştır.",
    "Yapay zeka kışları, bu alana yönelik araştırma fonlarının kesildiği ve genel ilginin azaldığı durağan dönemleri tanımlamak için kullanılır. İyimser beklentilerin karşılanamaması ve donanım yetersizlikleri bu dönemlerin temel tetikleyicileri olmuştur. Tarihsel olarak, özellikle 1970'ler ve 1980'lerin sonlarında iki büyük kış dönemi yaşanmıştır.",
    "Makine öğrenmesi, bilgisayarların açıkça programlanmadan verilerden öğrenmesini sağlayan algoritmaların incelenmesidir. Sistemler deneyim kazandıkça belirli görevlerdeki performanslarını otomatik olarak iyileştirirler. Günümüzde spam filtrelemeden görüntü tanımaya kadar çok geniş bir yelpazede başarıyla uygulanmaktadır.",
    "Çok katmanlı algılayıcı (MLP), ileri beslemeli bir yapay sinir ağı sınıfıdır. Girdi, gizli ve çıktı katmanlarından oluşur ve verilerdeki karmaşık, doğrusal olmayan ilişkileri modellemek için kullanılır. Özellikle derin öğrenme mimarilerinin temel yapı taşlarından birini oluşturur.",
    "Python, nesne yönelimli, yorumlanabilir ve yüksek seviyeli genel amaçlı bir programlama dilidir. Sözdiziminin okunabilirliği ve sadeliği sayesinde hem yeni başlayanlar hem de profesyoneller tarafından yaygın olarak benimsenmiştir. Geniş standart kütüphanesi, onu veri bilimi ve otomasyon alanlarında öne çıkarır.",
    "Pandas, Python programlama dili için yüksek performanslı veri manipülasyonu ve analizi araçları sunan açık kaynaklı bir kütüphanedir. Özellikle tablo şeklindeki verileri işlemek için geliştirilen DataFrame yapısı, veri bilimcilerin en çok başvurduğu araçlardandır. Eksik verilerin doldurulması ve verilerin gruplanması gibi işlemleri büyük ölçüde kolaylaştırır.",
    "Scikit-learn, Python tabanlı makine öğrenmesi uygulamaları için endüstri standardı haline gelmiş bir kütüphanedir. Sınıflandırma, regresyon ve kümeleme gibi temel algoritmaları tek bir standart API üzerinden kullanıcıya sunar. NumPy ve SciPy kütüphaneleriyle tam uyumlu çalışacak şekilde tasarlanmıştır.",
    "PyTorch, makine öğrenmesi ve derin öğrenme modelleri geliştirmek için kullanılan güçlü bir açık kaynaklı çerçevedir. Özellikle dinamik hesaplama grafikleri (dynamic computation graphs) sunması, araştırmacıların modelleri eğitirken anlık değişiklikler yapabilmesine olanak tanır. GPU hızlandırması sayesinde büyük veri setleri üzerinde yüksek performans gösterir.",
    "Yönetim Bilişim Sistemleri (YBS), işletmelerin karar verme süreçlerini desteklemek amacıyla teknoloji, insan ve süreçleri bir araya getiren disiplinlerarası bir alandır. Bilginin toplanması, işlenmesi ve stratejik bir değere dönüştürülmesi bu bölümün temel odak noktasıdır. Günümüz iş dünyasında, organizasyonların dijital dönüşüm süreçlerini yönetmek için kritik bir rol oynar.",
    "Cari oran, bir işletmenin kısa vadeli borçlarını dönen varlıklarıyla karşılama kapasitesini ölçen temel bir finansal likidite rasyosudur. Bu oranın 1.5 ile 2.0 arasında olması, işletmenin borç ödeme gücünün yeterli kabul edildiğini gösterir. Ancak oranın çok yüksek olması, atıl fonların etkin kullanılmadığı anlamına da gelebilir.",
    "Nakit oranı, işletmenin stoklar ve alacaklar gibi nakde dönüşmesi zaman alabilecek varlıklarını dışarıda bırakarak sadece hazır değerleriyle kısa vadeli borçlarını ödeme gücünü gösterir. En muhafazakar likidite ölçütlerinden biri olarak kabul edilir. Kriz dönemlerinde şirketlerin finansal dayanıklılığını test etmek için sıklıkla başvurulan bir metriktir.",
    "Borç/Özkaynak oranı, bir şirketin varlıklarını finanse etmek için kullandığı yabancı kaynaklar ile ortakların koyduğu sermaye arasındaki ilişkiyi gösterir. Bu oranın yüksek olması şirketin finansal riskinin arttığına işaret ederken, yatırımcılar için potansiyel getirinin de yüksek olabileceğini ima edebilir. Sektör ortalamalarıyla karşılaştırılarak analiz edilmesi en doğru sonucu verir."
]

# --- 2. EMBEDDING MODELİNİ YÜKLEME ---
print("Embedding modeli yükleniyor...")
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# --- 3. DOKÜMANLARI VEKTÖRLERE ÇEVİRME ---
print("Dokümanlar vektör uzayına yerleştiriliyor...")
doc_embeddings = embedding_model.encode(documents)

# --- 4. KULLANICI SORGUSU ---
query = "Yapay zeka alanında araştırmalara olan ilginin azaldığı ve maddi desteklerin kesildiği dönemlere ne ad verilir?"
print(f"\nSoru: {query}\n")
print("-" * 50)

# --- 5. BENZERLİK HESAPLAMA (RETRIEVAL) ---
query_embedding = embedding_model.encode([query])
similarities = cosine_similarity(query_embedding, doc_embeddings)[0]

# --- 6. EN YAKIN DOKÜMANLARI BULMA (TOP-K) ---
k = 2
top_k_indices = np.argsort(similarities)[::-1][:k]

print("Bağlam olarak kullanılacak dokümanlar bulundu.")
for rank, index in enumerate(top_k_indices, 1):
    print(f"Top {rank} Skor: {similarities[index]:.4f} -> Index: {index}")


# --- 7. LLM ENTEGRASYONU (GENERATION) ---
print("-" * 50)
print("Groq LLM istemcisi başlatılıyor...")

# Bulunan dokümanları birleştirip tek bir bağlam metni oluşturma
retrieved_texts = [documents[i] for i in top_k_indices]
context = "\n\n---\n\n".join(retrieved_texts)

print("\nBağlam Groq LLM'e gönderildi, cevap bekleniyor...")

# LLM Prompt Yönetimi ve İçerik Üretme
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "Sen kurumsal bir yapay zeka asistanısın. Sana verilen 'Sağlanan Bağlam' metnini dikkatlice oku. Kullanıcının sorusunu SADECE bu metne dayanarak, net ve kısa bir şekilde cevapla. Kendi içsel bilgilerini kesinlikle kullanma."
        },
        {
            "role": "user",
            "content": f"Sağlanan Bağlam:\n{context}\n\nKullanıcı Sorusu: {query}"
        }
    ],
    model="llama-3.1-8b-instant", 
    temperature=0.1, 
)

print("\nRAG SİSTEMİ CEVABI:")
print(chat_completion.choices[0].message.content)
