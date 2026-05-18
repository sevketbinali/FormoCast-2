import pytest
from src.pattern_recognition.patterns import PatternDetector

@pytest.fixture
def detector():
    # %5 toleransla dedektörümüzü başlatıyoruz
    return PatternDetector(tolerance_pct=0.05)

def test_find_double_top(detector):
    """İkili Tepe (Double Top) tespitinin doğruluğunu test eder."""
    # İdeal bir ikili tepe: (idx, price)
    peaks = [(2, 100.0), (8, 98.0)] # %2 fark var, tolerans içinde (%5)
    troughs = [(5, 80.0)] # 80 < 98 * 0.95 (ok, dip tepeden baya düşük)
    
    patterns = detector.find_double_top(peaks, troughs)
    
    assert len(patterns) == 1
    assert patterns[0]['type'] == "Double Top"
    assert patterns[0]['start_idx'] == 2
    assert patterns[0]['end_idx'] == 8

def test_find_double_top_invalid_tolerance(detector):
    """Tepeler arası fark toleransın dışındaysa formasyon sayılmamalı."""
    peaks = [(2, 100.0), (8, 90.0)] # %10 fark var, %5 toleransın dışında
    troughs = [(5, 80.0)]
    
    patterns = detector.find_double_top(peaks, troughs)
    
    assert len(patterns) == 0 # Formasyon bulunmamalı

def test_find_head_and_shoulders(detector):
    """Omuz Baş Omuz (H&S) tespitinin doğruluğunu test eder."""
    # Sol omuz (100), Baş (120), Sağ omuz (102)
    peaks = [(2, 100.0), (5, 120.0), (8, 102.0)]
    troughs = [(3, 90.0), (7, 91.0)]
    
    patterns = detector.find_head_and_shoulders(peaks, troughs)
    
    assert len(patterns) == 1
    assert patterns[0]['type'] == "Head and Shoulders"
    assert patterns[0]['left_shoulder'][1] == 100.0
    assert patterns[0]['head'][1] == 120.0

def test_find_head_and_shoulders_invalid_head(detector):
    """Eğer Baş omuzlardan yüksek değilse formasyon olmamalı."""
    peaks = [(2, 100.0), (5, 95.0), (8, 102.0)] # Baş, omuzlardan düşük
    troughs = [(3, 90.0), (7, 91.0)]
    
    patterns = detector.find_head_and_shoulders(peaks, troughs)
    
    assert len(patterns) == 0
