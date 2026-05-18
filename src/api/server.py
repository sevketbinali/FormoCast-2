from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from src.scanner.live_scanner import LiveScanner
from src.data_ingestion.fetcher import BISTDataFetcher
from src.pattern_recognition.extrema import ExtremaDetector
from src.pattern_recognition.patterns import PatternDetector
import os

app = FastAPI(title="FormoCast API")

# Takip edilen hisse havuzu (BIST 30)
BIST_POOL = [
    "AKBNK", "ALARK", "ASELS", "ASTOR", "BIMAS", "BRSAN", "CINFO", "ENKAI", 
    "EREGL", "FROTO", "GARAN", "GUBRF", "HEKTS", "ISCTR", "KCHOL", "KONTR",
    "KOZAA", "KOZAL", "KRDMD", "ODAS", "PGSUS", "SAHOL", "SASA", "SISE", 
    "TCELL", "THYAO", "TOASO", "TUPRS", "YKBNK", "PETKM"
]

@app.get("/api/tickers")
def get_tickers():
    return {"status": "success", "data": BIST_POOL}

@app.get("/api/history/{ticker}")
def get_history(ticker: str):
    """Belirli bir hisse için geçmiş formasyonları ve tahmin detaylarını getirir (Son 20 yıl)"""
    fetcher = BISTDataFetcher()
    # 20 yıllık veriyi al
    df = fetcher.fetch_historical_data(ticker, period="20y")
    if df is None or df.empty:
        return {"status": "error", "message": "Veri çekilemedi."}
        
    prices = df['Close'].values
    dates = df.index.strftime('%Y-%m-%d').tolist()
    
    extrema_detector = ExtremaDetector()
    extrema_data = extrema_detector.find_extrema(df['Close'])
    peaks = extrema_data['peaks']
    troughs = extrema_data['troughs']
    
    pattern_detector = PatternDetector(tolerance_pct=0.03)
    double_tops = pattern_detector.find_double_top(peaks, troughs)
    head_and_shoulders = pattern_detector.find_head_and_shoulders(peaks, troughs)
    
    all_patterns = double_tops + head_and_shoulders
    
    # Tarih maplemelerini yap
    enriched_patterns = []
    for p in all_patterns:
        start_idx = p["start_idx"]
        end_idx = p["end_idx"]
        target_idx = min(end_idx + p["target_bars_added"], len(dates) - 1)
        
        enriched_patterns.append({
            "type": p["type"],
            "direction": p["direction"],
            "detection_date": dates[end_idx],
            "detection_price": p["detection_price"],
            "target_price": p["target_price"],
            "target_date": dates[target_idx],
            "start_date": dates[start_idx],
            "end_date": dates[end_idx]
        })
    
    # Chart için mum verisini hazırla (Lightweight Charts formatı)
    candles = []
    for index, row in df.iterrows():
        candles.append({
            "time": index.strftime('%Y-%m-%d'),
            "open": row["Open"],
            "high": row["High"],
            "low": row["Low"],
            "close": row["Close"]
        })
        
    return {
        "status": "success",
        "ticker": ticker,
        "patterns": enriched_patterns,
        "candles": candles
    }

# Frontend klasörünün yolu
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frontend')

# Statik dosyaları sunmak için (CSS, JS) mount işlemi
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

@app.get("/")
def read_index():
    return FileResponse(os.path.join(frontend_dir, 'index.html'))
