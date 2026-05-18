import yfinance as yf
import pandas as pd
from typing import Optional
from src.utils.logger import logger

class BISTDataFetcher:
    """
    Borsa İstanbul (BIST) hisselerinin geçmiş fiyat verilerini çekmekten 
    sorumlu veri sağlayıcı sınıf.
    """
    
    def __init__(self):
        """
        DataFetcher sınıfının başlatılması.
        """
        pass

    def fetch_historical_data(self, ticker: str, period: str = "1y", interval: str = "1d") -> Optional[pd.DataFrame]:
        """
        Belirtilen BIST hissesi için OHLCV (Açılış, Yüksek, Düşük, Kapanış, Hacim) verilerini çeker.
        
        Parametreler:
            ticker (str): Hisse senedi sembolü (örn. "THYAO")
            period (str): Çekilecek veri periyodu (örn. "1y" 1 yıl, "6mo" 6 ay)
            interval (str): Veri aralığı (örn. "1d" günlük, "1h" saatlik)
            
        Dönüş:
            pd.DataFrame: Temizlenmiş fiyat verileri. Hata durumunda None döner.
        """
        # BIST hisseleri için Yahoo Finance sembol sonuna ".IS" eklenmesi gerekir
        if not ticker.endswith(".IS"):
            ticker = f"{ticker}.IS"
            
        try:
            logger.info(f"'{ticker}' için veri çekiliyor. Periyot: {period}, Aralık: {interval}")
            stock = yf.Ticker(ticker)
            df = stock.history(period=period, interval=interval)
            
            if df is None or df.empty:
                logger.error(f"ERR-DATA-001: '{ticker}' için veri kaynağına ulaşılamadı veya veri boş döndü.")
                return None
                
            # Veri formatı ve bütünlük kontrolü
            required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
            for col in required_cols:
                if col not in df.columns:
                    logger.error(f"ERR-DATA-002: '{ticker}' verisinde eksik kolon: {col}")
                    return None
                    
            # Eksik (NaN) değerlerin silinmesi (Temizlik)
            df.dropna(subset=required_cols, inplace=True)
            
            if df.empty:
                logger.error(f"ERR-DATA-002: '{ticker}' verisinde NaN temizliği sonrası veri kalmadı.")
                return None
                
            logger.info(f"'{ticker}' için veri başarıyla çekildi. Satır sayısı: {len(df)}")
            return df
            
        except Exception as e:
            logger.error(f"ERR-DATA-001: Veri kaynağına ulaşılamadı. Sembol: '{ticker}', Hata: {str(e)}")
            return None
