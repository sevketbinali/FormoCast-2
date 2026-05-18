# FormoCast - Mimari Tasarım (Design Document)

## 1. Sistem Mimarisi

FormoCast, bakımı kolay, genişletilebilir ve test edilebilir olması amacıyla **Modüler Monolit (Modular Monolith)** mimari tarzında tasarlanmıştır. Sistem temel olarak 4 ana modülden oluşmaktadır.

### 1.1. Veri Sağlama Modülü (Data Ingestion Module)
- **Görev:** BIST hisse senetlerinin geçmiş ve güncel OHLCV (Açılış, Yüksek, Düşük, Kapanış, Hacim) verilerini çekmek.
- **Teknolojiler:** `yfinance`, `pandas`.
- **Veri Akışı:** Çekilen veriler temizlenir, eksik günler doldurulur ve standart bir Pandas DataFrame formatına dönüştürülerek diğer modüllere aktarılır.

### 1.2. Formasyon Tanıma Modülü (Pattern Recognition Module)
- **Görev:** Fiyat verileri üzerindeki geometrik formasyonları (OBO, İkili Tepe vb.) tespit etmek.
- **Teknolojiler:** `scipy.signal` (yerel tepe ve dip tespiti için), `numpy`.
- **Algoritma Mantığı:** Fiyat serisi üzerinde hareketli ortalamalar veya ZigZag algoritması ile gürültü azaltılır. Bulunan ekstremum noktaları arasındaki fiyat ve zaman oranlarına bakılarak formasyon kuralları işletilir (örn. OBO için sol omuz, baş ve sağ omuzun oransal büyüklükleri ve boyun çizgisi kırılımı).

### 1.3. Backtest ve Simülasyon Modülü (Backtesting Engine)
- **Görev:** Geçmişte tespit edilen formasyonların ne kadar başarılı olduğunu hesaplamak ve simülasyon (X TL yatırılsaydı) raporu üretmek.
- **Teknolojiler:** `vectorbt` veya özel yazılmış simülasyon sınıfı.
- **İşleyiş:** Formasyon tespit edildiği anda (sinyal anı) sanal bir işleme girilir. Belirlenen Take-Profit (Kar Al) veya Stop-Loss (Zarar Kes) seviyelerine ulaşıldığında işlem kapatılır. Sonuçlar kümülatif olarak raporlanır.

### 1.4. Canlı Tarama ve Raporlama Modülü (Live Scanner & Reporting)
- **Görev:** Belirlenen hisse havuzunu (örn. BIST 100) periyodik olarak taramak ve anlık durum raporu üretmek.
- **Rapor Formatlayıcı:** Terminal çıktısı veya metin tabanlı (Markdown/JSON) çıktı üreterek kullanıcıya "Formasyon Bulundu, Geçmiş Doğruluk: %X" mesajını iletir.

## 2. Docker ve Altyapı Tasarımı

Sistem, taşınabilirlik ve kolay kurulum sağlamak amacıyla tamamen Dockerize edilecektir.
- **Konteyner Yapısı:** Tüm Python bağımlılıkları, modüller ve test araçları tek bir Docker imajı içinde paketlenecektir.
- **Çalıştırma Modları:** Konteyner ayağa kaldırılırken ortam değişkenleri (ENV_VARS) aracılığıyla "Backtest Modu" veya "Canlı Tarama Modu" seçilebilecektir.
- **Dockerfile:** `python:3.10-slim` tabanlı, `requirements.txt` üzerinden bağımlılıkların kurulduğu hafif bir yapı tercih edilecektir.

## 3. Veri Akış Şeması (Data Flow)
1. **İstek:** Kullanıcı veya zamanlayıcı tarama başlatır.
2. **Veri:** API üzerinden hisse verileri indirilir (`Data Ingestion`).
3. **Analiz:** Veriler `Pattern Recognition` modülüne girer, ekstremum noktaları bulunur, formasyonlar işaretlenir.
4. **Değerlendirme:** Eğer canlı mod ise, formasyon var mı kontrol edilir. Geçmiş performansı almak için `Backtesting Engine` çağrılır.
5. **Çıktı:** Karar destek metni formatlanarak kullanıcıya sunulur (`Reporting`).
