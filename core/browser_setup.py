from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from config import settings


def setup_driver():
    """
    Selenium WebDriver'ı yapılandırılmış seçeneklerle kurar ve başlatır.
    """
    print("Selenium WebDriver hazırlanıyor...")

    chrome_options = webdriver.ChromeOptions()

    # Chrome tercihlerini (preferences) ayarlamak için bir sözlük oluşturuyoruz.
    prefs = {
        "download.default_directory": str(settings.DOWNLOADS_DIR),  # İndirme yolunu belirt
        "download.prompt_for_download": False,  # Her indirme için onay isteme
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,  # Güvenli taramayı etkinleştir

        # --- YENİ VE EN ÖNEMLİ AYAR ---
        # "Birden çok dosya indirme" iznini otomatik olarak vermek için.
        # Bu ayar, Chrome'un gösterdiği "İzin ver / Engelle" penceresini tamamen engeller.
        "profile.default_content_setting_values.automatic_downloads": 1
    }
    chrome_options.add_experimental_option("prefs", prefs)

    # Tarayıcının tam ekran başlaması için
    chrome_options.add_argument("--start-maximized")

    # (İsteğe Bağlı) Script'i arkaplanda (GUI olmadan) çalıştırmak isterseniz aşağıdaki satırı aktif edin.
    # chrome_options.add_argument("--headless")

    # WebDriver'ı otomatik olarak yönetecek servisi kur
    service = ChromeService(executable_path=ChromeDriverManager().install())

    # Ayarlanmış seçenekler ve servis ile WebDriver'ı başlat
    driver = webdriver.Chrome(service=service, options=chrome_options)
    print("WebDriver başarıyla başlatıldı.")

    return driver