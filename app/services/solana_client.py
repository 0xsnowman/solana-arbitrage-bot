from solana.rpc.api import Client
from app.core.config import settings

solana_client = Client(settings.SOLANA_RPC_URL)

def get_balance(wallet_address: str):
    return solana_client.get_balance(wallet_address)

def get_latest_blockhash():
    return solana_client.get_recent_blockhash()

def get_transaction(tx_signature: str):
    return solana_client.get_confirmed_transaction(tx_signature)
