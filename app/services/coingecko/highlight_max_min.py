def highlight_max_min(x, color):
    
    return np.where((x == np.nanmax(x.to_numpy())) |
                    (x == np.nanmin(x.to_numpy())),
                    f"color: {color};",
                    None)