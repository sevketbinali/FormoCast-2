import logging
import sys

def setup_logger(name: str = "FormoCast") -> logging.Logger:
    """
    FormoCast projesi için merkezi loglama yapılandırmasını oluşturur.
    Console çıktısı ve dosya çıktısı olarak iki yönlü loglama yapar.
    Hata mesajları `knowledge.md` standartlarına uygun formatlanır.
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        
        # Log formatı (Tarih - Seviye - Mesaj)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Konsol Handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        
        # Log Dosyası Handler
        file_handler = logging.FileHandler('formocast.log', encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        
    return logger

# Tüm proje genelinde kullanılacak ortak logger nesnesi
logger = setup_logger()
