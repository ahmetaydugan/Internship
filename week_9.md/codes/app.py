import streamlit as st
import pandas as pd
from log_utils import veriyi_yukle # log_utils modülünü ekledik

# Sayfa yapılandırması
st.set_page_config(page_title="Log Anomali Tespiti", layout="wide")

st.title("Hafta 6-7: Yapılandırılmış Loglar ve Anomali Sonuçları")
st.write("Ayrıştırılan log verileri ve anomali tespit sonuçları aşağıda listelenmektedir.")

# Veriyi önbelleğe alarak sayfa her yenilendiğinde tekrar okunmasını engelliyoruz
@st.cache_data
def cache_veriyi_yukle():
    # json dosyasını doğrudan pd.read_json yerine güncellenmiş fonksiyon ile okuyoruz
    return veriyi_yukle("structured_logs.json")

try:
    # Fonksiyon ismini değiştirdik
    df = cache_veriyi_yukle()
    
    if df.empty:
         st.error("Hata: 'structured_logs.json' dosyası bulunamadı veya okunamadı.")
    else:
        # Eğer verinde anomali durumunu tutan bir sütun varsa (örneğin 'is_anomaly' veya 'anomaly')
        anomali_sutunlari = [col for col in df.columns if 'anomal' in col.lower()]
        
        if anomali_sutunlari:
            hedef_sutun = anomali_sutunlari[0]
            sadece_anomaliler = st.checkbox("Sadece tespit edilen anomalileri göster")
            
            if sadece_anomaliler:
                df = df[df[hedef_sutun] == True]
                
        # Tabloyu ekrana bastırma
        st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Veri yüklenirken bir hata oluştu: {e}")
