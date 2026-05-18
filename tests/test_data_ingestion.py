import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from src.data_ingestion.fetcher import BISTDataFetcher

@pytest.fixture
def fetcher():
    """BISTDataFetcher sınıfının bir örneğini oluşturur."""
    return BISTDataFetcher()

@pytest.fixture
def mock_valid_df():
    """Geçerli bir pandas DataFrame kopyası oluşturur."""
    data = {
        'Open': [10.0, 10.5],
        'High': [11.0, 11.5],
        'Low': [9.0, 9.5],
        'Close': [10.8, 11.2],
        'Volume': [1000, 1500]
    }
    return pd.DataFrame(data, index=pd.date_range(start='2023-01-01', periods=2))

@pytest.fixture
def mock_invalid_df():
    """Gerekli kolonların eksik olduğu hatalı bir DataFrame oluşturur."""
    data = {
        'Open': [10.0, 10.5],
        'Close': [10.8, 11.2]
        # High, Low, Volume kolonları eksik
    }
    return pd.DataFrame(data, index=pd.date_range(start='2023-01-01', periods=2))

@patch('src.data_ingestion.fetcher.yf.Ticker')
def test_fetch_historical_data_success(mock_ticker, fetcher, mock_valid_df):
    """Geçerli veri döndüğünde fonksiyonun DataFrame döndürdüğünü doğrular."""
    # Mock ayarı
    mock_instance = MagicMock()
    mock_instance.history.return_value = mock_valid_df
    mock_ticker.return_value = mock_instance
    
    # Test yürütme
    result = fetcher.fetch_historical_data("THYAO")
    
    # Doğrulama
    assert result is not None
    assert isinstance(result, pd.DataFrame)
    assert not result.empty
    assert list(result.columns) == ['Open', 'High', 'Low', 'Close', 'Volume']
    # ".IS" ekinin otomatik eklendiğini kontrol et
    mock_ticker.assert_called_with("THYAO.IS")

@patch('src.data_ingestion.fetcher.yf.Ticker')
def test_fetch_historical_data_empty_return(mock_ticker, fetcher):
    """Veri kaynağı boş DataFrame döndürdüğünde sistemin None dönmesini doğrular."""
    mock_instance = MagicMock()
    mock_instance.history.return_value = pd.DataFrame() # Boş veri
    mock_ticker.return_value = mock_instance
    
    result = fetcher.fetch_historical_data("BOS_HISSE")
    
    assert result is None

@patch('src.data_ingestion.fetcher.yf.Ticker')
def test_fetch_historical_data_missing_columns(mock_ticker, fetcher, mock_invalid_df):
    """Gelen veride eksik kolonlar olduğunda ERR-DATA-002 hatası alınmalı ve None dönmelidir."""
    mock_instance = MagicMock()
    mock_instance.history.return_value = mock_invalid_df
    mock_ticker.return_value = mock_instance
    
    result = fetcher.fetch_historical_data("THYAO")
    
    assert result is None

@patch('src.data_ingestion.fetcher.yf.Ticker')
def test_fetch_historical_data_with_is_suffix(mock_ticker, fetcher, mock_valid_df):
    """Eğer kullanıcı ".IS" ekini zaten girmişse tekrar eklememesini doğrular."""
    mock_instance = MagicMock()
    mock_instance.history.return_value = mock_valid_df
    mock_ticker.return_value = mock_instance
    
    fetcher.fetch_historical_data("GARAN.IS")
    
    mock_ticker.assert_called_with("GARAN.IS")
