from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from src.scanner.live_scanner import LiveScanner
import os

app = FastAPI(title="FormoCast API")

# Takip edilen hisse havuzu (Genişletilebilir)
BIST_POOL = ["THYAO", "GARAN", "KCHOL", "TUPRS", "AKBNK", "EREGL", "BIMAS", "SAHOL", "SISE", "ASELS"]

@app.get("/api/scan")
def scan_market():
    """Belirli hisse havuzunu tarar ve aktif formasyonları JSON olarak döner."""
    scanner = LiveScanner(recent_bars=5)
    live_reports = scanner.scan_market(BIST_POOL)
    return {"status": "success", "data": live_reports}

# Frontend klasörünün yolu
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frontend')

# Statik dosyaları sunmak için (CSS, JS) mount işlemi
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

@app.get("/")
def read_index():
    """Kök dizine girildiğinde index.html sayfasını döndürür."""
    return FileResponse(os.path.join(frontend_dir, 'index.html'))
