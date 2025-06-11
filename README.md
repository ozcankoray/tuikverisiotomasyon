# TÜİK Veri Otomasyon Aracı

![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

TÜİK Veri Portalı'ndan otomatik olarak veri indiren, işleyen ve birleştiren bir Python otomasyon aracıdır. Bu araç, manuel veri toplama sürecini ortadan kaldırarak araştırmacılar ve veri analistleri için zaman tasarrufu sağlamak üzere tasarlanmıştır.

![Uygulama Demosu](https://user-images.githubusercontent.com/10940562/228994793-17b5e4c0-2e45-429a-8a1a-463d11b156b2.gif)
*(Not: Bu bir örnek GIF'tir. Kendi projenizin ekran kaydını ekleyebilirsiniz.)*

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
