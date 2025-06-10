import time
from core.browser_setup import setup_driver
from core.api_scraper import fetch_bulletin_list


def get_raw_html_of_bulletin_page():
    """
    SADECE bir bülten sayfasının HTML'ini almak için tasarlanmış,
    hiçbir arama veya tıklama yapmayan, garantili bir script.
    """
    print("===== HAM HTML ALMA SCRİPT'İ BAŞLATILDI =====")

    # Adım 1: Sadece bir URL almak için API'yi kullan
    bulletin_list = fetch_bulletin_list()
    if not bulletin_list:
        print("API'den bülten listesi alınamadı. Script durduruluyor.")
        return

    target_bulletin = bulletin_list[0]
    print(f"Hedef bültenin URL'i alındı: {target_bulletin['name']}")

    driver = None
    try:
        # Adım 2: Tarayıcıyı başlat ve sayfaya git
        driver = setup_driver()
        driver.get(target_bulletin['url'])
        print(f"Sayfaya gidildi: {target_bulletin['url']}")

        # Adım 3: EN KRİTİK ADIM - HİÇBİR ŞEY YAPMADAN BEKLEME
        # Sayfadaki tüm pop-up'ların, anketlerin ve diğer script'lerin
        # yüklenmesi için 15 saniye bekleniyor.
        print("\nSayfanın tam olarak yüklenmesi için 15 saniye bekleniyor...")
        time.sleep(15)
        print("Bekleme tamamlandı.")

        # Adım 4: Sayfanın o anki HTML'ini al ve kaydet
        print("Sayfa HTML'i alınıyor ve dosyaya kaydediliyor...")
        filename = "bulletin_page_source.html"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(driver.page_source)

        print(f"\nİŞLEM BAŞARILI! Sayfa HTML'i '{filename}' dosyasına kaydedildi.")
        print("Lütfen bu dosyanın içeriğini analiz için paylaşın.")

    except Exception as e:
        print(f"\n!!!!!! BİR HATA OLUŞTU: {e}")
    finally:
        # Adım 5: Tarayıcıyı kapat
        if driver:
            driver.quit()
            print("\nTarayıcı kapatıldı.")


if __name__ == "__main__":
    get_raw_html_of_bulletin_page()