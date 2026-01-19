import asyncio
import logging
from analytics import AnalyticsEngine
from config import INSTRUMENT, RISK

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("RollBot")

class RollStrategy:
    def __init__(self, broker):
        self.broker = broker
        self.running = False
        self.expiry_near = "2026-12-26" 
        self.expiry_far = "2027-01-29"

    async def run_cycle(self):
        try:
            near_data, far_data = await asyncio.gather(
                self.broker.get_market_data(INSTRUMENT.symbol_near),
                self.broker.get_market_data(INSTRUMENT.symbol_far)
            )

            bid_near = near_data['bid']
            ask_far = far_data['ask']

            spot_est = (near_data['last'] + far_data['last']) / 2 

            t_near = AnalyticsEngine.calculate_time_to_expiry(self.expiry_near)
            t_far = AnalyticsEngine.calculate_time_to_expiry(self.expiry_far)

            fair_spread = AnalyticsEngine.calculate_fair_spread(
                spot_price=spot_est,
                time_near=t_near,
                time_far=t_far,
                r=RISK.interest_rate,
                q=RISK.dividend_yield
            )

            market_spread = bid_near - ask_far

            logger.info(f"Market Spread: {market_spread:.2f} | Fair Value: {fair_spread:.2f} | Delta: {market_spread - fair_spread:.2f}")

            
            if market_spread < fair_spread - RISK.spread_threshold:
                logger.info(">>> OPPORTUNITY DETECTED: Executing Roll <<<")
                await self.execute_roll(INSTRUMENT.symbol_near, INSTRUMENT.symbol_far, RISK.max_qty)
                return True # Signal that we traded

        except Exception as e:
            logger.error(f"Error in strategy cycle: {e}")
        
        return False

    async def execute_roll(self, near_sym, far_sym, qty):

        supports_combo = True 
        
        if supports_combo:
            logger.info("Sending Atomic Spread Order...")
            await self.broker.place_combo_order(near_sym, far_sym, "SELL", "BUY", qty)
        else:
            logger.warning("Atomic Unsupported. LEGGING IN (Simultaneous Market Orders).")
            # Fire both orders at once without awaiting sequentially to minimize latency
            await asyncio.gather(
                self.broker.place_market_order(near_sym, "SELL", qty),
                self.broker.place_market_order(far_sym, "BUY", qty)
            )
        
        self.running = False # Stop after execution (for safety in this demo)