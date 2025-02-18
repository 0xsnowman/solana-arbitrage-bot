from fastapi import APIRouter
from app.services.solana_client import get_balance

router = APIRouter()

@router.get("/wallet/{wallet_address}")
def wallet_balance(wallet_address: str):
    return {"wallet": wallet_address, "balance": get_balance(wallet_address)}

@router.get("/deposit/{wallet_address}")
def wallet_deposit(wallet_address: str):
    return "deposited"

@router.get("/reinvest/{wallet_address}")
def wallet_reinvest(wallet_address: str, percent: float):
    return "reinvest"

