import pandas as pd
import numpy as np
from scipy.signal import argrelextrema
from src.utils.logger import logger

class ExtremaDetector:
    """
    Fiyat verileri üzerinde yerel tepe (peak) ve dip (trough) noktalarını 
    tespit etmekten sorumlu sınıf.
    """
    
    def __init__(self, order: int = 5):
        """
        ExtremaDetector sınıfının başlatılması.
        
        Parametreler:
            order (int): scipy.signal.argrelextrema için 'order' parametresi. 
                         Kaç bar sağına ve soluna bakılacağını belirler. 
                         Daha yüksek order, daha az ve belirgin tepe/dip bulur.
        """
        self.order = order

    def find_extrema(self, series: pd.Series) -> dict:
        """
        Verilen bir fiyat serisi (örn. 'Close' fiyatları) üzerinde tepe ve dip noktalarını bulur.
        
        Parametreler:
            series (pd.Series): Tepe/dip noktalarının aranacağı fiyat serisi.
            
        Dönüş:
            dict: 'peaks' ve 'troughs' (tepeler ve dipler) anahtarlarına sahip,
                  her biri [indeks_listesi, fiyat_listesi] içeren bir sözlük döner.
        """
        try:
            if series is None or series.empty:
                logger.error("ERR-PTRN-001: Ekstremum bulmak için gönderilen veri serisi boş.")
                return {'peaks': [], 'troughs': []}
                
            data = series.values
            
            # Yerel maksimumları (tepeler) bulma
            local_max = argrelextrema(data, np.greater, order=self.order)[0]
            # Yerel minimumları (dipler) bulma
            local_min = argrelextrema(data, np.less, order=self.order)[0]
            
            if len(local_max) == 0 and len(local_min) == 0:
                logger.warning("ERR-PTRN-001: Verilen parametrelerle hiçbir tepe veya dip bulunamadı. Order çok yüksek olabilir.")
                
            peaks = [(int(idx), float(data[idx])) for idx in local_max]
            troughs = [(int(idx), float(data[idx])) for idx in local_min]
            
            return {
                'peaks': peaks,
                'troughs': troughs
            }
            
        except Exception as e:
            logger.error(f"ERR-PTRN-001: Ekstremum noktaları hesaplanırken beklenmeyen bir hata oluştu: {str(e)}")
            return {'peaks': [], 'troughs': []}
