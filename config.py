import os
from dataclasses import dataclass

@dataclass
class InstrumentConfig:
    symbol_near: str  
    symbol_far: str   
    exchange_symbol: str 
    
@dataclass
class RiskConfig:
    max_slippage_pct: float = 0.001  
    max_qty: int = 50                
    interest_rate: float = 0.05      
    dividend_yield: float = 0.00     
    spread_threshold: float = 0.05   

API_KEY = os.getenv("BROKER_API_KEY", "your_key_here")
API_SECRET = os.getenv("BROKER_API_SECRET", "your_secret_here")
REFRESH_RATE = 1.0  # Seconds between ticks (if polling)

INSTRUMENT = InstrumentConfig(
    symbol_near='FUT-DEC',
    symbol_far='FUT-JAN',
    exchange_symbol='XYZ-INDEX'
)

RISK = RiskConfig()