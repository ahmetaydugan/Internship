from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Gerçekçi ve Çok Cümleli Metin Seti (12 Paragraf)
paragraflar = [
    # Tema 1: Yapay Zeka ve Makine Öğrenmesi (Wikipedia)
    "Yapay zeka, makinelerin insan zekasına benzer bilişsel işlevleri yerine getirme yeteneğidir. Alanın temelleri 1956 yılında düzenlenen Dartmouth Konferansı'nda atılmış olup, bu etkinlikte alanın ismi resmi olarak kabul edilmiştir. O günden bu yana yapay zeka araştırmaları birçok iniş ve çıkış yaşamıştır.",
    "Yapay zeka kışları, bu alana yönelik araştırma fonlarının kesildiği ve genel ilginin azaldığı durağan dönemleri tanımlamak için kullanılır. İyimser beklentilerin karşılanamaması ve donanım yetersizlikleri bu dönemlerin temel tetikleyicileri olmuştur. Tarihsel olarak, özellikle 1970'ler ve 1980'lerin sonlarında iki büyük kış dönemi yaşanmıştır.",
    "Makine öğrenmesi, bilgisayarların açıkça programlanmadan verilerden öğrenmesini sağlayan algoritmaların incelenmesidir. Sistemler deneyim kazandıkça belirli görevlerdeki performanslarını otomatik olarak iyileştirirler. Günümüzde spam filtrelemeden görüntü tanımaya kadar çok geniş bir yelpazede başarıyla uygulanmaktadır.",
    "Çok katmanlı algılayıcı (MLP), ileri beslemeli bir yapay sinir ağı sınıfıdır. Girdi, gizli ve çıktı katmanlarından oluşur ve verilerdeki karmaşık, doğrusal olmayan ilişkileri modellemek için kullanılır. Özellikle derin öğrenme mimarilerinin temel yapı taşlarından birini oluşturur.",
    
    # Tema 2: Python ve Veri Bilimi Ekosistemi (Dokümantasyonlar)
    "Python, nesne yönelimli, yorumlanabilir ve yüksek seviyeli genel amaçlı bir programlama dilidir. Sözdiziminin okunabilirliği ve sadeliği sayesinde hem yeni başlayanlar hem de profesyoneller tarafından yaygın olarak benimsenmiştir. Geniş standart kütüphanesi, onu veri bilimi ve otomasyon alanlarında öne çıkarır.",
    "Pandas, Python programlama dili için yüksek performanslı veri manipülasyonu ve analizi araçları sunan açık kaynaklı bir kütüphanedir. Özellikle tablo şeklindeki verileri işlemek için geliştirilen DataFrame yapısı, veri bilimcilerin en çok başvurduğu araçlardandır. Eksik verilerin doldurulması ve verilerin gruplanması gibi işlemleri büyük ölçüde kolaylaştırır.",
    "Scikit-learn, Python tabanlı makine öğrenmesi uygulamaları için endüstri standardı haline gelmiş bir kütüphanedir. Sınıflandırma, regresyon ve kümeleme gibi temel algoritmaları tek bir standart API üzerinden kullanıcıya sunar. NumPy ve SciPy kütüphaneleriyle tam uyumlu çalışacak şekilde tasarlanmıştır.",
    "PyTorch, makine öğrenmesi ve derin öğrenme modelleri geliştirmek için kullanılan güçlü bir açık kaynaklı çerçevedir. Özellikle dinamik hesaplama grafikleri (dynamic computation graphs) sunması, araştırmacıların modelleri eğitirken anlık değişiklikler yapabilmesine olanak tanır. GPU hızlandırması sayesinde büyük veri setleri üzerinde yüksek performans gösterir.",
    
    # Tema 3: YBS ve Finansal Analiz
    "Yönetim Bilişim Sistemleri (YBS), işletmelerin karar verme süreçlerini desteklemek amacıyla teknoloji, insan ve süreçleri bir araya getiren disiplinlerarası bir alandır. Bilginin toplanması, işlenmesi ve stratejik bir değere dönüştürülmesi bu bölümün temel odak noktasıdır. Günümüz iş dünyasında, organizasyonların dijital dönüşüm süreçlerini yönetmek için kritik bir rol oynar.",
    "Cari oran, bir işletmenin kısa vadeli borçlarını dönen varlıklarıyla karşılama kapasitesini ölçen temel bir finansal likidite rasyosudur. Bu oranın 1.5 ile 2.0 arasında olması, işletmenin borç ödeme gücünün yeterli kabul edildiğini gösterir. Ancak oranın çok yüksek olması, atıl fonların etkin kullanılmadığı anlamına da gelebilir.",
    "Nakit oranı, işletmenin stoklar ve alacaklar gibi nakde dönüşmesi zaman alabilecek varlıklarını dışarıda bırakarak sadece hazır değerleriyle kısa vadeli borçlarını ödeme gücünü gösterir. En muhafazakar likidite ölçütlerinden biri olarak kabul edilir. Kriz dönemlerinde şirketlerin finansal dayanıklılığını test etmek için sıklıkla başvurulan bir metriktir.",
    "Borç/Özkaynak oranı, bir şirketin varlıklarını finanse etmek için kullandığı yabancı kaynaklar ile ortakların koyduğu sermaye arasındaki ilişkiyi gösterir. Bu oranın yüksek olması şirketin finansal riskinin arttığına işaret ederken, yatırımcılar için potansiyel getirinin de yüksek olabileceğini ima edebilir. Sektör ortalamalarıyla karşılaştırılarak analiz edilmesi en doğru sonucu verir."
]

# 2. Çok Dilli Modeli Yükleme (Türkçe anlamsal ilişkiler için)
print("Model yükleniyor ve embedding'ler oluşturuluyor...")
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
embeddings = model.encode(paragraflar)

# 3. Cosine Similarity Matrisini Hesaplama
similarity_matrix = cosine_similarity(embeddings)

# 4. Sonuçları Görselleştirme
plt.figure(figsize=(11, 9))
sns.heatmap(similarity_matrix, annot=True, cmap="YlGnBu", fmt=".2f", 
            xticklabels=[f"P{i+1}" for i in range(12)], 
            yticklabels=[f"P{i+1}" for i in range(12)])

plt.title("Gelişmiş Metin Seti ile Cosine Similarity (Anlamsal Benzerlik) Matrisi")
plt.xlabel("Paragraf İndeksi")
plt.ylabel("Paragraf İndeksi")
plt.tight_layout()
plt.show()
