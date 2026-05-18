import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from src.api.server import app

client = TestClient(app)

def test_read_index():
    """Ana sayfanın (HTML) başarıyla döndüğünü test eder."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "FormoCast" in response.text

@patch('src.api.server.LiveScanner.scan_market')
def test_scan_market_endpoint(mock_scan):
    """API endpoint'inin doğru JSON formatında döndüğünü test eder."""
    mock_scan.return_value = [
        {
            "ticker": "THYAO",
            "pattern": "Double Top",
            "win_rate": 75.5,
            "direction": "DÜŞÜŞ",
            "report": "Örnek rapor metni",
            "date": "2024-01-01"
        }
    ]
    
    response = client.get("/api/scan")
    assert response.status_code == 200
    data = response.json()
    
    assert data["status"] == "success"
    assert len(data["data"]) == 1
    assert data["data"][0]["ticker"] == "THYAO"
