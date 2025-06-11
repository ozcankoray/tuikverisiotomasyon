# data_processing/file_handler.py dosyasının GÜNCEL içeriği

import os
import shutil
import time
from config import settings


def clean_directory(directory_path):
    """Belirtilen klasörün içeriğini temizler. Eğer klasör yoksa oluşturur."""
    if os.path.exists(directory_path):
        shutil.rmtree(directory_path)
    os.makedirs(directory_path, exist_ok=True)
    print(f"'{directory_path}' klasörü temizlendi ve yeniden oluşturuldu.")


def wait_and_rename_newest_file(directory_path: str, category_name: str, files_before_download: list,
                                timeout: int = 60):
    """
    Belirtilen klasörde YENİ bir EXCEL dosyasının indirilmesini bekler ve onu yeniden adlandırır.
    .htm gibi sahte dosyaları görmezden gelir.
    """
    start_time = time.time()
    print("Yeni Excel dosyası indirme işleminin tamamlanması bekleniyor...")

    while time.time() - start_time < timeout:
        current_files = os.listdir(directory_path)
        new_files = [f for f in current_files if f not in files_before_download]

        # <-- DEĞİŞTİ: Artık sadece .xls ve .xlsx uzantılı dosyalara odaklanıyoruz.
        for new_file in new_files:
            # Sadece gerçek Excel dosyalarını dikkate al, diğer her şeyi görmezden gel.
            if new_file.lower().endswith(('.xls', '.xlsx')) and not new_file.startswith('~'):

                # Dosyanın diske tam yazılması için kısa bir güvenlik beklemesi
                time.sleep(1)

                original_filepath = os.path.join(directory_path, new_file)

                # Bazen dosya bulunamaz hatası almamak için varlığını tekrar kontrol et
                if not os.path.exists(original_filepath):
                    continue

                safe_name = "".join(c for c in category_name if c.isalnum() or c in (' ', '_')).rstrip()
                file_extension = os.path.splitext(new_file)[1]
                new_filename = f"{safe_name}{file_extension}"
                new_filepath = os.path.join(directory_path, new_filename)

                try:
                    os.rename(original_filepath, new_filepath)
                    print(f"Dosya başarıyla indirildi ve yeniden adlandırıldı: '{new_filename}'")
                    return  # Görev tamamlandı, fonksiyondan çık
                except OSError as e:
                    print(f"Yeniden adlandırma sırasında bir hata oluştu: {e}. Dosya atlanıyor.")
                    return

        time.sleep(0.5)

    print(f"Hata: '{category_name}' için dosya indirme işlemi zaman aşımına uğradı!")
