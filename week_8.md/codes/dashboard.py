import streamlit as st
import pandas as pd

st.set_page_config(page_title="Log Analiz Dashboard", layout="wide")

st.title("Gün 2: Log Anomali Dashboard")
st.markdown("HDFS loglarının Drain3 ile ayrıştırılması ve anomali tespiti sonuçlarının görselleştirilmesi.")

@st.cache_data
def veriyi_yukle():
    df = pd.read_json("structured_logs.json")
    
    # 1. ZAMAN DAMGASI ÇIKARTMA
    df['timestamp'] = pd.to_datetime(df['raw_log'].str.slice(0, 13), format='%y%m%d %H%M%S', errors='coerce')
    
    # 2. ANOMALİ TESPİTİ (WARN/ERROR)
    df['anomaly'] = df['raw_log'].str.contains('WARN|ERROR', case=False, na=False)
    
    return df

try:
    df = veriyi_yukle()

    # --- BÖLÜM 1: ANA ÖZET KARTLARI ---
    st.header("Genel Özet")
    col1, col2, col3 = st.columns(3)
    
    toplam_log = len(df)
    anomali_sayisi = df['anomaly'].sum()
    anomali_orani = (anomali_sayisi / toplam_log) * 100 if toplam_log > 0 else 0

    col1.metric("Toplam Log Satırı", f"{toplam_log:,}")
    col2.metric("Tespit Edilen Anomali", f"{anomali_sayisi:,}", delta="Dikkat Gerektirir", delta_color="inverse")
    col3.metric("Anomali Oranı", f"%{anomali_orani:.2f}")

    st.divider()

    # --- BÖLÜM 2: GRAFİKLER ---
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Şablon (Template) Dağılım Grafiği")
        template_dagilimi = df['template_id'].value_counts()
        st.bar_chart(template_dagilimi)

    with col_right:
        st.subheader("Zaman İçinde Log Sıklığı (Trend)")
        if not df['timestamp'].isnull().all():
            zaman_trendi = df.set_index('timestamp').resample('10min').size()
            st.line_chart(zaman_trendi)
        else:
            st.warning("Zaman damgası ayrıştırılamadı.")

    st.divider()

    # --- BÖLÜM 3: HAFTA 6 İNCELEMESİ ---
    st.header("Hafta 6 İncelemesi: Over-clustering Bulgusu")
    st.markdown("""
    Drain3 algoritmasının benzerlik eşiği (sim_th) optimize edilmeden önce loglar **17 farklı şablona** bölünmekteydi. 
    Yapılan ince ayarlar sayesinde, anlamsal olarak birbirinin aynısı olan yapılar birleştirilerek şablon sayısı **14'e** düşürülmüş ve analiz kalitesi artırılmıştır.
    """)

    oc_col1, oc_col2 = st.columns(2)
    with oc_col1:
        st.metric(label="Varsayılan Parametreler", value="17 Şablon", delta="Aşırı Bölünmüş (Over-clustered)", delta_color="inverse")
    with oc_col2:
        st.metric(label="Optimize Edilmiş Parametreler", value="14 Şablon", delta="-3 Şablon (İyileştirilmiş)", delta_color="normal")

    # --- BÖLÜM 4: DETAYLI VERİ TABLOSU ---
    st.subheader("Ham Veri ve Şablonlar")
    sadece_anomaliler = st.checkbox("Sadece tespit edilen anomalileri göster")
    
    gosterilecek_df = df[df['anomaly'] == True] if sadece_anomaliler else df
    st.dataframe(gosterilecek_df[['timestamp', 'template_id', 'anomaly', 'template', 'raw_log']], use_container_width=True)

except FileNotFoundError:
    st.error("Hata: 'structured_logs.json' dosyası bulunamadı. Lütfen dosyanın uygulamanın çalıştığı dizinde olduğundan emin ol.")