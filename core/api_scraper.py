import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime
from dateutil.relativedelta import relativedelta  # Ay hesaplaması için

# --- YENİ KISIM: Türkçe ay adları için bir sözlük ---
TURKISH_MONTHS = {
    1: "Ocak", 2: "Şubat", 3: "Mart", 4: "Nisan", 5: "Mayıs", 6: "Haziran",
    7: "Temmuz", 8: "Ağustos", 9: "Eylül", 10: "Ekim", 11: "Kasım", 12: "Aralık"
}


def fetch_bulletin_list() -> list[dict] | None:
    """
    TÜİK'in API'sine istek göndererek SADECE BİR ÖNCEKİ AYA AİT
    bültenlerin listesini dinamik olarak çeker.
    """
    api_url = "https://data.tuik.gov.tr/Kategori/GetHaberBultenleri"
    base_url = "https://data.tuik.gov.tr/"

    # --- YENİ KISIM: Dinamik olarak bir önceki ayı hesapla ---
    today = datetime.now()
    previous_month_date = today - relativedelta(months=1)
    target_year = previous_month_date.year
    target_month_name = TURKISH_MONTHS[previous_month_date.month]

    # Aranacak metin, örn: "Mayıs 2025"
    target_period_string = f"{target_month_name} {target_year}"
    print(f"Dinamik filtreleme aktif: Sadece '{target_period_string}' içeren bültenler alınacak.")

    payload = {'UstId': '106', 'DilId': '1', 'Page': '1', 'Count': '1000'}
    headers = {'User-Agent': 'Mozilla/5.0', 'X-Requested-With': 'XMLHttpRequest'}

    print("API'ye istek gönderilerek tüm bülten listesi çekiliyor...")

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

        # --- YENİ KISIM: Filtreleme işlemi ---
        filtered_bulletins = [
            b for b in all_bulletins if target_period_string in b['name']
        ]

        print(
            f"API'den toplam {len(all_bulletins)} bülten alındı, filtrelenerek {len(filtered_bulletins)} bülten işleme alınıyor.")
        return filtered_bulletins

    except requests.RequestException as e:
        print(f"Hata: API'ye istek gönderilirken bir sorun oluştu: {e}")
        return None