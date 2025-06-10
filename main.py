from core.browser_setup import setup_driver
from core.browser_actions import TuikBrowserActions
from core.api_scraper import fetch_bulletin_list  # <-- YENİ İMPORT
from data_processing.file_handler import clean_directory
from data_processing.excel_processor import process_and_merge_all_excels
from config import settings
import time


def main():
    """Projenin ana, API-destekli ve en güvenilir iş akışını yönetir."""
    start_time = time.time()
    print("===== TÜİK Veri İndirme Otomasyonu Başlatıldı =====")

    clean_directory(settings.DOWNLOADS_DIR)
    clean_directory(settings.OUTPUT_DIR)

    # Adım 1: API aracılığıyla bülten listesini hızlıca çek
    bulletin_list = fetch_bulletin_list()

    if not bulletin_list:
        print("İşlem yapılacak bülten bulunamadı, program sonlandırılıyor.")
        return

    driver = None
    try:
        # Adım 2: Sadece indirme işlemleri için Selenium'u başlat
        driver = setup_driver()
        actions = TuikBrowserActions(driver)

        # Adım 3: Her bir bülteni gez ve dosyaları indir
        for bulletin in bulletin_list:
            bulletin_name = bulletin['name']
            bulletin_url = bulletin['url']

            print(f"\n{'=' * 20} BÜLTEN İŞLENİYOR: {bulletin_name} {'=' * 20}")
            driver.get(bulletin_url)
            actions.download_files_from_bulletin_page(bulletin_name)

        print("\n\n===== Tüm Bültenlerin İndirilmesi Tamamlandı! =====")

        # Adım 4: İndirilen tüm Excel dosyalarını işle ve birleştir
        process_and_merge_all_excels()

    except Exception as e:
        print(f"\n!!!!!! PROGRAM DURDURULDU, KRİTİK BİR HATA OLUŞTU: {e}")
    finally:
        if driver:
            driver.quit()
            print("\nTarayıcı kapatıldı.")

    end_time = time.time()
    print(f"\n===== Görev Tamamlandı! Toplam Süre: {end_time - start_time:.2f} saniye =====")


if __name__ == "__main__":
    main()