import pandas as pd
from datetime import datetime
from drain3 import TemplateMiner
from drain3.template_miner_config import TemplateMinerConfig
from drain3.masking import MaskingInstruction

# 1. HDFS Loglarından Zaman Bilgisini Çıkarma Fonksiyonu
def extract_timestamp(line):
    try:
        parts = line.split()
        date_str = parts[0] + " " + parts[1]
        return datetime.strptime(date_str, "%y%m%d %H%M%S")
    except Exception:
        return None

# 2. İstatistiksel Anomali Tespit Fonksiyonu
def detect_anomalies(time_bins_df, std_multiplier=2):
    anomalies = []
    
    for template_id in time_bins_df.columns:
        freq_series = time_bins_df[template_id]
        
        mean_val = freq_series.mean()
        std_val = freq_series.std()
        
        if pd.isna(std_val):
            std_val = 0.0
            
        threshold = mean_val + (std_multiplier * std_val)
        outliers = freq_series[(freq_series > threshold) & (freq_series > 0)]
        
        for timestamp, count in outliers.items():
            anomalies.append({
                'Zaman': timestamp,
                'Template_ID': template_id,
                'Frekans': count,
                'Ortalama': round(mean_val, 3),
                'Standart_Sapma': round(std_val, 3),
                'Esik_Degeri': round(threshold, 3)
            })
            
    return pd.DataFrame(anomalies)

# 3. Drain3 Konfigürasyonu
config = TemplateMinerConfig()
config.masking_instructions = [
    MaskingInstruction(mask_with="IP", pattern=r"((?<=[^A-Za-z0-9])|^)(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})((?=[^A-Za-z0-9])|$)"),
    MaskingInstruction(mask_with="BLOCK", pattern=r"(?<=blk_)[-\d]+"),
    MaskingInstruction(mask_with="NUM", pattern=r"((?<=[^A-Za-z0-9])|^)([\-\+]?\d+)((?=[^A-Za-z0-9])|$)")
]

miner = TemplateMiner(config=config)
log_records = []

# 4. Logları Okuma ve İşleme
print("1/3 - Loglar okunuyor ve ayrıştırılıyor...")
with open("HDFS_2k.log", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line: continue
        
        timestamp = extract_timestamp(line)
        if not timestamp: continue
            
        result = miner.add_log_message(line)
        
        log_records.append({
            "timestamp": timestamp,
            "cluster_id": result["cluster_id"],
            "template": result["template_mined"]
        })

# 5. Veriyi Pandas DataFrame'e Çevirme ve time_bins OLUŞTURMA
print("2/3 - Zaman pencereleri (time_bins) hesaplanıyor...")
df = pd.DataFrame(log_records)
df.set_index("timestamp", inplace=True)

freq = '1min' # 1 dakikalık pencereler
# Eksik olan time_bins değişkeni burada tanımlanıyor
time_bins = df.groupby([pd.Grouper(freq=freq), 'cluster_id']).size().unstack(fill_value=0)

# 6. Anomalileri Tespit Etme ve Listeleme
print("3/3 - Anomaliler tespit ediliyor...\n")
detected_anomalies = detect_anomalies(time_bins, std_multiplier=2)

print("--- TESPİT EDİLEN ANOMALİ ADAYLARI ---")
if not detected_anomalies.empty:
    detected_anomalies = detected_anomalies.sort_values(by='Zaman').reset_index(drop=True)
    print(detected_anomalies.to_string())
else:
    print("Belirtilen eşik değerini aşan herhangi bir anomali tespit edilmedi.")
