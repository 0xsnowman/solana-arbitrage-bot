import asyncio
import base58
import base64
import aiohttp
import statistics
import time
import sys
from solana.rpc.async_api import AsyncClient
from solders.keypair import Keypair
from solders.transaction import VersionedTransaction
from solders.compute_budget import set_compute_unit_price

asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

INPUT_MINT = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"  # USDC
OUTPUT_MINT = "So11111111111111111111111111111111111111112"  # SOL
AMOUNT = 1000000  # 0.001 SOL in lamports

async def main():
    await asyncio.sleep(1)
    try:
        print("Starting Jupiter swap...")
        print(f"Input mint: {INPUT_MINT}")
        print(f"Output mint: {OUTPUT_MINT}")
        print(f"Amount: {AMOUNT} lamports")
        
        quote_url = f'https://api.jup.ag/swap/v1/quote?inputMint={INPUT_MINT}&outputMint={OUTPUT_MINT}&amount=100000000&slippageBps=50&restrictIntermediateTokens=true'
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(quote_url, timeout=10) as response:
                    response.raise_for_status()
                    quote_response = await response.json()
                    print(f"Quote response: {quote_response}")
                    
                    print("Getting swap data from Jupiter...")
                    swap_url = "https://api.jup.ag/swap/v1/swap"
                    swap_header = {
                        'Content-Type': 'application/json',
                        # 'x-api-key': '' # enter API key here if needed
                    }
                    swap_data = {
                        "quoteResponse": quote_response,  # Replace with actual quoteResponse data
                        "userPublicKey": "FMUfPzB3i38nuVUM9d8vHpXJFf5GuESc4ZehCuySCGe3",  # Replace with the wallet's public key
                        "dynamicComputeUnitLimit": True,
                        "dynamicSlippage": True,
                        "prioritizationFeeLamports": {
                            "priorityLevelWithMaxLamports": {
                                "maxLamports": 1000000,
                                "priorityLevel": "veryHigh"
                            }
                        }
                    }
                    try:
                        async with aiohttp.ClientSession() as session:
                            async with session.post(swap_url, headers=swap_header, json=swap_data, timeout=10) as response:
                                response.raise_for_status()
                                swap_response = await response.json()
                                print(f"Swap response: {swap_response}")
                    except aiohttp.ClientError as e:
                        print(f"Error getting swap data from Jupiter: {e}")
                        return None
        except aiohttp.ClientError as e:
            print(f"Error getting quote from Jupiter: {e}")
            return None

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    pass

asyncio.run(main())

# loop = asyncio.get_event_loop()
# try:
#     loop.run_until_complete(main())
# finally:
#     pending = asyncio.all_tasks(loop)
#     for task in pending:
#         task.cancel()
#         try:
#             loop.run_until_complete(task)
#         except asyncio.CancelledError:
#             pass
#     loop.close()