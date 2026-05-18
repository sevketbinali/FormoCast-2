# FormoCast - Finansal Formasyon Analiz Sistemi

FormoCast, Borsa İstanbul (BIST) hisse senetleri üzerinde otomatik olarak geometrik fiyat formasyonlarını (İkili Tepe, Omuz Baş Omuz vb.) tespit eden, bu formasyonların geçmiş başarı oranlarını hesaplayan (backtest) ve anlık olarak güncel piyasayı tarayabilen profesyonel bir teknik analiz botudur.

## Temel Özellikler
1. **Geçmiş Veri Analizi ve Formasyon Tespiti:** Seçilen BIST hisselerinin fiyat grafiklerindeki "Tepe" (Peak) ve "Dip" (Trough) noktalarını matematiksel olarak (Scipy kullanılarak) bularak formasyon tespitleri yapar.
2. **Backtest ve PnL Simülasyonu:** "Geçmişte bu formasyon bulunduğunda X TL yatırılsaydı, Kar-Al (Take Profit) ve Zarar-Kes (Stop Loss) stratejisiyle sonuç ne olurdu?" simülasyonunu çalıştırır ve **Win Rate (Başarı Oranı)** hesaplar.
3. **Canlı Piyasa Taraması (Live Scanner):** Belirlediğiniz hisse havuzunda (Örn: BIST 30) son birkaç gün içerisinde oluşmuş güncel formasyonları bulur. Geçmiş başarı oranlarına dayanarak yön öngörülerinde (YÜKSELİŞ/DÜŞÜŞ) bulunur.
4. **Modüler ve Dockerize Mimari:** Kurulum ve dağıtımın kusursuz yapılabilmesi için tüm sistem Docker container üzerinde çalışmaktadır.

## Kullanılan Teknolojiler
- **Python 3.10+**
- **Veri Çekme:** `yfinance`, `pandas`
- **Hesaplama Motoru:** `numpy`, `scipy.signal`
- **Test Altyapısı:** `pytest`
- **Altyapı:** Docker, Docker Compose

## Kurulum ve Çalıştırma
Projeyi kendi ortamınızda çalıştırmak için yalnızca Docker'a ihtiyacınız vardır.

```bash
# Proje dizinine gidin
cd "FormoCast 2"

# Sistemi derleyin ve çalıştırın
docker-compose up --build
```
*Not: Sistem çalıştırıldığında `main.py` içerisindeki entegrasyon senaryosu işleyecektir. Öncelikle THYAO hissesi üzerinde geçmişe dönük backtest yapacak, ardından seçili havuzda canlı tarama (Live Scan) yapıp rapor oluşturacaktır.*

## Testleri Çalıştırma
Projeye entegre edilmiş Unit Test'leri Docker üzerinden çalıştırmak için:
```bash
docker-compose run formocast_app pytest tests/
```

## Proje Dizini (Mimari)
- **`src/data_ingestion/`**: Fiyat verilerini indirme modülü.
- **`src/pattern_recognition/`**: Matematiksel tepe/dip tespiti ve İkili Tepe, OBO tespit algoritmaları.
- **`src/backtesting/`**: Strateji simülasyonu ve PnL (Kar/Zarar) hesaplamaları.
- **`src/scanner/`**: Güncel formasyon taraması ve raporlama.
- **`src/utils/`**: Merkezi hata yönetimli ve formatlı loglama (Logger).
- **`knowledge.md`**: Sistem özelindeki hata kodlarının (ERR-DATA-001 vb.) anlamlarını içerir.
- **`plan.md`, `requirements.md`, `design.md`**: Sistemin temel mimari dökümanlarıdır.
