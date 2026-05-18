import pandas as pd
from typing import List, Dict, Any
from src.utils.logger import logger

class Simulator:
    """
    Tespit edilen formasyonların üzerinde geriye dönük (backtest) işlem
    simülasyonu yaparak başarı oranlarını ve kâr/zarar durumunu hesaplar.
    """
    
    def __init__(self, initial_capital: float = 10000.0, tp_pct: float = 0.05, sl_pct: float = 0.03):
        """
        Simülatörü başlatır.
        
        Parametreler:
            initial_capital (float): Başlangıç sermayesi (Örn: X TL yatırılsaydı).
            tp_pct (float): Kar al (Take-Profit) yüzdesi (Örn: 0.05 -> %5 kar).
            sl_pct (float): Zarar kes (Stop-Loss) yüzdesi (Örn: 0.03 -> %3 zarar).
        """
        self.initial_capital = initial_capital
        self.current_capital = initial_capital
        self.tp_pct = tp_pct
        self.sl_pct = sl_pct
        
    def run_backtest(self, df: pd.DataFrame, patterns: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Verilen veri seti ve formasyon listesi üzerinde simülasyon çalıştırır.
        Formasyonun bittiği gün (end_idx) ertesi gün işleme girildiği varsayılır.
        
        Parametreler:
            df (pd.DataFrame): Fiyat verisi ('Close', 'High', 'Low' içermeli).
            patterns (List[Dict]): Tespit edilen formasyonların listesi.
            
        Dönüş:
            Dict: Simülasyon sonuçlarını (Kâr, Win Rate vb.) içeren sözlük.
        """
        if not patterns:
            logger.warning("ERR-SIM-001: Simülasyon için herhangi bir formasyon bulunamadı.")
            return {
                "initial_capital": self.initial_capital,
                "final_capital": self.initial_capital,
                "total_trades": 0,
                "win_rate": 0.0,
                "pnl_pct": 0.0
            }
            
        wins = 0
        losses = 0
        trade_logs = []
        
        for pattern in patterns:
            # Formasyon end_idx'te tamamlanıyor.
            entry_idx = pattern['end_idx'] + 1
            
            # Eğer formasyon verinin en son günüyse işleme giremeyiz
            if entry_idx >= len(df):
                continue
                
            entry_price = df['Close'].iloc[entry_idx]
            
            # Yön varsayımı: Burada Double Top / OBO için "Düşüş" (Short) da olabilir.
            # Ancak BIST spot piyasası genelde "Long" yönlüdür.
            # Şimdilik örnek olarak formasyon oluşumunda yükseliş beklentisi (Long) olarak simüle edelim.
            # (Gelecekte formasyon tipine göre yön belirlenebilir).
            
            target_price = entry_price * (1 + self.tp_pct)
            stop_price = entry_price * (1 - self.sl_pct)
            
            # Gelecekteki günleri tara (İşleme girdikten sonra ne oldu?)
            trade_result = None
            exit_price = 0.0
            
            for i in range(entry_idx + 1, len(df)):
                current_high = df['High'].iloc[i]
                current_low = df['Low'].iloc[i]
                
                if current_low <= stop_price:
                    trade_result = 'LOSS'
                    exit_price = stop_price
                    losses += 1
                    break
                elif current_high >= target_price:
                    trade_result = 'WIN'
                    exit_price = target_price
                    wins += 1
                    break
            
            # Eğer veri bittiğinde işlem kapanmadıysa, son gün fiyatından kapatılır
            if trade_result is None:
                exit_price = df['Close'].iloc[-1]
                if exit_price > entry_price:
                    trade_result = 'WIN (Unclosed)'
                    wins += 1
                else:
                    trade_result = 'LOSS (Unclosed)'
                    losses += 1
                    
            # Sermayeyi güncelle (Tam bakiye ile işleme girildiği varsayımı)
            pct_change = (exit_price - entry_price) / entry_price
            self.current_capital = self.current_capital * (1 + pct_change)
            
            trade_logs.append({
                "pattern": pattern['type'],
                "entry_price": entry_price,
                "exit_price": exit_price,
                "result": trade_result,
                "capital_after": self.current_capital
            })
            
        total_trades = wins + losses
        win_rate = (wins / total_trades) * 100 if total_trades > 0 else 0.0
        pnl_pct = ((self.current_capital - self.initial_capital) / self.initial_capital) * 100
        
        logger.info(f"Simülasyon tamamlandı. İşlem: {total_trades}, Win Rate: %{win_rate:.2f}, PnL: %{pnl_pct:.2f}")
        
        return {
            "initial_capital": self.initial_capital,
            "final_capital": round(self.current_capital, 2),
            "total_trades": total_trades,
            "win_rate": round(win_rate, 2),
            "pnl_pct": round(pnl_pct, 2),
            "logs": trade_logs
        }
