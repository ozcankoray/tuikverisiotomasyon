# config/settings.py dosyasının GÜNCEL içeriği

from pathlib import Path

# Projenin ana dizinini referans noktası olarak al
BASE_DIR = Path(__file__).resolve().parent.parent

# --- YENİ BÖLÜM: Çıktı klasörünü kullanıcının "İndirilenler" klasörü olarak ayarla ---
# Bu, farklı işletim sistemlerinde (Windows, macOS, Linux) sorunsuz çalışır.
DOWNLOADS_DIR_USER = Path.home() / "Downloads"

# Geçici indirme ve log klasörleri projenin içinde kalmaya devam etsin
DOWNLOADS_DIR = BASE_DIR / "downloads"
LOGS_DIR = BASE_DIR / "logs"

# <-- DEĞİŞTİ: OUTPUT_DIR artık kullanıcının İndirilenler klasörünü gösteriyor.
OUTPUT_DIR = DOWNLOADS_DIR_USER 

# Eğer İndirilenler klasörü yoksa (çok nadir bir durum), program çökmesin diye oluştur.
OUTPUT_DIR.mkdir(exist_ok=True) 

# --- BÖLÜM SONU ---

# Sonuç Excel dosyasının temel adı
FINAL_EXCEL_NAME = "Birlestirilmis.xlsx"

# Tarayıcı bekleme süresi (saniye)
WAIT_TIMEOUT = 15

# İşlem yapılacak TÜİK kategorileri ve API ID'leri
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
