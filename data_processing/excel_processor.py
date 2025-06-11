# data_processing/excel_processor.py dosyasının GÜNCEL içeriği

import pandas as pd
import os
from config import settings

# ... _find_header_row ve _auto_fit_columns fonksiyonlarınız aynı kalabilir ...
def _find_header_row(file_path: str, engine: str, keywords: list, max_rows_to_scan: int = 20) -> int:
    """Bir Excel dosyasında, belirtilen anahtar kelimeleri içeren başlık satırını bulur."""
    try:
        df_preview = pd.read_excel(file_path, header=None, nrows=max_rows_to_scan, engine=engine)
        for index, row in df_preview.iterrows():
            row_content = ' '.join(str(cell).lower() for cell in row.dropna())
            if any(keyword.lower() in row_content for keyword in keywords):
                return index
    except Exception as e:
        print(f"Uyarı: Başlık satırı aranırken '{os.path.basename(file_path)}' dosyasında hata: {e}")
    return 0


def _auto_fit_columns(worksheet):
    """Verilen Excel çalışma sayfasındaki sütun genişliklerini içeriğe göre ayarlar."""
    for column_cells in worksheet.columns:
        length = max(len(str(cell.value)) for cell in column_cells)
        worksheet.column_dimensions[column_cells[0].column_letter].width = length + 2


# <-- DEĞİŞTİ: Fonksiyon artık kaynak ve hedef yollarını parametre olarak alıyor.
def process_and_merge_all_excels(source_directory: str, output_filepath: str):
    """
    Belirtilen klasördeki tüm Excel dosyalarını işler ve her birini
    tek bir ana dosyanın FARKLI SAYFALARINA yazar.
    """
    print(f"\n{'=' * 20} EXCEL İŞLEME VE SAYFALARA YAZMA İŞLEMİ BAŞLADI {'=' * 20}")

    # <-- DEĞİŞTİ: Değişkenler artık parametrelerden geliyor.
    downloads_path = source_directory
    output_file_path = output_filepath

    excel_files = [f for f in os.listdir(downloads_path) if f.endswith(('.xls', '.xlsx')) and not f.startswith('~')]
    if not excel_files:
        print("İşlenecek Excel dosyası bulunamadı.")
        return

    try:
        with pd.ExcelWriter(output_file_path, engine='openpyxl') as writer:
            sheet_counter = 1
            for filename in excel_files:
                file_path = os.path.join(downloads_path, filename)
                print(f"  -> İşleniyor: {filename}")

                try:
                    engine_to_use = None
                    if filename.lower().endswith('.xls'):
                        engine_to_use = 'xlrd'
                    elif filename.lower().endswith('.xlsx'):
                        engine_to_use = 'openpyxl'
                    else:
                        continue

                    temp_sheet_name = f"{sheet_counter} - {os.path.splitext(filename)[0]}"
                    sheet_name = temp_sheet_name[:31]
                    sheet_counter += 1

                    header_keywords = ['Yıl', 'Ay', 'Dönem', 'Tarih', 'Endeks', 'Değişim', 'Year', 'Month']
                    header_row_index = _find_header_row(file_path, engine=engine_to_use, keywords=header_keywords)

                    df = pd.read_excel(file_path, header=header_row_index, engine=engine_to_use)
                    df.dropna(how='all', axis=0, inplace=True)
                    df.dropna(how='all', axis=1, inplace=True)

                    df.to_excel(writer, sheet_name=sheet_name, index=False)

                    worksheet = writer.sheets[sheet_name]
                    _auto_fit_columns(worksheet)

                    print(f"     '{filename}' başarıyla '{sheet_name}' sayfasına yazıldı.")

                except Exception as e:
                    print(f"Hata: '{filename}' dosyası işlenemedi. Atlanıyor. Detay: {e}")

        print(
            f"\nBAŞARILI! Tüm dosyalar tek bir Excel belgesine farklı sayfalar olarak kaydedildi: \n{output_file_path}")

    except Exception as e:
        print(f"Hata: Sonuçlar ana Excel dosyasına yazılamadı. Detay: {e}")
