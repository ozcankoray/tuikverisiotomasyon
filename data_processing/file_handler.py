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
    Belirtilen klasörde YENİ bir dosyanın indirilmesini bekler ve onu yeniden adlandırır.

    Args:
        directory_path (str): İndirme klasörünün yolu.
        category_name (str): Dosyaya verilecek temel ad.
        files_before_download (list): İndirme başlamadan önce klasördeki dosyaların listesi.
        timeout (int): Beklenecek maksimum saniye.
    """
    start_time = time.time()
    print("Yeni dosya indirme işleminin tamamlanması bekleniyor...")

    while time.time() - start_time < timeout:
        current_files = os.listdir(directory_path)
        # İndirme öncesi listede olmayan YENİ dosyaları bul
        new_files = [f for f in current_files if f not in files_before_download]

        if new_files:
            # Yeni dosyalar içinde, indirmesi tamamlanmış olanı (geçici olmayan) bul
            for new_file in new_files:
                if not new_file.endswith(('.crdownload', '.tmp')):
                    time.sleep(1)  # Dosyanın tam yazıldığından emin olmak için kısa bekleme

                    original_filepath = os.path.join(directory_path, new_file)

                    # Dosya adını temizle ve uzantısını koru
                    safe_name = "".join(c for c in category_name if c.isalnum() or c in (' ', '_')).rstrip()
                    file_extension = os.path.splitext(new_file)[1]
                    new_filename = f"{safe_name}{file_extension}"
                    new_filepath = os.path.join(directory_path, new_filename)

                    os.rename(original_filepath, new_filepath)

                    print(f"Dosya başarıyla indirildi ve yeniden adlandırıldı: '{new_filename}'")
                    return  # Görev tamamlandı, fonksiyondan çık

        time.sleep(0.5)

    print(f"Hata: '{category_name}' için dosya indirme işlemi zaman aşımına uğradı!")