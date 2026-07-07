import redis
import json

# Connect to local Redis
r = redis.Redis(host='localhost', port=6379, db=0)

@app.post("/webhook/mt5")
async def receive_mt5_data(tick: MarketTick):
    # Push the tick data to a list named 'market_ticks'
    # We store it as a JSON string
    r.lpush("market_ticks", tick.json())

    # Keep only the last 100 ticks to prevent memory bloat
    r.ltrim("market_ticks", 0, 99)

    return {"status": "ok"}
