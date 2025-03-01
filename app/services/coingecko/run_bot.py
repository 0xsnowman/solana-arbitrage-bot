def run_bot(country,
            base_curr,
            target_curr):
    
    df_ex_all = get_trade_exchange_per_country(country, base_curr, target_curr)
    
    # Collect data every minute    
    while True:
        time.sleep(60)
        df_new = get_trade_exchange_per_country(country, base_curr, target_curr)
        
        # Merge to existing DataFrame
        df_ex_all = pd.concat([df_ex_all, df_new])
        
        # Remove duplicate rows based on all columns
        df_ex_all = df_ex_all.drop_duplicates()
        
        # Clear previous display once new one is available
        clear_output(wait = True)
        display_agg_per_exchange(df_ex_all, base_curr)        
        
    return None