import requests
from solana.rpc.api import Client
from solders.transaction import Transaction
from solders.account import Account
from solders.system_program import transfer
from solana.rpc.commitment import Commitment
from solana.rpc.types import TxOpts
from solders.pubkey import Pubkey
from solders.keypair import Keypair
import base64
import json

# Helius API endpoint (replace with your API key)
HELIUS_API_KEY = "HELIUS_API_KEY"
SOLANA_RPC_URL = f"https://mainnet.helius-rpc.com/?api-key={HELIUS_API_KEY}"

# Initialize Solana client
client = Client(SOLANA_RPC_URL)

# Raydium endpoints for swap and pool data
RAYDIUM_API_URL = "https://api.raydium.io/v2/main/ammV3/pools"

# Function to fetch Raydium pool data
def get_raydium_pools():
    response = requests.get(RAYDIUM_API_URL)
    if response.status_code == 200:
        pools = response.json()
        print("Fetched Raydium pools successfully!")
        for pool in pools[:5]:  # Display the first 5 pools
            print(f"Pool: {pool['name']}, Liquidity: {pool['liquidity']} SOL")
        return pools
    else:
        print("Failed to fetch pools:", response.status_code)
        return []

# Function to get Solana account balance
def get_solana_balance(public_key: str):
    balance = client.get_balance(Pubkey(public_key))
    sol_balance = balance['result']['value'] / 10**9  # Convert lamports to SOL
    print(f"Balance for {public_key}: {sol_balance} SOL")
    return sol_balance

# Function to perform a simple Solana transfer
def transfer_sol(sender: Keypair, recipient: str, amount: float):
    txn = Transaction()
    lamports = int(amount * 10**9)  # Convert SOL to lamports
    txn.add(transfer(
        from_pubkey=sender.public_key,
        to_pubkey=Pubkey(recipient),
        lamports=lamports,
    ))
    
    # Sign and send transaction
    opts = TxOpts(skip_confirmation=False, preflight_commitment=Commitment("confirmed"))
    result = client.send_transaction(txn, sender, opts=opts)
    print("Transaction result:", result)
    return result

# Example: Set up a test wallet (replace with your own private key)
def create_keypair_from_private_key(private_key: str):
    decoded = base64.b64decode(private_key)
    return Keypair.from_seed(decoded)

# Sample usage
def main():
    # Replace with your own wallet private key
    private_key = "your_base64_encoded_private_key"
    sender = create_keypair_from_private_key(private_key)
    recipient = "your_recipient_wallet_address"
    
    # Get wallet balance
    get_solana_balance(str(sender.public_key))

    # Fetch Raydium pools
    pools = get_raydium_pools()

    # Example transfer (1 SOL)
    transfer_sol(sender, recipient, 1.0)

if __name__ == "__main__":
    main()
