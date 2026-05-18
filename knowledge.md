# FormoCast - Hata Yönetimi ve Bilgi Bankası (Knowledge Base)

Bu dosya, FormoCast sistemi çalışırken karşılaşılabilecek özel hata kodlarını, bu hataların olası sebeplerini ve çözüm adımlarını içerir.

## Hata Kodları (Error Codes)

### ERR-DATA-001: Veri Kaynağına Ulaşılamadı
- **Anlamı:** Hisse senedi verilerini çeken API'ye (örn. yfinance) bağlantı kurulamadı veya sunucu cevap vermiyor.
- **Olası Sebep:** İnternet bağlantısı koptu, API limitlerine takılındı veya borsa tatili nedeniyle veri akışı durdu.
- **Çözüm Adımı:** İnternet bağlantınızı kontrol edin. Sık istek atılıyorsa (rate limit) bekleme (sleep) sürelerini artırın. İlgili hisse (örn. `THYAO.IS`) kodunun doğru yazıldığından emin olun.

### ERR-DATA-002: Eksik veya Bozuk Veri Formatı
- **Anlamı:** Çekilen veri seti içerisinde boş (NaN) değerler mevcut veya istenen OHLCV kolonları bulunmuyor.
- **Olası Sebep:** Hisse halka yeni arz olmuş olabilir, işlem görmediği bir döneme denk gelinmiş olabilir.
- **Çözüm Adımı:** DataFrame üzerindeki `.dropna()` veya `.fillna()` metodlarının doğru çalıştığından emin olun. Gerekirse veri aralığını daraltın.

### ERR-PTRN-001: Ekstremum Noktaları Hesaplanamadı
- **Anlamı:** Formasyon analizi için yeterli sayıda tepe veya dip noktası bulunamadı.
- **Olası Sebep:** Veri setinin boyutu (gün sayısı) çok az veya piyasa o dönemde tamamen yatay (flat) ilerlemiş.
- **Çözüm Adımı:** Çekilen tarih aralığını uzatın (en az 6 aylık veri önerilir). Algoritmaya verilen "order" veya pürüzsüzleştirme (smoothing) parametresini düşürün.

### ERR-SIM-001: Simülasyon Sıfır İşlem Döndürdü
- **Anlamı:** Backtest simülasyonu çalıştı ancak belirtilen tarih aralığında geçmişte hiçbir formasyon tespit edilemediği için kar/zarar (PnL) hesabı yapılamadı.
- **Olası Sebep:** Formasyon kuralları veya hata toleransı çok katı belirlenmiş.
- **Çözüm Adımı:** İlgili formasyonun parametrelerindeki hata payı (tolerance threshold) oranını (örn. %2'den %5'e) artırarak esneklik sağlayın.

### ERR-DOCKER-001: Konteyner Başlatılamadı veya Hızlıca Kapandı
- **Anlamı:** `docker-compose up` komutu sonrası Python servisi hata vererek exit(1) koduna düştü.
- **Olası Sebep:** Eksik environment variable (Çevre değişkeni) veya bağımlılıkların (`requirements.txt`) yanlış yüklenmesi.
- **Çözüm Adımı:** `docker logs formocast_app` komutu ile iç logları inceleyin. `.env` dosyanızın oluşturulduğundan ve gerekli değişkenlerin tanımlandığından emin olun.

## Geliştirici Notları
Uygulama genelinde, hatalar ekrana basılırken daima `logger.error(f"{HATA_KODU}: Detay...")` formatı kullanılmalıdır. Bu sayede log mekanizması, hataları standart bir şekilde kaydedebilir ve gerektiğinde izleme (monitoring) sistemlerine entegre edilebilir.
