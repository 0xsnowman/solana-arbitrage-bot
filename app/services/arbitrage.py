def check_arbitrage_opportunity(price_a: float, price_b: float, fee: float = 0.002):
    if price_a * (1 - fee) > price_b:
        return {"action": "Sell A, Buy B", "profit": price_a - price_b}
    elif price_b * (1 - fee) > price_a:
        return {"action": "Sell B, Buy A", "profit": price_b - price_a}
    return {"action": "No Arbitrage", "profit": 0}
