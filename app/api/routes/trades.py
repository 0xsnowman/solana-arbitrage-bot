from fastapi import APIRouter
from app.services.arbitrage import check_arbitrage_opportunity

router = APIRouter()

@router.get("/check-arbitrage")
def arbitrage(price_a: float, price_b: float):
    return check_arbitrage_opportunity(price_a, price_b)