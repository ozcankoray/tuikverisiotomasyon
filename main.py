# main.py dosyasının KULLANICI SEÇİMİNE OLANAK TANIYAN GÜNCEL içeriği

from core.browser_setup import setup_driver
from core.browser_actions import TuikBrowserActions
from core.api_scraper import fetch_bulletin_list
from data_processing.file_handler import clean_directory
from data_processing.excel_processor import process_and_merge_all_excels
from config import settings
import time
import sys  # Programı temizce sonlandırmak için eklendi


def prompt_for_category_selection():
    """
    Kullanıcıya ayarlar dosyasındaki kategorileri listeler ve bir veya daha fazla
    seçim yapmasını ister. Seçilen kategorileri bir sözlük olarak döndürür.
    """
    # Ayarlar dosyasındaki kategorileri daha kolay erişim için bir listeye dönüştür
    categories_list = list(settings.CATEGORIES_TO_PROCESS.items())

    while True:
        print("\n" + "=" * 30)
        print("LÜTFEN İŞLEMEK İSTEDİĞİNİZ KATEGORİLERİ SEÇİN")
        print("=" * 30)

        # Kullanıcıya numaralandırılmış bir liste sun
        for i, (name, cat_id) in enumerate(categories_list, 1):
            print(f"  {i:2d}. {name.replace('_', ' ')}")

        print("\nSeçim Yöntemleri:")
        print("  - Tek bir kategori için numarasını girin (Örn: 7).")
        print("  - Birden fazla kategori için numaraları virgülle ayırın (Örn: 4, 7, 11).")
        print("  - TÜM kategorileri işlemek için 'hepsi' yazın.")
        print("  - Çıkmak için 'q' veya 'cikis' yazın.")

        user_input = input("\nSeçiminiz >>> ").strip().lower()

        if user_input in ["q", "cikis"]:
            return None  # Kullanıcı çıkmak istediğinde None döndür

        if user_input in ["hepsi", "all", "tum"]:
            return settings.CATEGORIES_TO_PROCESS  # Tüm listeyi döndür

        selected_categories = {}
        has_error = False

        try:
            choices = user_input.split(',')
            if not choices or not any(c.strip() for c in choices):
                raise ValueError("Boş giriş yaptınız.")

            for choice in choices:
                choice_num = int(choice.strip())
                if not (1 <= choice_num <= len(categories_list)):
                    print(f"HATA: {choice_num} geçersiz bir numara. Lütfen listeden bir numara seçin.")
                    has_error = True
                    break

                # Kullanıcının 1 tabanlı seçimini 0 tabanlı indexe çevir
                selected_name, selected_id = categories_list[choice_num - 1]
                selected_categories[selected_name] = selected_id

            if not has_error:
                print("\nŞu kategoriler işlenecek:")
                for name in selected_categories.keys():
                    print(f"  - {name.replace('_', ' ')}")
                time.sleep(2)
                return selected_categories

        except ValueError:
            print("HATA: Lütfen sadece sayıları veya izin verilen komutları kullanın.")
            has_error = True

        if has_error:
            print("Lütfen tekrar deneyin...")
            time.sleep(2)


def main():
    """Kullanıcının seçtiği kategoriler için veri indirme otomasyonunu yönetir."""
    # <-- YENİ: Önce kullanıcıdan seçim yapmasını iste
    selected_items = prompt_for_category_selection()

    # <-- YENİ: Kullanıcı çıkmayı seçtiyse programı sonlandır
    if not selected_items:
        print("\nProgramdan çıkılıyor. Hoşça kalın!")
        sys.exit()

    overall_start_time = time.time()
    print("\n===== TÜİK VERİ OTOMASYONU BAŞLATILDI =====")

    # Artık tüm listeyi değil, kullanıcının seçtiği listeyi işle
    for category_name, category_id in selected_items.items():
        category_start_time = time.time()
        print(f"\n\n{'=' * 25} KATEGORİ İŞLENİYOR: {category_name} (ID: {category_id}) {'=' * 25}")

        download_dir = settings.DOWNLOADS_DIR
        clean_directory(download_dir)

        final_excel_path = settings.OUTPUT_DIR / f"Birlestirilmis_{category_name}.xlsx"
        if final_excel_path.exists():
            final_excel_path.unlink()

        bulletin_list = fetch_bulletin_list(category_id)

        if not bulletin_list:
            print(f"'{category_name}' kategorisi için işlenecek bülten bulunamadı. Sonraki kategoriye geçiliyor.")
            continue

        driver = None
        try:
            driver = setup_driver()
            actions = TuikBrowserActions(driver)

            for bulletin in bulletin_list:
                bulletin_name = bulletin['name']
                bulletin_url = bulletin['url']

                print(f"\n{'=' * 20} BÜLTEN İŞLENİYOR: {bulletin_name} {'=' * 20}")
                driver.get(bulletin_url)
                actions.download_files_from_bulletin_page(bulletin_name)

            print(f"\n===== '{category_name}' Kategorisindeki Tüm Bültenlerin İndirilmesi Tamamlandı! =====")

            process_and_merge_all_excels(
                source_directory=str(download_dir),
                output_filepath=str(final_excel_path)
            )

        except Exception as e:
            print(f"\n!!!!!! '{category_name}' KATEGORİSİ İŞLENİRKEN KRİTİK BİR HATA OLUŞTU: {e}")
        finally:
            if driver:
                driver.quit()
                print("\nTarayıcı kapatıldı.")

        category_end_time = time.time()
        print(
            f"\n===== '{category_name}' Kategorisi Tamamlandı! Süre: {category_end_time - category_start_time:.2f} saniye =====")

    overall_end_time = time.time()
    print(f"\n\n===== TÜM GÖREVLER TAMAMLANDI! Toplam Süre: {overall_end_time - overall_start_time:.2f} saniye =====")


if __name__ == "__main__":
    main()
