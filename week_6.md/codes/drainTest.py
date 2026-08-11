from drain3 import TemplateMiner

# Drain3 yöneticisi başlatılıyor
miner = TemplateMiner()
cluster_stats = {}

print("HDFS_2k.log işleniyor...\n")

# Dosyayı oku ve logları Drain3'e besle
with open("HDFS_2k.log", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
            
        result = miner.add_log_message(line)
        cluster_id = result["cluster_id"]
        
        # Şablon verilerini kaydet ve sayacı artır
        if cluster_id not in cluster_stats:
            cluster_stats[cluster_id] = {
                "template": result["template_mined"],
                "count": 0
            }
        
        cluster_stats[cluster_id]["count"] += 1

# Şablonları frekansa göre (count) azalan şekilde sırala
sorted_clusters = sorted(
    cluster_stats.items(), 
    key=lambda item: item[1]["count"], 
    reverse=True
)

# İstenilen terminal çıktısını oluştur
print(f"Toplam benzersiz template (şablon) sayısı: {len(sorted_clusters)}")
print("-" * 70)
print("En sık görülen 5 template:\n")

for i, (cid, data) in enumerate(sorted_clusters[:5], 1):
    print(f"{i}. Template: {data['template']}")
    print(f"   Görülme Sıklığı: {data['count']}")
    print("-" * 70)
