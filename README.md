TÜİK Veri Otomasyon Aracı
![alt text](https://img.shields.io/badge/Python-3.9%2B-blue.svg)
![alt text](https://img.shields.io/badge/License-MIT-green.svg)
Bu proje, Türkiye İstatistik Kurumu'nun (TÜİK) Veri Portalı'nda yayınlanan haber bültenlerine ait istatistiksel tabloları otomatik olarak indirmek, işlemek ve düzenli Excel dosyaları halinde kaydetmek için geliştirilmiş bir otomasyon aracıdır.
Araştırmacılar, veri analistleri ve düzenli olarak TÜİK verilerine ihtiyaç duyan herkes için veri toplama sürecini önemli ölçüde hızlandırmak ve basitleştirmek amacıyla tasarlanmıştır.
✨ Temel Özellikler
Çoklu Kategori Desteği: Sadece enflasyon değil, "Dış Ticaret", "İşgücü İstatistikleri" gibi 17 farklı ana kategorideki verileri işleyebilir.
İnteraktif Kullanıcı Menüsü: Program çalıştığında, hangi kategorilerin işleneceğini kullanıcıya sorar. Tek bir kategori, birden fazla kategori veya tüm kategoriler aynı anda işlenebilir.
Görünmez (Headless) Tarayıcı: Tüm tarayıcı işlemleri arka planda, kullanıcıyı rahatsız etmeden (pencere açmadan) yürütülür.
Akıllı Veri Çekme: Bülten listelerini TÜİK'in web servisleri (API) üzerinden hızlıca alır ve sadece dosya indirme gibi zorunlu işlemler için Selenium kullanır. Bu hibrit yaklaşım, performansı ve güvenilirliği artırır.
Dinamik Tarih Filtreleme: Her çalıştırmada otomatik olarak bir önceki aya ait bültenleri hedefler. Manuel tarih ayarı gerektirmez.
Güvenilir Dosya Yönetimi: İndirilen dosyanın tamamlandığını anlar, bekler ve dosyaları Bülten Adı_Tablo Adı.xlsx gibi anlamlı isimlerle otomatik olarak yeniden adlandırır.
Gelişmiş Excel İşleme:
Farklı formatlardaki Excel dosyalarında başlık satırını akıllıca bulur.
İndirilen tüm tabloları, ilgili kategori için oluşturulmuş tek bir ana Excel dosyasının ayrı sayfalarına kaydeder.
Sonuç dosyasında sütun genişliklerini içeriğe göre otomatik ayarlar.
Yapılandırma Odaklı: Tüm kategoriler ve temel ayarlar config klasöründeki dosyalardan yönetilir, kod içinde değişiklik yapmaya gerek kalmaz.
📂 Proje Yapısı
Proje, sorumlulukların net bir şekilde ayrıldığı modüler bir yapıya sahiptir:
tuikverisiotomasyon/
│
├── config/
│   └── settings.py           # Temel ayarlar, klasör yolları ve kategori ID'leri
│
├── core/
│   ├── api_scraper.py        # Bülten listesini API'den çeken modül
│   ├── browser_actions.py    # Selenium ile indirme eylemlerini yöneten modül
│   ├── browser_setup.py      # Headless Chrome tarayıcısını yapılandıran modül
│
├── data_processing/
│   ├── excel_processor.py    # İndirilen Excel'leri işleyen ve birleştiren modül
│   ├── file_handler.py       # Dosya ve klasör işlemlerini yöneten modül
│
├── output/                     # Oluşturulan birleştirilmiş Excel dosyalarının kaydedildiği yer
├── downloads/                  # Geçici olarak indirilen ham Excel dosyalarının tutulduğu yer
│
├── main.py                     # Projenin ana giriş noktası, kullanıcı menüsünü içerir
└── requirements.txt            # Gerekli Python kütüphaneleri
Use code with caution.
🚀 Kurulum
Projeyi yerel makinenizde çalıştırmak için aşağıdaki adımları izleyin.
1. Projeyi Klonlayın:
git clone https://github.com/ozcankoray/tuikverisiotomasyon.git
cd tuikverisiotomasyon
Use code with caution.
Bash
2. Sanal Ortam (Virtual Environment) Oluşturun ve Aktif Edin:
Bu, projenin bağımlılıklarını sisteminizden izole tutmak için en iyi yöntemdir.
macOS / Linux:
python3 -m venv .venv
source .venv/bin/activate
Use code with caution.
Bash
Windows:
python -m venv .venv
.\.venv\Scripts\activate
Use code with caution.
Bash
3. Gerekli Kütüphaneleri Yükleyin:
requirements.txt dosyası, projenin ihtiyaç duyduğu tüm kütüphaneleri içerir.
pip install -r requirements.txt
Use code with caution.
Bash
Kurulum tamamlandı! Proje artık çalışmaya hazır.
🏃‍♀️ Kullanım
Projeyi çalıştırmak için ana dizindeyken aşağıdaki komutu girin:
python main.py
Use code with caution.
Bash
Program başladığında karşınıza interaktif bir menü çıkacaktır:
==============================
LÜTFEN İŞLEMEK İSTEDİĞİNİZ KATEGORİLERİ SEÇİN
==============================
   1. Adalet ve Secim
   2. Bilim Teknoloji ve Bilgi Toplumu
   3. Cevre ve Enerji
   4. Dis Ticaret
   ... (diğer kategoriler)

Seçim Yöntemleri:
  - Tek bir kategori için numarasını girin (Örn: 7).
  - Birden fazla kategori için numaraları virgülle ayırın (Örn: 4, 7, 11).
  - TÜM kategorileri işlemek için 'hepsi' yazın.
  - Çıkmak için 'q' veya 'cikis' yazın.

Seçiminiz >>>
Use code with caution.
Tek bir kategori için: Sadece numarasını yazın (örn: 4).
Birden fazla kategori için: Numaraları aralarına virgül koyarak yazın (örn: 4,7,11).
Tüm kategoriler için: hepsi yazın.
Seçiminizi yaptıktan sonra program, işlemleri arka planda (headless modda) yürütecek ve tüm adımları terminal ekranına yazdıracaktır.
📊 Çıktı
İşlem tamamlandığında, seçtiğiniz her kategori için output/ klasörü içinde aşağıdakine benzer bir Excel dosyası oluşturulur:
output/Birlestirilmis_Dis_Ticaret.xlsx
output/Birlestirilmis_Enflasyon_ve_Fiyat.xlsx
Bu Excel dosyalarının her birinin içinde, o kategoriye ait indirilen tüm istatistiksel tablolar ayrı sayfalarda yer alır.
🛠️ Kullanılan Teknolojiler
Python 3.9+
Selenium: Web tarayıcı otomasyonu ve dosya indirme işlemleri için.
Pandas: Excel dosyalarını okuma, işleme ve yazma için.
Requests: TÜİK API'sine HTTP istekleri göndermek için.
BeautifulSoup4: API'den gelen HTML yanıtını ayrıştırmak için.
webdriver-manager: Chrome sürücüsünü otomatik olarak yönetmek için.
