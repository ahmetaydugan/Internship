import pandas as pd
from datetime import datetime
from drain3 import TemplateMiner
from drain3.template_miner_config import TemplateMinerConfig
from drain3.masking import MaskingInstruction

# --- 1. DRAIN3 AYARLARI VE LOG OKUMA ---
config = TemplateMinerConfig()
config.masking_instructions = [
    MaskingInstruction(mask_with="IP", pattern=r"((?<=[^A-Za-z0-9])|^)(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})((?=[^A-Za-z0-9])|$)"),
    MaskingInstruction(mask_with="BLOCK", pattern=r"(?<=blk_)[-\d]+"),
    MaskingInstruction(mask_with="NUM", pattern=r"((?<=[^A-Za-z0-9])|^)([\-\+]?\d+)((?=[^A-Za-z0-9])|$)")
]
miner = TemplateMiner(config=config)

def extract_timestamp(line):
    try:
        parts = line.split()
        return datetime.strptime(parts[0] + " " + parts[1], "%y%m%d %H%M%S")
    except Exception:
        return None

print("Veri seti hazırlanıyor (Loglar okunup pencerelere bölünüyor)...")
log_records = []
with open("HDFS_2k.log", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line: continue
        ts = extract_timestamp(line)
        if ts:
            res = miner.add_log_message(line)
            log_records.append({"timestamp": ts, "cluster_id": res["cluster_id"]})

df = pd.DataFrame(log_records)
df.set_index("timestamp", inplace=True)
# 1 dakikalık periyotlarla frekans matrisini oluşturuyoruz
time_bins = df.groupby([pd.Grouper(freq='1min'), 'cluster_id']).size().unstack(fill_value=0)


# --- 2. KURAL TABANLI SİSTEM (SABİT EŞİK) ---
def kural_tabanli_test(matris, sabit_deger):
    """
    Sisteme dışarıdan "if frekans > X ise anomali de" kuralını verir.
    Geçmiş veriyi veya logun kendi karakteristiğini umursamaz.
    """
    # Matris içindeki değeri sabit eşiği aşan toplam hücre sayısını bul
    anomali_sayisi = (matris > sabit_deger).sum().sum()
    return anomali_sayisi


# --- 3. İSTATİSTİKSEL / ÖĞRENEN SİSTEM (DİNAMİK EŞİK) ---
def istatistiksel_test(matris, sigma_carpani):
    """
    Her log şablonunun kendi geçmişine (ortalamasına) ve dalgalanma payına (standart sapma)
    bakarak her şablon için eşiği otomatik olarak kendi belirler.
    """
    toplam_anomali = 0
    for col in matris.columns:
        seri = matris[col]
        mean, std = seri.mean(), seri.std()
        if pd.isna(std): std = 0.0
        
        # Formül: Dinamik Eşik = Ortalama + (Çarpan * Standart Sapma)
        dinamik_esik = mean + (sigma_carpani * std)
        
        # Hem eşiği aşan hem de gerçekten görülmüş ( > 0 ) olanları say
        toplam_anomali += ((seri > dinamik_esik) & (seri > 0)).sum()
        
    return toplam_anomali


# --- 4. KONTROLLÜ DENEY VE RAPORLAMA ---
print("\n" + "="*60)
print(" KURAL TABANLI vs İSTATİSTİKSEL ÖĞRENME DENEYİ ")
print("="*60 + "\n")

# Deney 1: Sabit Eşik Değerlerini Değiştirmek
sabit_esikler = [2, 5, 10, 25, 50]
print("--- 1. YAKLAŞIM: KURAL TABANLI (SABİT EŞİK) ---")
print("Mantık: 'Dakikada X adedi geçen her log tehlikelidir.'\n")

for esik in sabit_esikler:
    sonuc = kural_tabanli_test(time_bins, esik)
    print(f"Eşik Değeri: {esik:2d}  -->  Bulunan Anomali: {sonuc}")

print("\n" + "-"*60 + "\n")

# Deney 2: Standart Sapma (Sigma) Çarpanını Değiştirmek
sigma_degerleri = [1, 2, 3, 4]
print("--- 2. YAKLAŞIM: İSTATİSTİKSEL (DİNAMİK EŞİK) ---")
print("Mantık: 'Ortalama rutininden Y sigma kadar sapan log tehlikelidir.'\n")

for sigma in sigma_degerleri:
    sonuc = istatistiksel_test(time_bins, sigma)
    print(f"Sigma Çarpanı: {sigma}  -->  Bulunan Anomali: {sonuc}")

print("\n" + "="*60)
