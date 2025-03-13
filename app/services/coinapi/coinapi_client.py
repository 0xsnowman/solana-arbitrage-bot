import httpx
from typing import Optional

class CoinAPIClient:
    BASE_URL = "https://rest.coinapi.io/v1"
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {"X-CoinAPI-Key": self.api_key}

    async def get_price(self, asset_id_base: str, asset_id_quote: str) -> Optional[float]:
        url = f"{self.BASE_URL}/exchangerate/{asset_id_base}/{asset_id_quote}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                return data.get('rate')
            else:
                print(f"Failed to fetch price: {response.status_code} - {response.text}")
                return None
