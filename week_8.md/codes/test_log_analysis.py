import unittest
import pandas as pd
from log_utils import veriyi_yukle, cluster_stats

class TestLogAnalysis(unittest.TestCase):
    
    def setUp(self):
        # Bu metod her test fonksiyonundan önce otomatik çalışır.
        # Testlerde kullanmak üzere veriyi yüklüyoruz.
        self.df = veriyi_yukle("structured_logs.json")

    def test_json_dogru_okundu_mu(self):
        """JSON dosyasının doğru okunup DataFrame'e çevrildiğini kontrol eder."""
        self.assertFalse(self.df.empty, "Test Başarısız: Veriseti boş. 'structured_logs.json' okunamadı.")
        self.assertIn('template_id', self.df.columns, "Sütun Eksik: 'template_id' bulunamadı.")
        self.assertIn('anomaly', self.df.columns, "Sütun Eksik: 'anomaly' bulunamadı.")

    def test_template_sayisi_sifir_degil(self):
        """Template (Şablon) sayısının sıfırdan büyük olduğunu teyit eder."""
        istatistikler = cluster_stats(self.df)
        self.assertGreater(istatistikler['template_sayisi'], 0, "Hata: Template sayısı 0 olamaz, kümeleme (clustering) başarısız.")

    def test_cluster_stats_mantigi(self):
        """cluster_stats fonksiyonunun matematiksel olarak mantıklı değerler döndürdüğünü sınar."""
        istatistikler = cluster_stats(self.df)
        
        # Anomali oranı %0 ile %100 arasında olmalıdır
        self.assertGreaterEqual(istatistikler['anomali_orani'], 0.0)
        self.assertLessEqual(istatistikler['anomali_orani'], 100.0)
        
        # Anomali sayısı toplam log sayısından büyük olamaz
        self.assertLessEqual(istatistikler['anomali_sayisi'], istatistikler['toplam_log'])

if __name__ == '__main__':
    unittest.main()
