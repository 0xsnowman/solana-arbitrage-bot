exchange_list_response = get_response("/exchanges", use_demo, exchange_params, PUB_URL)
df_ex = pd.DataFrame(exchange_list_response)