from fastapi import FastAPI, HTTPException
from coinapi_client import CoinAPIClient
import os

app = FastAPI()
coinapi_client = CoinAPIClient(api_key=os.getenv("COINAPI_KEY"))

@app.get("/price/{base}/{quote}")
async def get_price(base: str, quote: str):
    price = await coinapi_client.get_price(base, quote)
    if price is None:
        raise HTTPException(status_code=404, detail="Price not found")
    return {"base": base, "quote": quote, "price": price}
