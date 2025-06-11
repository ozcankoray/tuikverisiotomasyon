# core/api_scraper.py dosyasının GÜNCEL içeriği

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime
from dateutil.relativedelta import relativedelta
import time  # <-- YENİ İMPORT: Bekleme için gerekli

from config.settings import TWO_MONTH_WINDOW_CATEGORY_IDS

TURKISH_MONTHS = {
    1: "Ocak", 2: "Şubat", 3: "Mart", 4: "Nisan", 5: "Mayıs", 6: "Haziran",
    7: "Temmuz", 8: "Ağustos", 9: "Eylül", 10: "Ekim", 11: "Kasım", 12: "Aralık"
}


def fetch_bulletin_list(category_id: str) -> list[dict] | None:
    """
    TÜİK API'sine istek göndererek bülten listesini dinamik olarak çeker.
    Bağlantı hatalarına karşı yeniden deneme mekanizması içerir.
    """
    api_url = "https://data.tuik.gov.tr/Kategori/GetHaberBultenleri"
    base_url = "https://data.tuik.gov.tr/"

    today = datetime.now()
    target_periods = []
    prev_month_date = today - relativedelta(months=1)
    target_periods.append(f"{TURKISH_MONTHS[prev_month_date.month]} {prev_month_date.year}")

    if category_id in TWO_MONTH_WINDOW_CATEGORY_IDS:
        two_months_ago_date = today - relativedelta(months=2)
        target_periods.append(f"{TURKISH_MONTHS[two_months_ago_date.month]} {two_months_ago_date.year}")
        print(f"'{category_id}' ID'li kategori özel listede. Son 2 ay hedefleniyor: {target_periods}")
    else:
        print(f"Sadece bir önceki ay hedefleniyor: {target_periods}")

    payload = {'UstId': category_id, 'DilId': '1', 'Page': '1', 'Count': '1000'}
    headers = {'User-Agent': 'Mozilla/5.0', 'X-Requested-With': 'XMLHttpRequest'}

    # --- YENİ BÖLÜM: Yeniden Deneme (Retry) Mekanizması ---
    MAX_RETRIES = 3
    RETRY_DELAY_SECONDS = 5
    response = None

    for attempt in range(MAX_RETRIES):
        try:
            print(f"API'ye istek gönderiliyor (Deneme {attempt + 1}/{MAX_RETRIES})...")
            response = requests.post(api_url, data=payload, headers=headers, timeout=30)
            response.raise_for_status()  # HTTP 4xx veya 5xx hatalarını yakala
            print("API'den başarılı yanıt alındı.")
            break  # İstek başarılıysa döngüden çık
        except requests.RequestException as e:
            print(f"HATA (Deneme {attempt + 1}): API isteği başarısız oldu. Detay: {e}")
            if attempt < MAX_RETRIES - 1:
                print(f"{RETRY_DELAY_SECONDS} saniye sonra yeniden denenecek...")
                time.sleep(RETRY_DELAY_SECONDS)
            else:
                print("Maksimum deneme sayısına ulaşıldı. Bu kategori atlanıyor.")
                return None  # Tüm denemeler başarısız olursa None döndür
    # --- YENİ BÖLÜM SONU ---


    # Buradan sonrası sadece 'response' başarılı ise çalışır
    soup = BeautifulSoup(response.text, 'html.parser')
    all_bulletins = []
    bulletin_links = soup.select("div.news-content > a")

    if not bulletin_links:
        print("Hata: API'den gelen yanıtta bülten linki bulunamadı.")
        return None

    for link in bulletin_links:
        bulletin_name = link.text.strip()
        relative_url = link.get('href')
        full_url = urljoin(base_url, relative_url)
        all_bulletins.append({'name': bulletin_name, 'url': full_url})

    filtered_bulletins = [
        b for b in all_bulletins if any(period in b['name'] for period in target_periods)
    ]

    print(
        f"API'den toplam {len(all_bulletins)} bülten alındı, filtrelenerek {len(filtered_bulletins)} bülten işleme alınıyor.")
    return filtered_bulletins
