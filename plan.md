# FormoCast - Proje Planı (Project Plan)

## 1. Proje Özeti
FormoCast, Borsa İstanbul (BIST) verileri üzerinde finansal formasyonları (Omuz Baş Omuz, İkili Tepe/Dip, Destek/Direnç vb.) otomatik olarak tanıyan, analiz eden ve geriye dönük (backtest) başarı oranlarını hesaplayan profesyonel bir teknik analiz ve sinyal platformudur.

## 2. Kütüphane ve Teknoloji Seçimi
Yapılan araştırmalar sonucunda, geometrik formasyonların (OBO, İkili Tepe vb.) tespitinde tek bir "sihirli" kütüphane bulunmamaktadır. En profesyonel ve güvenilir yöntem, yerel ekstremum (tepe ve dip) noktalarını bulup, formasyon kurallarını matematiksel olarak uygulamaktır.

- **Veri Sağlayıcı (Data Ingestion):** `yfinance`, `tvDatafeed` veya BIST için yerel bir API (örn. İş Yatırım API).
- **Veri Manipülasyonu:** `pandas`, `numpy`
- **Tepe/Dip (Extrema) Tespiti:** `scipy.signal.argrelextrema` (Trend dönüş noktalarını bulmak için) veya `ZigZag` algoritmaları.
- **Teknik İndikatörler:** `TA-Lib` veya `pandas-ta` (Formasyonları RSI, MACD gibi hacim ve momentum indikatörleriyle doğrulamak için).
- **Simülasyon / Backtest:** `Backtrader` veya `vectorbt` (PnL hesaplamaları ve strateji simülasyonları için).
- **Altyapı:** Docker, Python 3.10+

## 3. Geliştirme Aşamaları

### Aşama 1: Temel Veri Altyapısı ve Uç Nokta (Extrema) Tespiti
- BIST hisselerinin (örn. THYAO, GARAN) günlük ve seanslık OHLCV verilerinin çekilmesi.
- Verilerin temizlenmesi ve `pandas` DataFrame olarak hazırlanması.
- `scipy` kullanarak grafikteki tepe (peak) ve dip (trough) noktalarının tespit edilmesi.

### Aşama 2: Formasyon Tanıma Motorunun (Pattern Recognition Engine) Geliştirilmesi
- İkili Tepe / İkili Dip (Double Top/Bottom) algoritmalarının yazılması.
- Omuz Baş Omuz (Head and Shoulders) ve Ters OBO algoritmalarının yazılması.
- Destek / Direnç seviyelerinin otomatik hesaplanması.
- Formasyonların doğruluk payını artırmak için hata tolerans (±%X) parametrelerinin eklenmesi.

### Aşama 3: Backtest ve Simülasyon Modülü
- Geçmiş verilere göre formasyonların başarı oranlarının (Win Rate) hesaplanması.
- Kar/Zarar (PnL) analizlerinin yapılması.
- "X TL yatırılsaydı, stop-loss ve take-profit seviyelerine göre kaç TL olurdu?" simülasyon motorunun entegrasyonu.

### Aşama 4: Canlı Tarama ve Raporlama Sistemi
- Aktif BIST hisselerinde güncel formasyonların tespiti.
- Her formasyon için geçmiş başarı oranına dayalı istatistiksel öngörü raporunun oluşturulması.
- Terminal veya arayüz üzerinden "Şu hissede şu formasyon var, geçmiş doğruluk %X, beklenen yön Y" şeklinde çıktı verilmesi.

### Aşama 5: Dockerizasyon ve Testler
- Sistemdeki her bir modül (Veri çekme, formasyon tespiti, backtest) için Unit Test yazılması (`pytest`).
- Tüm uygulamanın bir `docker-compose.yml` ile tek bir konteyner/servis mimarisinde ayağa kaldırılması.
- Kapsamlı Türkçe dökümantasyonun tamamlanması.
