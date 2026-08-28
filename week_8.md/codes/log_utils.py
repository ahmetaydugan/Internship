import pandas as pd

def veriyi_yukle(dosya_yolu="structured_logs.json"):
    """JSON dosyasını okur, zaman damgası ve anomali etiketlerini oluşturur."""
    try:
        df = pd.read_json(dosya_yolu)
        
        # Zaman damgası ve anomali tespiti
        df['timestamp'] = pd.to_datetime(df['raw_log'].str.slice(0, 13), format='%y%m%d %H%M%S', errors='coerce')
        df['anomaly'] = df['raw_log'].str.contains('WARN|ERROR', case=False, na=False)
        
        return df
    except FileNotFoundError:
        print(f"Hata: '{dosya_yolu}' bulunamadı.")
        return pd.DataFrame() # Hata durumunda uygulamanın çökmemesi için boş DataFrame dönüyoruz

def cluster_stats(df):
    """
    Log verisetine ait genel istatistikleri hesaplar.
    Dashboard ve raporlamalarda tekrar eden hesaplama mantığını tekilleştirir.
    """
    if df.empty:
        return {"toplam_log": 0, "anomali_sayisi": 0, "anomali_orani": 0.0, "template_sayisi": 0}
    
    toplam_log = len(df)
    anomali_sayisi = df['anomaly'].sum()
    anomali_orani = (anomali_sayisi / toplam_log) * 100 if toplam_log > 0 else 0
    template_sayisi = df['template_id'].nunique()
    
    return {
        "toplam_log": toplam_log,
        "anomali_sayisi": anomali_sayisi,
        "anomali_orani": anomali_orani,
        "template_sayisi": template_sayisi
    }
