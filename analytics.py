import numpy as np
from datetime import datetime

class AnalyticsEngine:
    
    @staticmethod
    def calculate_time_to_expiry(expiry_date: str) -> float:
        exp = datetime.strptime(expiry_date, "%Y-%m-%d")
        now = datetime.now()
        days = (exp - now).days
        return max(days / 365.0, 0.001) 

    @staticmethod
    def calculate_fair_spread(spot_price: float, 
                              time_near: float, 
                              time_far: float, 
                              r: float, 
                              q: float = 0.0) -> float:
        fair_near = spot_price * np.exp((r - q) * time_near)
        fair_far = spot_price * np.exp((r - q) * time_far)
        
        return fair_near - fair_far

    @staticmethod
    def get_live_spread(bid_near, ask_near, bid_far, ask_far):
        execution_spread = bid_near - ask_far
        return execution_spread