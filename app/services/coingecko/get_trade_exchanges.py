def get_trade_exchange(id, base_curr, target_curr):
    
    exchange_ticker_response = get_response(f"/exchanges/{id}/tickers",
                                            use_demo,
                                            {},
                                            PUB_URL)
    
    found_match = ""
    
    for ticker in exchange_ticker_response["tickers"]:
        if ticker["base"] == base_curr and ticker["target"] == target_curr:
            found_match = ticker
            break
            
    if found_match == "":
        warnings.warn(f"No data found for {base_curr}-{target_curr} pair in {id}")
    
    return found_match