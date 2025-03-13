from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import redis

# FastAPI app setup
app = FastAPI()

# Redis connection
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Models for request bodies
class Token(BaseModel):
    mint_address: str
    symbol: str
    decimals: int

class Pool(BaseModel):
    pool_address: str
    token_a: str
    token_b: str
    platform: str
    fee: float

class Price(BaseModel):
    token: str
    pool_address: str
    price: float

class Trade(BaseModel):
    token_a: str
    token_b: str
    amount_in: float
    amount_out: float
    pool_address: str

class ArbitrageOpportunity(BaseModel):
    token_a: str
    token_b: str
    profit: float
    pool_a: str
    pool_b: str


# Token Operations
@app.post("/tokens/")
async def add_token(token: Token):
    redis_client.hset(f"token:{token.mint_address}", mapping={
        "symbol": token.symbol,
        "decimals": token.decimals
    })
    return {"message": "Token added successfully."}

@app.get("/tokens/{mint_address}")
async def get_token(mint_address: str):
    token = redis_client.hgetall(f"token:{mint_address}")
    if not token:
        raise HTTPException(status_code=404, detail="Token not found.")
    return {k.decode(): v.decode() for k, v in token.items()}


# Pool Operations
@app.post("/pools/")
async def add_pool(pool: Pool):
    redis_client.hset(f"pool:{pool.pool_address}", mapping={
        "token_a": pool.token_a,
        "token_b": pool.token_b,
        "platform": pool.platform,
        "fee": pool.fee
    })
    return {"message": "Pool added successfully."}

@app.get("/pools/{pool_address}")
async def get_pool(pool_address: str):
    pool = redis_client.hgetall(f"pool:{pool_address}")
    if not pool:
        raise HTTPException(status_code=404, detail="Pool not found.")
    return {k.decode(): v.decode() for k, v in pool.items()}


# Price Operations
@app.post("/prices/")
async def add_price(price: Price):
    timestamp = datetime.utcnow().timestamp()
    redis_client.zadd(f"price:{price.token}:{price.pool_address}", {timestamp: price.price})
    return {"message": "Price added successfully."}

@app.get("/prices/{token}/{pool_address}")
async def get_latest_price(token: str, pool_address: str):
    prices = redis_client.zrange(f"price:{token}:{pool_address}", -1, -1, withscores=True)
    if not prices:
        raise HTTPException(status_code=404, detail="Price not found.")
    return {"timestamp": datetime.utcfromtimestamp(prices[0][0]).isoformat(), "price": prices[0][1]}


# Trade Operations
@app.post("/trades/")
async def log_trade(trade: Trade):
    trade_data = {
        "token_a": trade.token_a,
        "token_b": trade.token_b,
        "amount_in": trade.amount_in,
        "amount_out": trade.amount_out,
        "pool": trade.pool_address,
        "timestamp": datetime.utcnow().isoformat()
    }
    redis_client.lpush("trades", str(trade_data))
    return {"message": "Trade logged successfully."}

@app.get("/trades/")
async def get_recent_trades(count: int = 10):
    trades = redis_client.lrange("trades", 0, count - 1)
    return [eval(trade.decode()) for trade in trades]


# Arbitrage Opportunity Operations
@app.post("/arbitrage/")
async def add_arbitrage_opportunity(opportunity: ArbitrageOpportunity):
    redis_client.zadd("arbitrage_opportunities", {
        f"{opportunity.token_a}:{opportunity.token_b}:{opportunity.pool_a}:{opportunity.pool_b}": opportunity.profit
    })
    return {"message": "Arbitrage opportunity added successfully."}

@app.get("/arbitrage/")
async def get_top_arbitrage_opportunities(count: int = 5):
    opportunities = redis_client.zrevrange("arbitrage_opportunities", 0, count - 1, withscores=True)
    return [{"opportunity": opportunity.decode(), "profit": profit} for opportunity, profit in opportunities]

