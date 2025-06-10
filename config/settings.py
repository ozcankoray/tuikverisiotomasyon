from pathlib import Path

# --- PROJE KÖK DİZİNİ ---
# Bu dosyanın (settings.py) bulunduğu konumdan iki üst dizine çıkarak ana proje klasörünü buluruz.
ROOT_DIR = Path(__file__).resolve().parent.parent

# --- KLASÖR YOLLARI ---
DOWNLOADS_DIR = ROOT_DIR / "downloads"
OUTPUT_DIR = ROOT_DIR / "output"
LOGS_DIR = ROOT_DIR / "logs"

# --- URL'LER ---
TUIK_BASE_URL = "https://data.tuik.gov.tr/"

# --- SELENIUM AYARLARI ---
# Elementlerin bulunması için beklenecek maksimum süre (saniye)
WAIT_TIMEOUT = 20

# --- ÇIKTI DOSYASI AYARLARI ---
FINAL_EXCEL_NAME = "Birlestirilmis.xlsx"