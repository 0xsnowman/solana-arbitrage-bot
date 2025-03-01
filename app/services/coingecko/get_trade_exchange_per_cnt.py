def get_trade_exchange_per_country(country,
                                   base_curr,
                                   target_curr):
    
    df_all = df_ex_subset[(df_ex_subset["country"] == country)]    
    
    exchanges_list = df_all["id"]
    ex_all = []    
       
    for exchange_id in exchanges_list:
        found_match = get_trade_exchange(exchange_id, base_curr, target_curr)
        if found_match == "":
            continue
        else:
            temp_dict = dict(
                             exchange = exchange_id,
                             last_price = found_match["last"],
                             last_vol   = found_match["volume"],
                             spread     = found_match["bid_ask_spread_percentage"],
                             trade_time = convert_to_local_tz(found_match["last_traded_at"])
                             )
            ex_all.append(temp_dict)
            
    return pd.DataFrame(ex_all)