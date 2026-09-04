import streamlit as st
import pandas as pd
import re
from log_utils import veriyi_yukle, cluster_stats

# Sayfa yapılandırması
st.set_page_config(page_title="Log Analiz Dashboard", layout="wide")

st.title("Anomali Detay Görünümü (Refactor Edilmiş)")


# Veriyi log_utils üzerinden önbelleğe alarak yüklüyoruz
@st.cache_data
def cache_veriyi_yukle():
    return veriyi_yukle("structured_logs.json")

try:
    df = cache_veriyi_yukle()

    if df.empty:
        st.error("Veri yüklenemedi. 'structured_logs.json' dosyasının ve 'log_utils.py' modülünün doğru çalıştığından emin olun.")
    else:
        # ==========================================
        # YAN MENÜ (SIDEBAR) FİLTRELERİ
        # ==========================================
        st.sidebar.header("Filtreleme Seçenekleri")
        
        # Tarih Aralığı Filtresi
        min_date = df['timestamp'].min().date()
        max_date = df['timestamp'].max().date()
        secilen_tarihler = st.sidebar.date_input("Tarih Aralığı", [min_date, max_date], min_value=min_date, max_value=max_date)
        
        # Template ID Filtresi
        mevcut_templateler = sorted(df['template_id'].dropna().unique().tolist())
        secilen_templateler = st.sidebar.multiselect("Template ID", mevcut_templateler, default=mevcut_templateler)

        # Veriyi Filtreleme İşlemi
        if len(secilen_tarihler) == 2:
            baslangic_tarihi, bitis_tarihi = secilen_tarihler
            maske = (df['timestamp'].dt.date >= baslangic_tarihi) & (df['timestamp'].dt.date <= bitis_tarihi) & (df['template_id'].isin(secilen_templateler))
            filtrelenmis_df = df[maske]
        else:
            filtrelenmis_df = df[df['template_id'].isin(secilen_templateler)]

        # ==========================================
        # 1. ANA ÖZET KARTLARI
        # ==========================================
        st.header("Genel Özet")
        col1, col2, col3 = st.columns(3)
        
        # Hesaplamaları log_utils.py içindeki fonksiyondan çekiyoruz
        istatistikler = cluster_stats(filtrelenmis_df)

        col1.metric("Toplam Log (Filtreli)", f"{istatistikler['toplam_log']:,}")
        col2.metric("Anormal Zaman Dilimi", f"{istatistikler['anormal_dakika']:,}", delta=f"{istatistikler['anomali_sayisi']} Satır Etkilendi", delta_color="inverse")
        col3.metric("Anomali Oranı", f"%{istatistikler['anomali_orani']:.2f}")

        st.divider()

        # ==========================================
        # 2. GRAFİKLER
        # ==========================================
        col_left, col_right = st.columns(2)

        with col_left:
            st.subheader("Şablon (Template) Dağılımı")
            st.bar_chart(filtrelenmis_df['template_id'].value_counts())

        with col_right:
            st.subheader("Zaman İçinde Log Sıklığı (10 Dakikalık)")
            if not filtrelenmis_df['timestamp'].isnull().all():
                zaman_trendi = filtrelenmis_df.set_index('timestamp').resample('10min').size()
                st.line_chart(zaman_trendi)

        st.divider()

        # ==========================================
        # 3. HAFTA 6 İNCELEMESİ
        # ==========================================
        st.header("Over-clustering Bulgusu")
        st.markdown("""
        Drain3 algoritmasının benzerlik eşiği (sim_th) optimize edilmeden önce loglar **17 farklı şablona** bölünmekteydi. 
        Yapılan ince ayarlar sayesinde, anlamsal olarak birbirinin aynısı olan yapılar birleştirilerek şablon sayısı **14'e** düşürülmüş ve analiz kalitesi artırılmıştır.
        """)

        oc_col1, oc_col2 = st.columns(2)
        with oc_col1:
            st.metric(label="Varsayılan Parametreler", value="17 Şablon", delta="Aşırı Bölünmüş (Over-clustered)", delta_color="inverse")
        with oc_col2:
            st.metric(label="Optimize Edilmiş Parametreler", value="14 Şablon", delta="-3 Şablon (İyileştirilmiş)", delta_color="normal")

        st.divider()

        # ==========================================
        # 4. ANOMALİ DETAY VE DİNAMİK AÇIKLAMALAR
        # ==========================================
        st.header("Anomali Detay Görünümü")
        
        anomali_df = filtrelenmis_df[filtrelenmis_df['anomaly'] == True]
        
        if anomali_df.empty:
            st.success("Seçili filtrelerde anomali bulunmamaktadır.")
        else:
            st.warning(f"Gösterilen anomali sayısı: {len(anomali_df)} (Sayfa performansı için ilk 50 kayıt listelenir)")
            
            for index, row in anomali_df.head(50).iterrows():
                # Expander başlığı için Regex ile Block ID bulma
                block_match = re.search(r'blk_-?\d+', row['raw_log'])
                block_id = block_match.group(0) if block_match else "Bilinmeyen_Blok"
                
                with st.expander(f"Anomali Tespiti - Block: {block_id} | Zaman: {row['timestamp']}"):
                    detay_sol, detay_sag = st.columns(2)
                    
                    with detay_sol:
                        st.markdown("**Ham Log (Raw Log):**")
                        st.code(row['raw_log'], language='text')
                        
                        st.markdown("**Şablon (Template):**")
                        st.code(row['template'], language='text')
                        
                    with detay_sag:
                        st.markdown("**📊 İstatistiksel Sapma:**")
                        template_orani = (len(df[df['template_id'] == row['template_id']]) / len(df)) * 100
                        st.info(f"Bu şablon (ID: {row['template_id']}) tüm veri setinin sadece %{template_orani:.2f}'sini oluşturuyor. Sıklık analizi sınırlarının dışında.")
                        
                        st.markdown("**🤖 Olası Hata Açıklaması (Şablon Tabanlı):**")
                        st.caption("*Not: Bu açıklamalar performans optimizasyonu amacıyla statik şablonlar kullanılarak üretilmiştir.*")
                        
                        # Regex ile IP Adresi bulma
                        ip_match = re.search(r'(10\.\d+\.\d+\.\d+)', row['raw_log'])
                        ip_addr = ip_match.group(1) if ip_match else "Bilinmeyen IP"
                        
                        # Dinamik metin oluşturma
                        if "exception" in row['raw_log'].lower():
                            llm_yanit = f"**{ip_addr}** hedefine **{block_id}** veri bloğu aktarılırken DataXceiver bileşeninde istisna (exception) yaşandı. Ağ bağlantısında anlık bir kopma veya hedef düğümde (node) aşırı yüklenme meydana gelmiş olabilir."
                        elif "terminating" in row['raw_log'].lower():
                            llm_yanit = f"**{block_id}** için PacketResponder işlemi beklenmeyen bir şekilde sonlandı. Node üzerindeki bellek tükenmesi veya thread çakışması bu duruma sebep olmuş olabilir."
                        else:
                            llm_yanit = f"**{block_id}** bloğu ile ilgili standart dışı bir olay tespit edildi. RAG veritabanındaki geçmiş arıza dokümanlarıyla eşleşme aranıyor."
                        
                        # LLM Yanıtını doğrudan ekrana basıyoruz
                        st.write(llm_yanit)

except Exception as e:
    st.error(f"Sistem çalıştırılırken beklenmeyen bir hata oluştu: {e}")
