from abc import ABC, abstractmethod
import asyncio
import random

class BrokerInterface(ABC):
    @abstractmethod
    async def get_market_data(self, symbol: str):
        pass

    @abstractmethod
    async def place_combo_order(self, leg1, leg2, action1, action2, qty):
        pass

    @abstractmethod
    async def place_market_order(self, symbol, action, qty):
        pass

class MockBroker(BrokerInterface):
    async def get_market_data(self, symbol: str):
        base_price = 1000 if "DEC" in symbol else 1005
        noise = random.uniform(-0.5, 0.5)
        price = base_price + noise
        return {
            "symbol": symbol,
            "bid": price - 0.05,
            "ask": price + 0.05,
            "last": price
        }

    async def place_combo_order(self, leg1, leg2, action1, action2, qty):
        print(f"[EXCHANGE] ATOMIC ORDER PLACED: {action1} {leg1} / {action2} {leg2} | Qty: {qty}")
        return {"status": "FILLED", "id": "ORDER_123"}

    async def place_market_order(self, symbol, action, qty):
        print(f"[EXCHANGE] MARKET ORDER: {action} {symbol} | Qty: {qty}")
        return {"status": "FILLED"}