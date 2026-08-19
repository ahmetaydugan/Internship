import os
import time
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from drain3 import TemplateMiner
from drain3.template_miner_config import TemplateMinerConfig
from drain3.masking import MaskingInstruction
from groq import Groq

# --- 1. AYARLAR VE YAPILANDIRMA ---
load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

config = TemplateMinerConfig()
config.masking_instructions = [
    MaskingInstruction(mask_with="IP", pattern=r"((?<=[^A-Za-z0-9])|^)(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})((?=[^A-Za-z0-9])|$)"),
    MaskingInstruction(mask_with="BLOCK", pattern=r"(?<=blk_)[-\d]+"),
    MaskingInstruction(mask_with="NUM", pattern=r"((?<=[^A-Za-z0-9])|^)([\-\+]?\d+)((?=[^A-Za-z0-9])|$)")
]
miner = TemplateMiner(config=config)

# --- 2. YARDIMCI FONKSİYONLAR ---
def extract_timestamp(line):
    try:
        parts = line.split()
        date_str = parts[0] + " " + parts[1]
        return datetime.strptime(date_str, "%y%m%d %H%M%S")
    except Exception:
        return None

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
                'Esik_Degeri': round(threshold, 3)
            })
    return pd.DataFrame(anomalies)

def analyze_anomaly_with_llm(template_text, frekans, esik):
    prompt = f"""
    Sen bir sistem log analisti uzmanısın. Aşağıdaki HDFS (Hadoop) log şablonu belirtilen dakikada normal eşik değerinin çok üzerine çıktı.
    
    Log Şablonu: {template_text}
    O Anki Frekans: {frekans}
    Normal Eşik Değeri: {esik}
    
    Lütfen bu ani artışın teknik olarak ne anlama gelebileceğini en fazla 2 cümlelik kısa ve öz bir Türkçe açıklamayla belirt.
    """
    start_time = time.time()
    
    response = client.chat.completions.create(
        model="qwen/qwen3.6-27b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=1024 # Limit artırıldı
    )
    
    latency = time.time() - start_time
    llm_output = response.choices[0].message.content.strip()
    
    # <think> bloklarını filtrele
    if "</think>" in llm_output:
        llm_output = llm_output.split("</think>")[-1].strip()
        
    p_tokens = response.usage.prompt_tokens
    c_tokens = response.usage.completion_tokens
    
    return llm_output, latency, p_tokens, c_tokens


# --- 3. ANA ÇALIŞMA AKIŞI (PIPELINE) ---
if __name__ == "__main__":
    log_records = []

    print("1/4 - Loglar okunuyor ve Drain3 ile ayrıştırılıyor...")
    with open("HDFS_2k.log", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line: continue
            
            timestamp = extract_timestamp(line)
            if not timestamp: continue
                
            result = miner.add_log_message(line)
            log_records.append({
                "timestamp": timestamp,
                "cluster_id": result["cluster_id"]
            })

    print("2/4 - Zaman pencereleri hesaplanıyor...")
    df = pd.DataFrame(log_records)
    df.set_index("timestamp", inplace=True)
    time_bins = df.groupby([pd.Grouper(freq='1min'), 'cluster_id']).size().unstack(fill_value=0)

    print("3/4 - İstatistiksel anomaliler tespit ediliyor...")
    detected_anomalies = detect_anomalies(time_bins, std_multiplier=2)

    print(f"4/4 - Kritik anomaliler LLM'e (Groq API) gönderiliyor...\n")
    print("="*75)
    
    if not detected_anomalies.empty:
        detected_anomalies['Sapma'] = detected_anomalies['Frekans'] - detected_anomalies['Esik_Degeri']
        top_anomalies = detected_anomalies.sort_values(by='Sapma', ascending=False).head(5)
        
        for index, row in top_anomalies.iterrows():
            t_id = row['Template_ID']
            cluster = next((c for c in miner.drain.clusters if c.cluster_id == t_id), None)
            template_text = cluster.get_template() if cluster else "Bilinmeyen Şablon"
            
            try:
                llm_out, lat, pt, ct = analyze_anomaly_with_llm(template_text, row['Frekans'], row['Esik_Degeri'])
                
                # Doğrudan terminale yazdır
                print(f"--- Anomali Zamanı: {row['Zaman']} | Template ID: {t_id} ---")
                print(f"Frekans: {row['Frekans']} (Eşik: {row['Esik_Degeri']})")
                print(f"Şablon: {template_text}\n")
                print(f" Yapay Zeka Analizi:\n{llm_out}\n")
                print(f"[Süre: {lat:.2f}s |  Girdi: {pt} |  Çıktı: {ct} token]")
                print("-" * 75)
                
            except Exception as e:
                print(f"--- Template ID {t_id} analiz edilirken API Hatası: {e} ---")
                print("-" * 75)

        print("\nSüreç başarıyla tamamlandı!")
    else:
        print("Sistemde herhangi bir istatistiksel anomali bulunamadı.")
