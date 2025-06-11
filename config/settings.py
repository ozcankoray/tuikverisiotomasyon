from pathlib import Path

# --- PROJE KÖK DİZİNİ ---
# Bu dosyanın (settings.py) bulunduğu konumdan iki üst dizine çıkarak ana proje klasörünü buluruz.
ROOT_DIR = Path(__file__).resolve().parent.parent

CATEGORIES_TO_PROCESS = {
    "Adalet_ve_Secim": "110",
    "Bilim_Teknoloji_ve_Bilgi_Toplumu": "102",
    "Cevre_ve_Enerji": "103",
    "Dis_Ticaret": "104",
    "Egitim_Kultur_Spor_ve_Turizm": "105",
    "Ekonomik_Guven": "117",
    "Enflasyon_ve_Fiyat": "106",
    "Gelir_Yasam_Tuketim_ve_Yoksulluk": "107",
    "Insaat_ve_Konut": "116",
    "Istihdam_Issizlik_ve_Ucret": "108",
    "Nufus_ve_Demografi": "109",
    "Saglik_ve_Sosyal_Koruma": "101",
    "Sanayi": "114",
    "Tarim": "111",
    "Ticaret_ve_Hizmet": "115",
    "Ulastirma_ve_Haberlesme": "112",
    "Ulusal_Hesaplar": "113",
}

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
