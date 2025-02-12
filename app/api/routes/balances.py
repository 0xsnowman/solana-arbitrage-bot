from fastapi import APIRouter
from app.services.solana_client import get_balance

router = APIRouter()

@router.get("/wallet/{wallet_address}")
def wallet_balance(wallet_address: str):
    return {"wallet": wallet_address, "balance": get_balance(wallet_address)}
