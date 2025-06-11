# core/api_scraper.py dosyasının GÜNCEL içeriği

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime
from dateutil.relativedelta import relativedelta

# <-- DEĞİŞTİ: Artık doğru değişken adını import ediyoruz.
from config.settings import TWO_MONTH_WINDOW_CATEGORY_IDS

TURKISH_MONTHS = {
    1: "Ocak", 2: "Şubat", 3: "Mart", 4: "Nisan", 5: "Mayıs", 6: "Haziran",
    7: "Temmuz", 8: "Ağustos", 9: "Eylül", 10: "Ekim", 11: "Kasım", 12: "Aralık"
}


# <-- DEĞİŞTİ: Fonksiyon artık gereksiz 'category_name' parametresini almıyor.
def fetch_bulletin_list(category_id: str) -> list[dict] | None:
    """
    TÜİK API'sine istek göndererek bülten listesini dinamik olarak çeker.
    Eğer kategori ID'si özel listedeyse 2 aylık, değilse 1 aylık veriyi hedefler.
    """
    api_url = "https://data.tuik.gov.tr/Kategori/GetHaberBultenleri"
    base_url = "https://data.tuik.gov.tr/"

    today = datetime.now()
    target_periods = []

    prev_month_date = today - relativedelta(months=1)
    prev_month_str = f"{TURKISH_MONTHS[prev_month_date.month]} {prev_month_date.year}"
    target_periods.append(prev_month_str)

    # <-- DEĞİŞTİ: Kontrol artık kategori ID'si üzerinden ve doğru değişkenle yapılıyor.
    if category_id in TWO_MONTH_WINDOW_CATEGORY_IDS:
        two_months_ago_date = today - relativedelta(months=2)
        two_months_ago_str = f"{TURKISH_MONTHS[two_months_ago_date.month]} {two_months_ago_date.year}"
        target_periods.append(two_months_ago_str)
        print(f"'{category_id}' ID'li kategori özel listede. Son 2 ay hedefleniyor: {target_periods}")
    else:
        print(f"Sadece bir önceki ay hedefleniyor: {target_periods}")

    payload = {'UstId': category_id, 'DilId': '1', 'Page': '1', 'Count': '1000'}
    headers = {'User-Agent': 'Mozilla/5.0', 'X-Requested-With': 'XMLHttpRequest'}

    print(f"API'ye istek gönderilerek '{category_id}' ID'li kategori için bülten listesi çekiliyor...")

    try:
        response = requests.post(api_url, data=payload, headers=headers, timeout=30)
        response.raise_for_status()
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

    except requests.RequestException as e:
        print(f"Hata: API'ye istek gönderilirken bir sorun oluştu: {e}")
        return None
