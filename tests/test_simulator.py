import pytest
import pandas as pd
from src.backtesting.simulator import Simulator

@pytest.fixture
def sample_df():
    """Simülasyon testleri için fiyat verisi oluşturur."""
    data = {
        'Close': [100, 105, 110, 100, 105, 115, 120, 130],
        'High':  [102, 106, 112, 105, 108, 118, 125, 135],
        'Low':   [98,  100, 108, 95,  100, 110, 115, 125]
    }
    return pd.DataFrame(data)

@pytest.fixture
def simulator():
    # %10 kar al, %5 zarar kes, 10,000 TL başlangıç
    return Simulator(initial_capital=10000.0, tp_pct=0.10, sl_pct=0.05)

def test_run_backtest_no_patterns(simulator, sample_df):
    """Hiç formasyon olmadığında sermayenin değişmediğini test eder (ERR-SIM-001 tetiklenir)."""
    result = simulator.run_backtest(sample_df, [])
    
    assert result['total_trades'] == 0
    assert result['final_capital'] == 10000.0

def test_run_backtest_with_win(simulator, sample_df):
    """TP (Kar al) hedefine ulaşan başarılı bir işlemi test eder."""
    # Varsayalım ki formasyon 2. indekste bitti. Giriş 3. indekste (fiyat: 100) olacak.
    patterns = [{'type': 'Test Pattern', 'end_idx': 2}]
    
    result = simulator.run_backtest(sample_df, patterns)
    
    # Giriş fiyatı: 100. %10 kar hedefi = 110. 
    # Sonraki barlarda High 118'e kadar çıkıyor, yani hedefe ulaşıyor.
    assert result['total_trades'] == 1
    assert result['win_rate'] == 100.0
    assert result['final_capital'] > 10000.0
    assert result['logs'][0]['result'] == 'WIN'

def test_run_backtest_with_loss(simulator):
    """SL (Zarar kes) hedefine ulaşan başarısız bir işlemi test eder."""
    data = {
        'Close': [100, 105, 110, 100, 90, 80],
        'High':  [102, 106, 112, 102, 95, 85],
        'Low':   [98,  100, 108, 98,  88, 78]
    }
    df = pd.DataFrame(data)
    
    patterns = [{'type': 'Test Pattern', 'end_idx': 2}]
    
    result = simulator.run_backtest(df, patterns)
    
    # Giriş 3. indekste (fiyat: 100). %5 zarar kes = 95.
    # 4. barın Low değeri 88. Yani SL patlar.
    assert result['total_trades'] == 1
    assert result['win_rate'] == 0.0
    assert result['final_capital'] < 10000.0
    assert result['logs'][0]['result'] == 'LOSS'
