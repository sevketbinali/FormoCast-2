import sys
from src.utils.logger import logger
from src.data_ingestion.fetcher import BISTDataFetcher
from src.pattern_recognition.extrema import ExtremaDetector
from src.pattern_recognition.patterns import PatternDetector
from src.backtesting.simulator import Simulator
from src.scanner.live_scanner import LiveScanner

def main():
    logger.info("=======================================")
    logger.info("       FormoCast Sistem Başlatıldı       ")
    logger.info("=======================================")
    
    # Sistemin iki temel modunu çalıştıralım:
    
    # 1. Geriye Dönük Analiz ve Simülasyon (Backtest Mode)
    logger.info("\n--- MOD 1: Geriye Dönük Analiz (Backtest) ---")
    ticker = "THYAO"
    fetcher = BISTDataFetcher()
    df = fetcher.fetch_historical_data(ticker, period="1y", interval="1d")
    
    if df is not None and not df.empty:
        extrema_detector = ExtremaDetector(order=5)
        extrema = extrema_detector.find_extrema(df['Close'])
        
        pattern_detector = PatternDetector(tolerance_pct=0.03)
        double_tops = pattern_detector.find_double_top(extrema['peaks'], extrema['troughs'])
        hs_patterns = pattern_detector.find_head_and_shoulders(extrema['peaks'], extrema['troughs'])
        
        all_patterns = double_tops + hs_patterns
        logger.info(f"{ticker} - Bulunan İkili Tepe: {len(double_tops)}, OBO: {len(hs_patterns)}")
        
        if all_patterns:
            simulator = Simulator(initial_capital=10000.0, tp_pct=0.05, sl_pct=0.03)
            results = simulator.run_backtest(df, all_patterns)
            logger.info(f"Simülasyon Win Rate: %{results['win_rate']}, PnL: %{results['pnl_pct']}, Final Bakiye: {results['final_capital']} TL")

    # 2. Canlı Tarama (Live Scanner Mode)
    logger.info("\n--- MOD 2: Canlı Piyasa Taraması (Live Scanner) ---")
    # Taranacak örnek bir BIST havuzu
    bist_pool = ["THYAO", "GARAN", "KCHOL", "TUPRS", "AKBNK"]
    
    # Son 5 gün içindeki formasyonları "Canlı/Aktif" kabul et
    scanner = LiveScanner(recent_bars=5)
    live_reports = scanner.scan_market(bist_pool)
    
    if live_reports:
        logger.info("\n>>> AKTİF FORMASYON RAPORLARI <<<")
        for report in live_reports:
            logger.info(f"[{report['ticker']} - {report['date']}]")
            logger.info(f"Yön: {report['direction']}")
            logger.info(f"Mesaj: {report['report']}\n")
    else:
        logger.info("\nŞu anki aktif piyasada takip edilen hisselerde güncel bir formasyon tespit edilemedi.")

    logger.info("=======================================")
    logger.info("       FormoCast İşlemleri Tamamlandı      ")
    logger.info("=======================================")

if __name__ == "__main__":
    main()
