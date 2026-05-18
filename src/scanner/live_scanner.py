from typing import List, Dict, Any
from src.utils.logger import logger
from src.data_ingestion.fetcher import BISTDataFetcher
from src.pattern_recognition.extrema import ExtremaDetector
from src.pattern_recognition.patterns import PatternDetector
from src.backtesting.simulator import Simulator

class LiveScanner:
    """
    Belirli bir hisse listesini tarayarak güncel (aktif) formasyonları bulan
    ve geçmiş başarı oranlarıyla raporlayan tarama modülü.
    """
    
    def __init__(self, recent_bars: int = 5):
        """
        LiveScanner sınıfının başlatılması.
        
        Parametreler:
            recent_bars (int): Kaç bar (gün) öncesine kadar olan formasyonların 
                               'Aktif' (Live) sayılacağını belirler. Varsayılan 5 gündür.
        """
        self.fetcher = BISTDataFetcher()
        self.extrema_detector = ExtremaDetector(order=5)
        self.pattern_detector = PatternDetector(tolerance_pct=0.03)
        # Geçmiş performans için simülatör (örnek 10.000 TL ile)
        self.simulator = Simulator(initial_capital=10000.0, tp_pct=0.05, sl_pct=0.03)
        self.recent_bars = recent_bars

    def scan_market(self, tickers: List[str]) -> List[Dict[str, Any]]:
        """
        Verilen hisse sembollerini tarar ve aktif formasyonları tespit eder.
        
        Parametreler:
            tickers (List[str]): Taranacak BIST hisse sembollerinin listesi.
            
        Dönüş:
            Aktif formasyonların ve üretilen rapor metinlerinin listesi.
        """
        live_reports = []
        
        for ticker in tickers:
            logger.info(f"Canlı Tarama başlatılıyor: {ticker}")
            
            df = self.fetcher.fetch_historical_data(ticker, period="2y", interval="1d")
            if df is None or df.empty:
                continue
                
            total_bars = len(df)
            extrema = self.extrema_detector.find_extrema(df['Close'])
            
            double_tops = self.pattern_detector.find_double_top(extrema['peaks'], extrema['troughs'])
            hs_patterns = self.pattern_detector.find_head_and_shoulders(extrema['peaks'], extrema['troughs'])
            all_patterns = double_tops + hs_patterns
            
            if not all_patterns:
                logger.info(f"{ticker} için geçmişte veya güncelde formasyon bulunamadı.")
                continue
                
            # Hisse üzerindeki bu formasyonların geçmiş başarı oranını hesapla
            sim_result = self.simulator.run_backtest(df, all_patterns)
            win_rate = sim_result['win_rate']
            
            # Güncel (Live) formasyonları filtrele
            active_patterns = [p for p in all_patterns if total_bars - p['end_idx'] <= self.recent_bars]
            
            for pattern in active_patterns:
                pattern_type = pattern['type']
                
                # Basit yön analizi: OBO ve İkili Tepe genelde düşüş sinyali olarak bilinir
                # Ancak burada BIST piyasasında esnek veya test amaçlı yön tayini yapabiliriz.
                # Şimdilik standart literatüre göre yön yazalım.
                expected_dir = "DÜŞÜŞ" if pattern_type in ["Double Top", "Head and Shoulders"] else "YÜKSELİŞ"
                
                # Gereksinimlerde istenen rapor formatı:
                report_text = (
                    f"Bu hissede {pattern_type} formasyonu bulunmaktadır. "
                    f"Bu formasyon geçmişte bu hissede %{win_rate:.2f} doğrulukla "
                    f"başarılı sonuç vermiştir. Şu an beklenen senaryo {expected_dir} yönündedir."
                )
                
                live_reports.append({
                    "ticker": ticker,
                    "pattern": pattern_type,
                    "win_rate": win_rate,
                    "direction": expected_dir,
                    "report": report_text,
                    "end_idx": pattern['end_idx'],
                    "date": str(df.index[pattern['end_idx']].date())
                })
                
                logger.info(f"CANLI SİNYAL: {ticker} - {report_text}")
                
        return live_reports
