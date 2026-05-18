# FormoCast - Gereksinimler (Requirements)

## 1. İşlevsel Gereksinimler (Functional Requirements)

### 1.1. Geçmiş Veri Analizi ve Backtest
- Sistem, belirlenen BIST hisselerinin geçmiş verilerini alabilmelidir.
- Geçmiş veriler üzerinde Omuz Baş Omuz (OBO), İkili Tepe/Dip, Destek/Direnç gibi formasyonları otomatik olarak tespit edebilmelidir.
- Tespit edilen formasyonların başarı oranlarını (Win Rate) ve Kar/Zarar (PnL) performanslarını analiz edebilmelidir.

### 1.2. Yatırım Simülasyonu
- Kullanıcı, "Şu tarihte şu hisseye X TL yatırılsaydı ve tespit edilen formasyona göre işlem yapılsaydı sonuç ne olurdu?" tarzında simülasyonlar çalıştırabilmelidir.
- Simülasyon sonuçları, giriş noktası, stop-loss ve take-profit seviyelerini hesaba katarak net kar/zarar miktarını göstermelidir.

### 1.3. Canlı Tarama ve Tespit (Live Scanning)
- Sistem, şu anda aktif olan hisse senetlerinin güncel grafiklerini tarayabilmelidir.
- Aktif grafiklerde oluşan formasyonları gerçek zamanlı (veya gün sonu) olarak tespit edebilmelidir.

### 1.4. Öngörü ve Raporlama
- Tespit edilen canlı formasyonlar için bir öngörü raporu oluşturulmalıdır.
- Rapor formatı: "Bu hissede [Formasyon Adı] formasyonu bulunmaktadır. Bu formasyon geçmişte bu hissede %X doğrulukla şu sonucu vermiştir. Şu an beklenen senaryo [Yön/Hedef] yönündedir." şeklinde olmalıdır.

## 2. Teknik ve Operasyonel Gereksinimler (Non-Functional Requirements)

### 2.1. Dil ve Dökümantasyon
- Sistemdeki tüm kod blokları (fonksiyonlar, sınıflar, değişkenler vb.) açık ve anlaşılır bir **Türkçe dökümantasyona** (docstring) sahip olmalıdır.
- Tüm mimari ve kullanım kılavuzları Türkçe yazılmalıdır.

### 2.2. Test Edilebilirlik
- Sistemin her bir modülü (veri çekme, formasyon tespiti, backtest, raporlama) için Unit Testler (Birim Testleri) yazılmalıdır.
- Test sonuçları otomatik olarak raporlanabilmelidir.

### 2.3. Dağıtım ve Altyapı (Deployment)
- Tüm servisler (veri tabanı, tarama motoru, raporlama) bir Docker ortamında çalışabilmelidir.
- `docker-compose up` komutu ile tüm sistem tek bir konteyner ortamında (veya network üzerinde) ayağa kaldırılabilir olmalıdır.

### 2.4. Hata Yönetimi
- Sistemde oluşabilecek istisnai durumlar için spesifik hata kodları tanımlanmalıdır.
- Bu hata kodlarının anlamları ve nasıl çözülecekleri ayrı bir `knowledge.md` dosyasında detaylıca açıklanmalıdır.
