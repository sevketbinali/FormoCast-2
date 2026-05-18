# Hafif Python imajı taban alınmıştır
FROM python:3.10-slim

# Çalışma dizini ayarı
WORKDIR /app

# Sistem bağımlılıkları (scipy, numpy, pandas derleme gereksinimleri için)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Gereksinimlerin kopyalanması
COPY requirements.txt .

# Bağımlılıkların yüklenmesi
RUN pip install --no-cache-dir -r requirements.txt

# Kaynak kodların kopyalanması
COPY . .

# Çevresel değişken (Python module search path için)
ENV PYTHONPATH=/app

# Uygulamanın varsayılan başlatma komutu
# Şu an main.py boş ancak sistemin temel noktasını temsil ediyor.
CMD ["python", "main.py"]
