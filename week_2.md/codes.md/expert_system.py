import json
import os

def parse_log(log):
    """Farklı log formatlarını normalize eder (Hem v1 hem v2'yi anlar)."""
    # Servis adı
    service = log.get("service") or log.get("app_component")
    
    # Durum
    status = log.get("status") or log.get("level")
    status = status.lower()
    
    # Hata kodu
    raw_code = log.get("code") or log.get("err_code")
    if isinstance(raw_code, str):
        code = int(raw_code.split("_")[-1]) 
    else:
        code = raw_code
        
    # Gecikme süresi
    raw_latency = log.get("latency_ms") or log.get("response_time")
    if isinstance(raw_latency, str):
        latency = float(raw_latency.replace("s", "")) * 1000 
    else:
        latency = raw_latency
        
    # Mesaj
    message = log.get("message") or log.get("msg")
    
    return service, status, code, latency, message.lower()


def expert_system(log_entry):
    """Log verisine göre aksiyon kararı veren uzman sistem."""
    service, status, code, latency, message = parse_log(log_entry)
    
    if code in [400, 401, 429]:
        return "ignore"
        
    if status in ["error", "critical", "fatal"]:
        if "node down" in message or "exhausted" in message:
            return "restart"
        elif code in [500, 503]:
            return "escalate"
            
    if latency > 1000:
        return "watch"
        
    if status in ["warning", "warn"]:
        return "watch"
        
    return "ignore"


# --- ANA ÇALIŞTIRMA BLOKU ---

dosya_1 = "ariza_kayitlari_v1.json"
dosya_2 = "ariza_kayitlari_v2.json"
tum_loglar = []

# 1. Dosyayı okuyup listeye ekliyoruz
if os.path.exists(dosya_1):
    with open(dosya_1, "r", encoding="utf-8") as file:
        tum_loglar.extend(json.load(file))
else:
    print(f"Uyarı: {dosya_1} bulunamadı.")

# 2. Dosyayı okuyup aynı listeye ekliyoruz (Verileri birleştiriyoruz!)
if os.path.exists(dosya_2):
    with open(dosya_2, "r", encoding="utf-8") as file:
        tum_loglar.extend(json.load(file))
else:
    print(f"Uyarı: {dosya_2} bulunamadı.")

# Birleştirilmiş verileri analiz edip ekrana basıyoruz
if tum_loglar:
    print("\n--- BİRLEŞTİRİLMİŞ (V1 + V2) ANALİZ RAPORU ---")
    print("-" * 65)
    
    for log in tum_loglar:
        aksiyon = expert_system(log)
        servis = str(log.get("service") or log.get("app_component") or "Bilinmeyen")
        mesaj = str(log.get("message") or log.get("msg") or "")
        
        print(f"Servis: {servis.ljust(20)} | Karar: {aksiyon.upper().ljust(8)} | Hata: {mesaj}")
else:
    print("İncelenecek log kaydı bulunamadı. Lütfen JSON dosyalarını kontrol et.")