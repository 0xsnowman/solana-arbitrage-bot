import redis
from datetime import datetime

# Connect to Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Tokens (Hash)
def add_token(mint_address, symbol, decimals):
    redis_client.hset(f"token:{mint_address}", mapping={
        "symbol": symbol,
        "decimals": decimals
    })

def get_token(mint_address):
    return redis_client.hgetall(f"token:{mint_address}")

# Pools (Hash)
def add_pool(pool_address, token_a, token_b, platform, fee):
    redis_client.hset(f"pool:{pool_address}", mapping={
        "token_a": token_a,
        "token_b": token_b,
        "platform": platform,
        "fee": fee
    })

def get_pool(pool_address):
    return redis_client.hgetall(f"pool:{pool_address}")

# Prices (Sorted Set)
def add_price(token, pool_address, price):
    timestamp = datetime.utcnow().timestamp()
    redis_client.zadd(f"price:{token}:{pool_address}", {timestamp: price})

def get_latest_price(token, pool_address):
    prices = redis_client.zrange(f"price:{token}:{pool_address}", -1, -1, withscores=True)
    return prices[0] if prices else None

# Trades (List)
def log_trade(token_a, token_b, amount_in, amount_out, pool_address):
    trade_data = {
        "token_a": token_a,
        "token_b": token_b,
        "amount_in": amount_in,
        "amount_out": amount_out,
        "pool": pool_address,
        "timestamp": datetime.utcnow().isoformat()
    }
    redis_client.lpush("trades", str(trade_data))

def get_recent_trades(count=10):
    return redis_client.lrange("trades", 0, count-1)

# Arbitrage Opportunities (Sorted Set by profit)
def add_arbitrage_opportunity(token_a, token_b, profit, pool_a, pool_b):
    redis_client.zadd("arbitrage_opportunities", {
        f"{token_a}:{token_b}:{pool_a}:{pool_b}": profit
    })

def get_top_arbitrage_opportunities(count=5):
    return redis_client.zrevrange("arbitrage_opportunities", 0, count-1, withscores=True)