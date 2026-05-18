import pytest
import pandas as pd
import numpy as np
from src.pattern_recognition.extrema import ExtremaDetector

@pytest.fixture
def detector():
    # Daha hassas bir tepe/dip bulma için order=1 veriyoruz ki test verimizde kolay yakalasın
    return ExtremaDetector(order=1)

@pytest.fixture
def sample_price_series():
    """Belirgin tepe ve dipleri olan basit bir fiyat serisi (11 elemanlı).
       İndeksler: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
       Fiyatlar:  10, 15, 20, 15, 10,  5, 10, 15, 10,  5, 10
       Beklenen Tepe (Peak): indeks 2 (fiyat 20), indeks 7 (fiyat 15)
       Beklenen Dip (Trough): indeks 5 (fiyat 5)
    """
    data = [10, 15, 20, 15, 10, 5, 10, 15, 10, 5, 10]
    return pd.Series(data)

def test_find_extrema_success(detector, sample_price_series):
    """Belirgin tepe ve dipleri doğru tespit ettiğini doğrular."""
    result = detector.find_extrema(sample_price_series)
    
    assert 'peaks' in result
    assert 'troughs' in result
    
    # peaks: list of tuples (index, value)
    peaks = result['peaks']
    troughs = result['troughs']
    
    # indeks 2 (20), indeks 7 (15) tepe noktalarıdır
    assert (2, 20.0) in peaks
    assert (7, 15.0) in peaks
    
    # indeks 5 (5) ve 9 (5) dip noktalarıdır
    assert (5, 5.0) in troughs
    assert (9, 5.0) in troughs

def test_find_extrema_empty_series(detector):
    """Boş seri gönderildiğinde boş dictionary döneceğini doğrular (Hata kodu: ERR-PTRN-001)."""
    empty_series = pd.Series(dtype=float)
    result = detector.find_extrema(empty_series)
    
    assert result['peaks'] == []
    assert result['troughs'] == []

def test_find_extrema_flat_series(detector):
    """Yatay (tepesiz, dipsiz) bir seride uyarı vereceğini ve boş liste döneceğini doğrular."""
    flat_series = pd.Series([10, 10, 10, 10, 10])
    result = detector.find_extrema(flat_series)
    
    assert len(result['peaks']) == 0
    assert len(result['troughs']) == 0
