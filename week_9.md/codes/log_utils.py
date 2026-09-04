import pandas as pd
import os

def veriyi_yukle(dosya_adi="structured_logs.json"):
    """JSON dosyasını okur ve Hafta 7 mantığıyla anomali tespiti yapar."""
    # log_utils.py dosyasının bulunduğu klasörün yolunu al
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # JSON dosyasının tam yolunu oluştur
    dosya_yolu = os.path.join(BASE_DIR, dosya_adi)

    try:
        df = pd.read_json(dosya_yolu)
        df['timestamp'] = pd.to_datetime(df['raw_log'].str.slice(0, 13), format='%y%m%d %H%M%S', errors='coerce')
        
        gecerli_df = df.dropna(subset=['timestamp']).copy()
        
        # --- HAFTA 7 MANTIĞI: unstack(fill_value=0) ---
        gecerli_df.set_index('timestamp', inplace=True)
        time_bins = gecerli_df.groupby([pd.Grouper(freq='1min'), 'template_id']).size().unstack(fill_value=0)
        
        anormal_zamanlar = []
        
        for template_id in time_bins.columns:
            freq_series = time_bins[template_id]
            mean_val = freq_series.mean()
            std_val = freq_series.std()
            
            if pd.isna(std_val):
                std_val = 0.0
                
            threshold = mean_val + (2 * std_val)
            outliers = freq_series[(freq_series > threshold) & (freq_series > 0)]
            
            for timestamp, _ in outliers.items():
                anormal_zamanlar.append({
                    'time_bin': timestamp, 
                    'template_id': template_id, 
                    'anomaly': True
                })
        
        anomali_df = pd.DataFrame(anormal_zamanlar)
        
        df['time_bin'] = df['timestamp'].dt.floor('min')
        
        if not anomali_df.empty:
            df = df.merge(anomali_df, on=['time_bin', 'template_id'], how='left')
            df['anomaly'] = df['anomaly'].fillna(False)
        else:
            df['anomaly'] = False
            
        df.drop(columns=['time_bin'], inplace=True)
        
        return df
    
    except FileNotFoundError:
        print(f"Hata: '{dosya_yolu}' bulunamadı.")
        return pd.DataFrame()

def cluster_stats(df):
    # ... (Bu kısım aynı kalacak) ...
    if df.empty:
        return {"toplam_log": 0, "anomali_sayisi": 0, "anomali_orani": 0.0, "template_sayisi": 0, "anormal_dakika": 0}
    
    toplam_log = len(df)
    anomali_sayisi = df['anomaly'].sum()
    template_sayisi = df['template_id'].nunique()
    
    # Anormal olan log satırlarının kaç farklı 'dakika' içinde gerçekleştiğini sayıyoruz
    anormal_df = df[df['anomaly'] == True]
    if not anormal_df.empty:
        anormal_dakika = anormal_df['timestamp'].dt.floor('min').nunique()
    else:
        anormal_dakika = 0
    
    # Anomali oranını anormal dakika / toplam log üzerinden hesaplıyoruz
    anomali_orani = (anormal_dakika / toplam_log) * 100 if toplam_log > 0 else 0
    
    return {
        "toplam_log": toplam_log,
        "anomali_sayisi": anomali_sayisi,
        "anomali_orani": anomali_orani,
        "template_sayisi": template_sayisi,
        "anormal_dakika": anormal_dakika
    }
