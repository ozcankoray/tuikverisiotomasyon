import os  # os.listdir için eklendi
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

from config import settings
from data_processing import file_handler


class TuikBrowserActions:
    """Sadece belirli bir bülten sayfasından dosya indirme eylemlerini yönetir."""

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, settings.WAIT_TIMEOUT)

    def download_files_from_bulletin_page(self, bulletin_name: str):
        """Mevcut bülten sayfasındaki 'İstatistiksel Tablolar' bölümünden dosyaları indirir."""
        try:
            print(f"     '{bulletin_name}' bülteni işleniyor...")

            table = self.wait.until(EC.presence_of_element_located((By.ID, "istatistikselTable")))
            excel_rows = table.find_elements(By.XPATH, ".//tr[.//img[contains(@src, 'excel.png')]]")

            if not excel_rows:
                print("     Bu bültende indirilebilir Excel dosyası bulunamadı.")
                return

            print(f"     {len(excel_rows)} adet Excel dosyası indirilecek...")
            for row in excel_rows:
                link_text = row.find_element(By.CSS_SELECTOR, "td:last-child").text.strip()
                download_anchor = row.find_element(By.XPATH, ".//a[.//img[contains(@src, 'excel.png')]]")
                file_base_name = f"{bulletin_name}_{link_text}"

                # --- EN ÖNEMLİ DEĞİŞİKLİK BURADA ---
                # Tıklamadan hemen önce klasörün durumunu kaydet
                files_in_downloads_before = os.listdir(settings.DOWNLOADS_DIR)

                # İndirmeyi başlat
                self.driver.execute_script("arguments[0].click();", download_anchor)

                # Yeni ve akıllı bekle/yeniden adlandır fonksiyonunu çağır
                file_handler.wait_and_rename_newest_file(
                    directory_path=str(settings.DOWNLOADS_DIR),
                    category_name=file_base_name,
                    files_before_download=files_in_downloads_before
                )

        except TimeoutException:
            print("     Bu bültende 'İstatistiksel Tablolar' bölümü bulunamadı.")
        except Exception as e:
            print(f"     Bu bülten işlenirken beklenmedik bir hata oluştu: {e}")