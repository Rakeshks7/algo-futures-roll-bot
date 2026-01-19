import asyncio
from broker_connector import MockBroker
from strategy import RollStrategy
from config import REFRESH_RATE

async def main():
    print("--- STARTING ROLL BOT [PRODUCTION MODE] ---")

    broker = MockBroker()
    bot = RollStrategy(broker)
    
    bot.running = True

    while bot.running:
        traded = await bot.run_cycle()
        
        if traded:
            print("--- ROLL COMPLETE. SHUTTING DOWN ---")
            break
            
        await asyncio.sleep(REFRESH_RATE)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped by user.")