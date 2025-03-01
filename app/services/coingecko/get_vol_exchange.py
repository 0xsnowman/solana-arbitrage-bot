def get_vol_exchange(id, days, base_curr):
    
    vol_params = {"days": days}
    
    exchange_vol_response = get_response(f"/exchanges/{id}/volume_chart",
                                         use_demo,
                                         vol_params,
                                         PUB_URL)
    
    time, volume = [], []
    
    # Get exchange rate when base_curr is not BTC
    ex_rate = 1.0
    if base_curr != "BTC":
        ex_rate = get_exchange_rate(base_curr)
        
        # Give a warning when exchange rate is not found
        if ex_rate == "":
            print(f"Unable to find exchange rate for {base_curr}, vol will be reported in BTC")
            ex_rate = 1.0
    
    for i in range(len(exchange_vol_response)):
        # Convert to seconds
        s = exchange_vol_response[i][0] / 1000
        time.append(datetime.datetime.fromtimestamp(s).strftime('%Y-%m-%d'))
        
        # Default unit for volume is BTC
        volume.append(float(exchange_vol_response[i][1]) * ex_rate)
                      
    df_vol = pd.DataFrame(list(zip(time, volume)), columns = ["date", "volume"])
    
    # Calculate SMA for a specific window
    df_vol["volume_SMA"] = df_vol["volume"].rolling(7).mean()
    
    return df_vol.sort_values(by = ["date"], ascending = False).reset_index(drop = True)