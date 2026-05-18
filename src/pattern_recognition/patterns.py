import pandas as pd
from typing import List, Dict, Any
from src.pattern_recognition.extrema import ExtremaDetector
from src.utils.logger import logger

class PatternDetector:
    """
    Fiyat grafiği üzerindeki extrema noktalarını (tepe ve dip) baz alarak,
    spesifik teknik formasyonları (Örn: İkili Tepe, Omuz Baş Omuz) tespit eder.
    """
    
    def __init__(self, tolerance_pct: float = 0.03):
        """
        PatternDetector sınıfının başlatılması.
        
        Parametreler:
            tolerance_pct (float): Fiyat seviyelerindeki esneklik/hata payı yüzdesi.
                                   Örneğin 0.03 değeri %3'lük bir farklılığın aynı seviye
                                   kabul edileceğini gösterir.
        """
        self.tolerance_pct = tolerance_pct
        
    def _is_same_level(self, price1: float, price2: float) -> bool:
        """İki fiyatın belirlenen tolerans aralığında aynı seviyede olup olmadığını kontrol eder."""
        diff = abs(price1 - price2)
        avg_price = (price1 + price2) / 2
        return (diff / avg_price) <= self.tolerance_pct

    def find_double_top(self, peaks: List[tuple], troughs: List[tuple]) -> List[Dict[str, Any]]:
        """
        Grafikteki 'İkili Tepe' (Double Top) formasyonlarını arar.
        Kural: Yaklaşık aynı seviyede iki tepe ve aralarında belirgin bir dip noktası olmalıdır.
        
        Dönüş:
            Bulunan formasyonların listesi (her biri sözlük formatında).
        """
        found_patterns = []
        
        # En az 2 tepeye ihtiyacımız var
        if len(peaks) < 2:
            return found_patterns
            
        for i in range(len(peaks) - 1):
            p1_idx, p1_price = peaks[i]
            p2_idx, p2_price = peaks[i+1]
            
            # 1. Kural: İki tepe aynı seviyede mi?
            if self._is_same_level(p1_price, p2_price):
                
                # 2. Kural: İki tepe arasında bir dip noktası (trough) olmalı
                intermediate_troughs = [t for t in troughs if p1_idx < t[0] < p2_idx]
                
                if intermediate_troughs:
                    # En düşük dip noktasını boyun çizgisi (neckline) olarak al
                    neckline_trough = min(intermediate_troughs, key=lambda x: x[1])
                    neck_idx, neck_price = neckline_trough
                    
                    # 3. Kural: Dip noktası tepelerden gerçekten aşağıda mı? (Örn: En az tolerans kadar düşmüş mü)
                    if neck_price < p1_price * (1 - self.tolerance_pct):
                        pattern = {
                            "type": "Double Top",
                            "start_idx": p1_idx,
                            "end_idx": p2_idx,
                            "peak1": (p1_idx, p1_price),
                            "peak2": (p2_idx, p2_price),
                            "neckline": (neck_idx, neck_price)
                        }
                        found_patterns.append(pattern)
                        
        return found_patterns

    def find_head_and_shoulders(self, peaks: List[tuple], troughs: List[tuple]) -> List[Dict[str, Any]]:
        """
        Grafikteki 'Omuz Baş Omuz' (Head and Shoulders - OBO) formasyonlarını arar.
        Kural: Sol omuz ve sağ omuz benzer seviyede, Baş (Head) bunlardan daha yüksekte olmalıdır.
        
        Dönüş:
            Bulunan formasyonların listesi.
        """
        found_patterns = []
        
        # En az 3 tepeye ihtiyacımız var
        if len(peaks) < 3:
            return found_patterns
            
        for i in range(len(peaks) - 2):
            ls_idx, ls_price = peaks[i]       # Left Shoulder (Sol Omuz)
            h_idx, h_price = peaks[i+1]       # Head (Baş)
            rs_idx, rs_price = peaks[i+2]     # Right Shoulder (Sağ Omuz)
            
            # 1. Kural: Sol omuz ve sağ omuz aynı hizada mı?
            if self._is_same_level(ls_price, rs_price):
                
                # 2. Kural: Baş (Head), her iki omuzdan da yüksek olmalı
                if h_price > ls_price * (1 + self.tolerance_pct) and h_price > rs_price * (1 + self.tolerance_pct):
                    
                    # 3. Kural: Omuzlar ve baş arasında boyun çizgisi (dipler) olmalı
                    left_troughs = [t for t in troughs if ls_idx < t[0] < h_idx]
                    right_troughs = [t for t in troughs if h_idx < t[0] < rs_idx]
                    
                    if left_troughs and right_troughs:
                        pattern = {
                            "type": "Head and Shoulders",
                            "start_idx": ls_idx,
                            "end_idx": rs_idx,
                            "left_shoulder": (ls_idx, ls_price),
                            "head": (h_idx, h_price),
                            "right_shoulder": (rs_idx, rs_price)
                        }
                        found_patterns.append(pattern)
                        
        return found_patterns
