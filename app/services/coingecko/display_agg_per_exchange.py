def display_agg_per_exchange(df_ex_all, base_curr):
    
    # Group data and calculate statistics per exchange    
    df_agg = (
        df_ex_all.groupby("exchange").agg
        (        
            trade_time_min = ("trade_time", 'min'),
            trade_time_latest = ("trade_time", 'max'),
            last_price_mean = ("last_price", 'mean'),
            last_vol_mean = ("last_vol", 'mean'),
            spread_mean = ("spread", 'mean'),
            num_trades = ("last_price", 'count')
        )
    )
    
    # Get time interval over which statistics have been calculated    
    df_agg["trade_time_duration"] = df_agg["trade_time_latest"] - df_agg["trade_time_min"]
    
    # Reset columns so that we can access exchanges below
    df_agg = df_agg.reset_index()
    
    # Calculate % of total volume for all exchanges
    last_vol_pert = []
    for i, row in df_agg.iterrows():
        try:
            df_vol = get_vol_exchange(row["exchange"], 30, base_curr)
            current_vol = df_vol["volume_SMA"][0]
            vol_pert = (row["last_vol_mean"] / current_vol) * 100
            last_vol_pert.append(vol_pert)
        except:
            last_vol_pert.append("")
            continue
            
    # Add % of total volume column
    df_agg["last_vol_pert"] = last_vol_pert
    
    # Remove redundant column
    df_agg = df_agg.drop(columns = ["trade_time_min"])
    
    # Round all float values
    # (seems to be overwritten by style below)
    df_agg = df_agg.round({"last_price_mean": 2,
                           "last_vol_mean": 2,
                           "spread_mean": 2
                          })
    
    display(df_agg.style.apply(highlight_max_min,
                               color = 'green',
                               subset = "last_price_mean")
           )
           
    return None