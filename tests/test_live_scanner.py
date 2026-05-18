import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from src.scanner.live_scanner import LiveScanner

@pytest.fixture
def scanner():
    return LiveScanner(recent_bars=3)

@pytest.fixture
def mock_df():
    """10 satırlık basit bir DataFrame (index 9 son bar)"""
    data = {
        'Close': [10, 20, 10, 20, 10, 20, 10, 20, 10, 20],
        'High':  [11, 21, 11, 21, 11, 21, 11, 21, 11, 21],
        'Low':   [9,  19, 9,  19, 9,  19, 9,  19, 9,  19]
    }
    dates = pd.date_range(start='2023-01-01', periods=10)
    return pd.DataFrame(data, index=dates)

@patch('src.scanner.live_scanner.BISTDataFetcher.fetch_historical_data')
@patch('src.scanner.live_scanner.ExtremaDetector.find_extrema')
@patch('src.scanner.live_scanner.PatternDetector.find_double_top')
@patch('src.scanner.live_scanner.Simulator.run_backtest')
def test_scan_market_live_pattern(mock_sim, mock_dt, mock_ext, mock_fetch, scanner, mock_df):
    """
    Son barlarda (recent_bars) gerçekleşen formasyonların 
    başarılı bir şekilde tespit edilip raporlandığını doğrular.
    """
    mock_fetch.return_value = mock_df
    mock_ext.return_value = {'peaks': [], 'troughs': []}
    
    # 10 satırlık veride (0-9 index), end_idx=8 olan bir formasyon 
    # recent_bars=3 içine girer (10 - 8 = 2 <= 3)
    mock_dt.return_value = [{'type': 'Double Top', 'end_idx': 8}]
    
    mock_sim.return_value = {'win_rate': 75.5}
    
    reports = scanner.scan_market(["TEST"])
    
    assert len(reports) == 1
    assert reports[0]['ticker'] == "TEST"
    assert reports[0]['pattern'] == "Double Top"
    assert "DÜŞÜŞ" in reports[0]['report']
    assert "%75.50" in reports[0]['report']

@patch('src.scanner.live_scanner.BISTDataFetcher.fetch_historical_data')
@patch('src.scanner.live_scanner.PatternDetector.find_double_top')
def test_scan_market_old_pattern(mock_dt, mock_fetch, scanner, mock_df):
    """Eski formasyonların (recent_bars dışında kalan) canlı sinyal olarak algılanmadığını test eder."""
    mock_fetch.return_value = mock_df
    
    # end_idx=2 (10 - 2 = 8 > 3 recent_bars) yani eski bir formasyon
    mock_dt.return_value = [{'type': 'Double Top', 'end_idx': 2}]
    
    reports = scanner.scan_market(["TEST"])
    
    # Geçmiş bir formasyon olduğu için canlı rapor oluşturulmamalı
    assert len(reports) == 0
