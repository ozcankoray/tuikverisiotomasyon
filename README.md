# TÜİK Veri Otomasyon Aracı

![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)

TÜİK Veri Portalı'ndan otomatik olarak veri indiren, işleyen ve birleştiren bir Python otomasyon aracıdır. Bu araç, manuel veri toplama sürecini ortadan kaldırarak araştırmacılar ve veri analistleri için zaman tasarrufu sağlamak üzere tasarlanmıştır.


---

## Ana Özellikler

- **Esnek Kategori Seçimi**: 17 farklı TÜİK ana kategorisinden dilediğiniz birini, birkaçını veya tümünü aynı anda işleyebilirsiniz.
- **Etkileşimli Arayüz**: Terminal üzerinden hangi verileri indireceğinizi kolayca seçmenizi sağlar.
- **Verimli ve Arka Planda Çalışma**: Tüm işlemleri `headless` (görünmez) modda yürüterek bilgisayarınızı meşgul etmez.
- **Akıllı Veri İşleme**: Farklı Excel formatlarındaki başlık satırlarını otomatik olarak algılar ve veriyi temizler.
- **Otomatik Raporlama**: İndirilen tüm tabloları, her kategori için ayrı ve düzenli bir Excel dosyasında, farklı sayfalara birleştirir.
- **Yapılandırma Odaklı**: Temel ayarlar koddan bağımsız olarak `config` klasöründen yönetilebilir.

---

## Kurulum

Projeyi çalıştırmak için makinenizde Python 3.9 veya üstü bir sürümün kurulu olması gerekmektedir.

**1. Proje Dosyalarını İndirin**

```bash
git clone https://github.com/ozcankoray/tuikverisiotomasyon.git
cd tuikverisiotomasyon


---


**2. Bağımlılıkları Yükleyin** 
Projenin ihtiyaç duyduğu kütüphaneleri requirements.txt dosyası ile tek komutta yükleyin:
# Bir sanal ortam oluşturup aktif etmeniz önerilir (opsiyonel)
# python -m venv venv
# venv\Scripts\activate

pip install -r requirements.txt
