import base64
import httpx
from solders.keypair import Keypair
from solders.transaction import VersionedTransaction
import asyncio

async def execute_jupiter_swap(api_key, keypair, input_mint, output_mint, amount, slippage_bps):
    # Helius RPC URL
    rpc_url = f"https://rpc.helius.xyz/?api-key={api_key}"

    # Jupiter Swap API endpoint
    jupiter_url = "https://quote-api.jup.ag/v6/swap"

    # Prepare the swap request payload
    swap_payload = {
        "route": {
            "inputMint": input_mint,
            "outputMint": output_mint,
            "amount": amount,
            "slippageBps": slippage_bps,
            "userPublicKey": str(keypair.pubkey())
        }
    }

    # Fetch the swap transaction from Jupiter API
    async with httpx.AsyncClient() as client:
        response = await client.post(jupiter_url, json=swap_payload)
        response.raise_for_status()
        swap_txn = response.json()["swapTransaction"]

    # Decode the transaction, sign it, and encode it back
    raw_tx = VersionedTransaction.from_bytes(base64.b64decode(swap_txn))
    signature = keypair.sign_message(bytes(raw_tx.message))
    signed_tx = VersionedTransaction.populate(raw_tx.message, [signature])
    encoded_tx = base64.b64encode(bytes(signed_tx)).decode('utf-8')

    # Submit the signed transaction to the Solana network via Helius RPC
    headers = {"Content-Type": "application/json"}
    data = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "sendTransaction",
        "params": [encoded_tx, {"skipPreflight": True, "preflightCommitment": "finalized"}]
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(rpc_url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()

    return result

# Your Helius API key
api_key = "HELIUS_API_KEY"

# Load your Solana keypair
keypair = Keypair.from_base58_string("BASE58_PRIVATE_KEY")

# Define swap parameters
input_mint = "So11111111111111111111111111111111111111112"  # Example: SOL
output_mint = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"  # Example: USDC
amount = 10000000  # Amount in lamports (0.01 SOL)
slippage_bps = 50  # Slippage tolerance in basis points (0.5%)

# Execute the swap
result = asyncio.run(execute_jupiter_swap(api_key, keypair, input_mint, output_mint, amount, slippage_bps))
print(result)