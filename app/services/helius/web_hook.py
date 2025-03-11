import httpx

async def create_helius_webhook(api_key, webhook_url, account_addresses, transaction_types):
    helius_api_url = f"https://api.helius.xyz/v0/webhooks?api-key={api_key}"
    payload = {
        "webhookURL": webhook_url,
        "transactionTypes": transaction_types,
        "accountAddresses": account_addresses,
        "webhookType": "enhanced",  # or "raw" based on your needs
        # "authHeader": "Optional_AuthHeader"  # if you want to add an auth header
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(helius_api_url, json=payload)
        response.raise_for_status()
        return response.json()

# Example usage
api_key = "HELIUS_API_KEY"
public_webhook_url = "https://ngid.ngrok.io/webhook"
account_addresses = ["ACCOUNT_ADDRESS_1", "ACCOUNT_ADDRESS_2"]
transaction_types = ["SWAP"]

import asyncio
result = asyncio.run(create_helius_webhook(api_key, public_webhook_url, account_addresses, transaction_types))
print(result)
