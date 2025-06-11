# core/browser_setup.py dosyasının GÜNCEL içeriği

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options  # <-- YENİ İMPORT
from webdriver_manager.chrome import ChromeDriverManager

from config import settings  # <-- YENİ İMPORT: İndirme klasörü yolunu almak için


def setup_driver() -> webdriver.Chrome:
    """
    Chrome WebDriver'ı "headless" modda ve gerekli ayarlar yapılmış olarak başlatır.
    """
    print("Chrome WebDriver 'headless' (görünmez) modda başlatılıyor...")

    # --- YENİ BÖLÜM: Chrome Seçeneklerini Yapılandırma ---
    chrome_options = Options()

    # 1. Headless modu etkinleştir. "new" argümanı modern ve daha stabil bir headless deneyimi sunar.
    chrome_options.add_argument("--headless=new")

    # 2. Grafik işlemci birimini (GPU) devre dışı bırak. Headless modda hataları önler.
    chrome_options.add_argument("--disable-gpu")

    # 3. Sayfa düzeninin bozulmaması için sanal pencere boyutunu belirle.
    chrome_options.add_argument("--window-size=1920,1080")

    # 4. (EN ÖNEMLİSİ) Headless modda dosya indirebilmek için ayar yap.
    #    'prefs' ayarı ile Chrome'a dosyaları nereye, sormadan indirmesi gerektiğini söylüyoruz.
    prefs = {
        "download.default_directory": str(settings.DOWNLOADS_DIR),  # Ayarlardan gelen indirme klasörü yolu
        "download.prompt_for_download": False,  # İndirme için onay isteme
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)
    # --- YENİ BÖLÜM SONU ---

    # WebDriver'ı güncellenmiş seçeneklerle başlat
    service = Service(ChromeDriverManager().install())

    # <-- DEĞİŞTİ: `options` parametresi eklendi
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Headless modda indirmelerin çalışması için bu ek komut gereklidir.
    driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd': 'Page.setDownloadBehavior',
              'params': {'behavior': 'allow', 'downloadPath': str(settings.DOWNLOADS_DIR)}}
    driver.execute("send_command", params)

    print("WebDriver başarıyla yapılandırıldı.")
    return driver
