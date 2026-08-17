import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from drain3 import TemplateMiner
from drain3.template_miner_config import TemplateMinerConfig
from drain3.masking import MaskingInstruction

# 1. HDFS Loglarından Zaman Bilgisini Çıkarma Fonksiyonu
# Örnek HDFS Log Başı: "081109 203518 143 INFO..." (YılAyGün SaatDakikaSaniye)
def extract_timestamp(line):
    try:
        parts = line.split()
        date_str = parts[0] + " " + parts[1]
        # Yıl(2 hane)AyGün SaatDakikaSaniye formatını datetime objesine çeviriyoruz
        return datetime.strptime(date_str, "%y%m%d %H%M%S")
    except Exception:
        return None

# 2. Drain3 Konfigürasyonu
config = TemplateMinerConfig()
config.masking_instructions = [
    MaskingInstruction(mask_with="IP", pattern=r"((?<=[^A-Za-z0-9])|^)(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})((?=[^A-Za-z0-9])|$)"),
    MaskingInstruction(mask_with="BLOCK", pattern=r"(?<=blk_)[-\d]+"),
    MaskingInstruction(mask_with="NUM", pattern=r"((?<=[^A-Za-z0-9])|^)([\-\+]?\d+)((?=[^A-Za-z0-9])|$)")
]

miner = TemplateMiner(config=config)
log_records = []

# 3. Logları Okuma ve İşleme
print("Loglar işleniyor, lütfen bekleyin...")
with open("HDFS_2k.log", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line: continue
        
        timestamp = extract_timestamp(line)
        if not timestamp:
            continue # Zaman bilgisi okunamayan satırları atla
            
        result = miner.add_log_message(line)
        
        # Her log satırını bir kayıt olarak listeye ekle
        log_records.append({
            "timestamp": timestamp,
            "cluster_id": result["cluster_id"],
            "template": result["template_mined"]
        })

# 4. Veriyi Pandas DataFrame'e Çevirme
df = pd.DataFrame(log_records)
df.set_index("timestamp", inplace=True)

# 5. Zaman Periyotlarına Göre Gruplama (Örn: '1min' = 1 dakikalık, '1H' = 1 saatlik)
# Logların yoğunluğuna göre '1min' veya '10s' (10 saniye) olarak değiştirebilirsiniz.
freq = '1min' 
time_bins = df.groupby([pd.Grouper(freq=freq), 'cluster_id']).size().unstack(fill_value=0)

# İstenen 1: Benzersiz Şablonların Genel Dağılım Özeti
total_counts = df['cluster_id'].value_counts()
rare_clusters = total_counts[total_counts == 1].index.tolist()

print("\n--- TEMPLATE DAĞILIM ÖZETİ ---")
print(f"Üretilen Toplam Benzersiz Template: {len(total_counts)}")
print(f"Tek Seferlik (Beklenmedik) Template Sayısı: {len(rare_clusters)}")

# 6. Grafiği Çizdirme
plt.style.use('seaborn-v0_8-darkgrid')
plt.figure(figsize=(16, 8))

# Her bir cluster_id (template) için zaman serisi çizgisi ekle
for col in time_bins.columns:
    if col in rare_clusters:
        # ÇÖZÜM: Sadece değeri 0'dan büyük olan (gerçekten görüldüğü) anları filtrele
        active_data = time_bins[time_bins[col] > 0][col]
        plt.plot(active_data.index, active_data.values, marker='X', markersize=12, linestyle='None', label=f'Tek Seferlik - ID: {col}')
    else:
        # Normal log şablonları için sıfıra inmeleri rutindir, onları normal çizdiriyoruz
        plt.plot(time_bins.index, time_bins[col], marker='o', markersize=4, label=f'Template {col}')

plt.title(f'Zaman İçinde Log Şablon (Template) Dağılımı ({freq} Periyotlarla)')
plt.xlabel('Zaman')
plt.ylabel('Log Görülme Sıklığı')
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0.)
plt.tight_layout()
plt.show()
