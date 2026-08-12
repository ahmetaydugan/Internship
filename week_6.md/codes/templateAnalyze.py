from drain3 import TemplateMiner
from drain3.template_miner_config import TemplateMinerConfig
from drain3.masking import MaskingInstruction

# regex_pattern yerine pattern kullanıldı
config = TemplateMinerConfig()
config.masking_instructions = [
    MaskingInstruction(mask_with="IP", pattern=r"((?<=[^A-Za-z0-9])|^)(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})((?=[^A-Za-z0-9])|$)"),
    MaskingInstruction(mask_with="BLOCK", pattern=r"(?<=blk_)[-\d]+"),
    MaskingInstruction(mask_with="NUM", pattern=r"((?<=[^A-Za-z0-9])|^)([\-\+]?\d+)((?=[^A-Za-z0-9])|$)")
]

miner = TemplateMiner(config=config)
cluster_stats = {}

with open("HDFS_2k.log", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line: continue
        
        result = miner.add_log_message(line)
        cid = result["cluster_id"]
        
        if cid not in cluster_stats:
            cluster_stats[cid] = {
                "template": result["template_mined"],
                "count": 0,
                "example": line 
            }
        cluster_stats[cid]["count"] += 1

# 1 kez görülen (tek seferlik) logları ayır
rare_clusters = {cid: data for cid, data in cluster_stats.items() if data["count"] == 1}

# İstenen 1: Template sayısı ve dağılım özeti
print("--- TEMPLATE DAĞILIM ÖZETİ ---")
print(f"Üretilen Toplam Benzersiz Template: {len(cluster_stats)}")
print(f"Tek Seferlik (Beklenmedik) Template: {len(rare_clusters)}\n")

# İstenen 2: Beklenmedik/tek seferlik log satırları
print("--- BEKLENMEDİK / TEK SEFERLİK LOGLAR ---")
for cid, data in rare_clusters.items():
    # Terminal taşmasını engellemek için kısaltma
    template = data['template'][:120] + "..." if len(data['template']) > 120 else data['template']
    orijinal_log = data['example'][:120] + "..." if len(data['example']) > 120 else data['example']
    
    print(f"ID       : {cid}")
    print(f"Template : {template}")
    print(f"Log      : {orijinal_log}")
    print("-" * 70)
