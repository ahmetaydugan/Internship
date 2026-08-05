from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# 1. Bilgi Tabanı (Knowledge Base) - Dünkü Doküman Seti
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

# 2. Embedding Modelini Yükleme
print("Model yükleniyor...")
model = SentenceTransformer('all-MiniLM-L6-v2')

# 3. Dokümanları Vektörlere Çevirme (Offline aşama / Veritabanına kayıt simülasyonu)
print("Dokümanlar embedding'e çevriliyor (vektör uzayına yerleştiriliyor)...")
doc_embeddings = model.encode(documents)

# 4. Kullanıcı Sorgusu (Query)
query = "Yapay zeka alanında araştırmalara olan ilginin azaldığı ve maddi desteklerin kesildiği dönemlere ne ad verilir?"
print(f"\nSoru: {query}\n")
print("-" * 50)

# 5. Sorguyu Vektöre Çevirme ve Benzerlik Hesaplama
query_embedding = model.encode([query])

# Cosine Similarity ile sorgu vektörünün, tüm doküman vektörleriyle arasındaki açıyı ölçüyoruz.
# Sonuç, -1 ile 1 arasında değer alan bir dizidir. (1 = mükemmel eşleşme)
similarities = cosine_similarity(query_embedding, doc_embeddings)[0]

# 6. En Yakın K Dokümanı Bulma (Top-K)
k = 3
# np.argsort indeksleri küçükten büyüğe sıralar. [::-1] ile ters çevirip en büyükleri alıyoruz.
top_k_indices = np.argsort(similarities)[::-1][:k]

# Sonuçları Yazdırma
for rank, index in enumerate(top_k_indices, 1):
    score = similarities[index]
    print(f"Top {rank} | Benzerlik Skoru: {score:.4f}")
    print(f"Doküman: {documents[index]}\n")
