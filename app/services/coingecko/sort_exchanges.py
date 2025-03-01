df_ex_subset = df_ex[["id", "name", "country", "trade_volume_24h_btc"]]
df_ex_subset = df_ex_subset.sort_values(by = ["trade_volume_24h_btc"], ascending = False)