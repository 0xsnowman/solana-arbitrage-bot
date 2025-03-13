import requests

# CoinMarketCap API key
API_KEY = 'COINMARKET_CAP_API_KEY'
BASE_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

def fetch_latest_prices(limit=20):
    """Fetch the latest cryptocurrency prices from CoinMarketCap."""
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': API_KEY,
    }
    params = {
        'start': '1',   # Start at rank 1
        'limit': limit,  # Number of coins to fetch
        'convert': 'USD' # Convert prices to USD
    }

    response = requests.get(BASE_URL, headers=headers, params=params)
    data = response.json()

    if response.status_code == 200:
        prices = {}
        for coin in data['data']:
            symbol = coin['symbol']
            price = coin['quote']['USD']['price']
            prices[symbol] = price
        return prices
    else:
        error_message = data['status']['error_message']
        raise Exception(f"Failed to fetch data: {error_message}")

