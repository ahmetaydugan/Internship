import streamlit as st
import pandas as pd

# Sayfa yapılandırması
st.set_page_config(page_title="Log Anomali Tespiti", layout="wide")

st.title("Hafta 6-7: Yapılandırılmış Loglar ve Anomali Sonuçları")
st.write("Ayrıştırılan log verileri ve anomali tespit sonuçları aşağıda listelenmektedir.")

# Veriyi önbelleğe alarak sayfa her yenilendiğinde tekrar okunmasını engelliyoruz
@st.cache_data
def veriyi_yukle():
    # JSON dosyasını okuma. 
    # Not: Eğer dosyan JSON Lines formatındaysa parametreye lines=True eklemelisin.
    return pd.read_json("structured_logs.json")

try:
    df = veriyi_yukle()
    
    # Eğer verinde anomali durumunu tutan bir sütun varsa (örneğin 'is_anomaly' veya 'anomaly')
    anomali_sutunlari = [col for col in df.columns if 'anomal' in col.lower()]
    
    if anomali_sutunlari:
        hedef_sutun = anomali_sutunlari[0]
        sadece_anomaliler = st.checkbox("Sadece tespit edilen anomalileri göster")
        
        if sadece_anomaliler:
            df = df[df[hedef_sutun] == True]
            
    # Tabloyu ekrana bastırma
    st.dataframe(df, use_container_width=True)

except FileNotFoundError:
    st.error("Hata: 'structured_logs.json' dosyası bulunamadı. Lütfen dosyanın uygulamanın çalıştığı dizinde olduğundan emin ol.")
except Exception as e:
    st.error(f"Veri yüklenirken bir hata oluştu: {e}\n(Eğer JSON her satırda ayrı bir obje barındırıyorsa `pd.read_json('structured_logs.json', lines=True)` kullanmayı dene.)")