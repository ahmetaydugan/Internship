import json
import random
from drain3 import TemplateMiner
from drain3.template_miner_config import TemplateMinerConfig
from drain3.masking import MaskingInstruction

# 1. YAPILANDIRMA: Maskeleme Kuralları
config = TemplateMinerConfig()
config.masking_instructions = [
    MaskingInstruction(mask_with="IP", pattern=r"((?<=[^A-Za-z0-9])|^)(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})((?=[^A-Za-z0-9])|$)"),
    MaskingInstruction(mask_with="BLOCK", pattern=r"(?<=blk_)[-\d]+"),
    MaskingInstruction(mask_with="NUM", pattern=r"((?<=[^A-Za-z0-9])|^)([\-\+]?\d+)((?=[^A-Za-z0-9])|$)")
]

miner = TemplateMiner(config=config)
cluster_stats = {}
structured_data = []

print("HDFS_2k.log işleniyor ve yapılandırılıyor...\n")

# 2. İŞLEME: Dosyayı Oku ve Drain3'e Besle
with open("HDFS_2k.log", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line: continue
        
        result = miner.add_log_message(line)
        cid = result["cluster_id"]
        template = result["template_mined"]
        
        # İstatistikler için kaydet
        if cid not in cluster_stats:
            cluster_stats[cid] = {
                "template": template,
                "count": 0,
                "example": line 
            }
        cluster_stats[cid]["count"] += 1
        
        # JSON dışa aktarımı için yapılandırılmış veri listesine ekle
        structured_data.append({
            "template_id": cid,
            "template": template,
            "raw_log": line
        })

# 3. DIŞA AKTARIM: JSON Olarak Kaydet (Hafta 7 Anomali Tespiti İçin)
with open("structured_logs.json", "w", encoding="utf-8") as json_file:
    json.dump(structured_data, json_file, indent=4, ensure_ascii=False)

# --- RAPORLAMA VE ÇIKTILAR ---

# Nadir (1 kez görülen) logları ayır
rare_clusters = {cid: data for cid, data in cluster_stats.items() if data["count"] == 1}

print("--- 1. TEMPLATE DAĞILIM ÖZETİ ---")
print(f"İşlenen Toplam Log Satırı         : {len(structured_data)}")
print(f"Üretilen Toplam Benzersiz Template: {len(cluster_stats)}")
print(f"Tek Seferlik (Anomali) Template   : {len(rare_clusters)}")
print(f"Durum: Veri seti 'structured_logs.json' olarak dışa aktarıldı.\n")

print("--- 2. BEKLENMEDİK / TEK SEFERLİK LOGLAR ---")
if not rare_clusters:
    print("Veri setinde tek seferlik log bulunamadı.\n")
else:
    for cid, data in rare_clusters.items():
        template_kisalt = data['template'][:100] + "..." if len(data['template']) > 100 else data['template']
        print(f"ID: {cid} | Template: {template_kisalt}")
print("\n")

print("--- 3. KALİTE KONTROL (RASTGELE 10 SATIR) ---")
sample_size = min(10, len(structured_data))
random_samples = random.sample(structured_data, sample_size)

for i, sample in enumerate(random_samples, 1):
    print(f"Örnek {i}")
    print(f"Gerçek Log: {sample['raw_log']}")
    print(f"Template  : [ID: {sample['template_id']}] {sample['template']}")
    print("-" * 70)
