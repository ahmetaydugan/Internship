import json
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder

# --- 1. DOSYALARI OKUMA ---
# JSON dosyalarını okuyoruz[cite: 1, 2]
with open("ariza_kayitlari_v2.json", "r", encoding="utf-8") as f1:
    source_1 = json.load(f1)
    
with open("ariza_kayitlari_v1.json", "r", encoding="utf-8") as f2:
    source_2 = json.load(f2)

# --- 2. YARDIMCI FONKSİYON ---
def egitim_icin_karar_ver(service, code, latency, msg):
    """Geçmiş verileri etiketlemek için basit kurallarımız"""
    if code >= 500 and latency >= 4.0: return "escalate"
    if service == "gateway" and code >= 500: return "escalate"
    if service == "auth" and "ldap" in msg: return "escalate"
    if "exhausted" in msg or "deadlock" in msg: return "restart"
    if service == "cache" and code >= 500: return "restart"
    if code in [400, 401, 429] or latency >= 0.5: return "watch"
    return "ignore"

parsed_data = []

# --- 3. V2 LOGLARINI DÜZENLEME ---
for log in source_1:
    # Servis adlarını sadeleştir[cite: 1]
    srv = log["app_component"].replace("authentication_v2", "auth").replace("payment_engine", "payment").replace("database_cluster", "db").replace("cache_layer", "cache")
    
    # Seviyeyi (level) küçük harfe çevir[cite: 1]
    seviye = log["level"].lower()
    
    # Hata kodunu sayıya çevir[cite: 1]
    code = int(log["err_code"].split("_")[1])
    
    # Gecikmeyi saniyeye (küsuratlı sayı) çevir[cite: 1]
    latency = float(log["response_time"].replace("s", ""))
    
    msg = log["msg"].lower()
    action = egitim_icin_karar_ver(srv, code, latency, msg)
    
    parsed_data.append({"servis": srv, "seviye": seviye, "hata_kodu": code, "gecikme": latency, "hedef_aksiyon": action})

# --- 4. V1 LOGLARINI DÜZENLEME ---
for log in source_2:
    # Servis adlarını sadeleştir[cite: 2]
    srv = log["service"].replace("api-gateway", "gateway")
    
    # Statüyü (status) V2 ile aynı anlama gelecek şekilde çevir[cite: 2]
    seviye = log["status"].lower().replace("ok", "info").replace("warning", "warn")
    
    # Hata kodu zaten sayı[cite: 2]
    code = int(log["code"])
    
    # Milisaniyeyi saniyeye çevir[cite: 2]
    latency = log["latency_ms"] / 1000.0
    
    msg = log["message"].lower()
    action = egitim_icin_karar_ver(srv, code, latency, msg)
    
    parsed_data.append({"servis": srv, "seviye": seviye, "hata_kodu": code, "gecikme": latency, "hedef_aksiyon": action})

# --- 5. VERİYİ TABLOYA ÇEVİRME VE SAYISALLAŞTIRMA ---
df = pd.DataFrame(parsed_data)

# Servis adlarını numaralandır
servis_encoder = LabelEncoder()
df["servis_kodu"] = servis_encoder.fit_transform(df["servis"]) 

# Seviye (info, error, warn vs.) bilgilerini numaralandır
seviye_encoder = LabelEncoder()
df["seviye_kodu"] = seviye_encoder.fit_transform(df["seviye"])

# --- 6. MAKİNEYE ÖĞRETME (EĞİTİM) ---
# Artık 3 değil, 'seviye_kodu' dahil 4 sütun veriyoruz!
X = df[["servis_kodu", "seviye_kodu", "hata_kodu", "gecikme"]]
y = df["hedef_aksiyon"]

model = DecisionTreeClassifier(random_state=42)
model.fit(X, y)

print("✅ Model, servis, seviye, hata kodu ve gecikme verileriyle başarıyla eğitildi!\n")

# --- 7. YENİ BİR OLAY TESTİ ---
test_servis = "db"
test_seviye = "error"
test_hata_kodu = 500
test_gecikme = 6.5

yeni_log = pd.DataFrame({
    "servis_kodu": [servis_encoder.transform([test_servis])[0]],
    "seviye_kodu": [seviye_encoder.transform([test_seviye])[0]], # Seviyeyi de sayıya çevirip ekledik
    "hata_kodu": [test_hata_kodu],
    "gecikme": [test_gecikme]
})

tahmin = model.predict(yeni_log)

print("--- CANLI TEST ---")
print(f"Olay: {test_servis} servisi, {test_seviye} seviyesi, {test_hata_kodu} hatası, {test_gecikme}s gecikme.")
print(f"Makinenin Kararı: {tahmin[0].upper()}")