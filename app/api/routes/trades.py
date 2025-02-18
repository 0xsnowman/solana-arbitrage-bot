from fastapi import APIRouter
from app.services.arbitrage import check_arbitrage_opportunity

router = APIRouter()

@router.get("/check-arbitrage")
def arbitrage(price_a: float, price_b: float):
    return check_arbitrage_opportunity(price_a, price_b)

@router.get("/price-coingecko")
def price_goingecko(pool_name: str, token_pair: str):
    return "price-coingecko"

@router.get("/dex-screener")
def price_dexscreener(pool_name: str, token_pair: str):
    return "price_dexscreener"