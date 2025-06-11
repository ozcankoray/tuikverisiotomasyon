from pathlib import Path

# Projenin ana dizinini referans noktası olarak al
BASE_DIR = Path(__file__).resolve().parent.parent

# Kullanıcının standart "İndirilenler" klasörünü bul (Tüm işletim sistemlerinde çalışır)
DOWNLOADS_DIR_USER = Path.home() / "Downloads"

# Uygulama içi geçici klasörler
DOWNLOADS_DIR = BASE_DIR / "downloads"
LOGS_DIR = BASE_DIR / "logs"

# === ANA ÇIKTI KLASÖRÜ ===
# Oluşturulan Excel dosyaları doğrudan kullanıcının İndirilenler klasörüne kaydedilecek.
OUTPUT_DIR = DOWNLOADS_DIR_USER

# İndirilenler klasörünün var olduğundan emin ol (genellikle hep vardır)
OUTPUT_DIR.mkdir(exist_ok=True)

# Tarayıcı bekleme süresi (saniye)
WAIT_TIMEOUT = 15

# === KATEGORİ AYARLARI ===

# İşlem yapılacak tüm TÜİK kategorileri ve API ID'leri
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

# --- YENİ BÖLÜM: 2 Aylık Veri Penceresi Gerektiren Kategori ID'leri ---
# Bu sette bulunan kategori ID'leri için program, hem bir önceki ayı hem de
# iki önceki ayı kontrol edecektir.
TWO_MONTH_WINDOW_CATEGORY_IDS = {
    "104",  # Dış Ticaret
    "116",  # İnşaat ve Konut
    "108",  # İstihdam, İşsizlik ve Ücret
    "114",  # Sanayi
    "115",  # Ticaret ve Hizmet
}
