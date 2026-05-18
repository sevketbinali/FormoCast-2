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
        found_patterns = []
        if len(peaks) < 2:
            return found_patterns
            
        for i in range(len(peaks) - 1):
            p1_idx, p1_price = peaks[i]
            p2_idx, p2_price = peaks[i+1]
            
            if self._is_same_level(p1_price, p2_price):
                intermediate_troughs = [t for t in troughs if p1_idx < t[0] < p2_idx]
                if intermediate_troughs:
                    neckline_trough = min(intermediate_troughs, key=lambda x: x[1])
                    neck_idx, neck_price = neckline_trough
                    
                    if neck_price < p1_price * (1 - self.tolerance_pct):
                        height = p1_price - neck_price
                        target_price = neck_price - height
                        pattern_duration = p2_idx - p1_idx
                        
                        pattern = {
                            "type": "Double Top",
                            "start_idx": p1_idx,
                            "end_idx": p2_idx,
                            "detection_price": p2_price,
                            "direction": "DÜŞÜŞ",
                            "target_price": target_price,
                            "target_bars_added": pattern_duration,
                            "peak1": (p1_idx, p1_price),
                            "peak2": (p2_idx, p2_price),
                            "neckline": (neck_idx, neck_price)
                        }
                        found_patterns.append(pattern)
        return found_patterns

    def find_head_and_shoulders(self, peaks: List[tuple], troughs: List[tuple]) -> List[Dict[str, Any]]:
        found_patterns = []
        if len(peaks) < 3:
            return found_patterns
            
        for i in range(len(peaks) - 2):
            ls_idx, ls_price = peaks[i]       
            h_idx, h_price = peaks[i+1]       
            rs_idx, rs_price = peaks[i+2]     
            
            if self._is_same_level(ls_price, rs_price):
                if h_price > ls_price * (1 + self.tolerance_pct) and h_price > rs_price * (1 + self.tolerance_pct):
                    left_troughs = [t for t in troughs if ls_idx < t[0] < h_idx]
                    right_troughs = [t for t in troughs if h_idx < t[0] < rs_idx]
                    
                    if left_troughs and right_troughs:
                        left_neck = min(left_troughs, key=lambda x: x[1])
                        right_neck = min(right_troughs, key=lambda x: x[1])
                        avg_neck_price = (left_neck[1] + right_neck[1]) / 2
                        
                        height = h_price - avg_neck_price
                        target_price = avg_neck_price - height
                        pattern_duration = rs_idx - ls_idx

                        pattern = {
                            "type": "Head and Shoulders",
                            "start_idx": ls_idx,
                            "end_idx": rs_idx,
                            "detection_price": rs_price,
                            "direction": "DÜŞÜŞ",
                            "target_price": target_price,
                            "target_bars_added": pattern_duration,
                            "left_shoulder": (ls_idx, ls_price),
                            "head": (h_idx, h_price),
                            "right_shoulder": (rs_idx, rs_price)
                        }
                        found_patterns.append(pattern)
        return found_patterns
