def get_exchange_rate(base_curr):
    
    # This returns current BTC to base_curr exchange rate    
    exchange_rate_response = get_response(f"/exchange_rates",
                                          use_demo,
                                          {},
                                          PUB_URL)
    rate = ""
    try:
        rate = exchange_rate_response["rates"][base_curr.lower()]["value"]
    except KeyError as ke:
        print("Currency not found in the exchange rate API response:", ke)
        
    return rate  