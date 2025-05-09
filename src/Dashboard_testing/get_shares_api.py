import requests

def get_shares_api(api_location):
    #returns json results from the api.
    try:
        print("awaiting api return: ", api_location)
        r = requests.get(api_location)
        r.raise_for_status()
        print("api call finished.", api_location)
        return r.json()
    except requests.RequestException as e:
        print(f"API fetch failed {e}")
        return {}

def get_columns(jobs_config_list:list[dict]) -> list:
    ##Realistically it would make sense to integrate this with the model section instead of a fresh calculation 
    '''
    inputs the output of get_jobs essentially (I think realistically I should make a config type. )

    outputs the same thing except now it has a columns_keep key for each dict that has a list of columns that must be kept for the update.
    '''
    
    all_columns = []
    for config in jobs_config_list:
        temp_columns = []
        if config["type"] == "RSI":
            name_RSI = f'RSI_window_{config["window"]}_periods_{config["min_periods"]}'
            name_gain = f'avg_gain_window_{config["window"]}_periods_{config["min_periods"]}'
            name_loss = f'avg_loss_window_{config["window"]}_periods_{config["min_periods"]}'
            temp_columns = [name_RSI,
                       name_gain,
                       name_loss]
        elif config["type"] == "moving_average":
            title = f'{config["day_small"]}/{config["day_long"]}_'
            perct_difference = title+'model_%_difference'
            streak_length = title+'streak_length'
            buy_status = title+'model_buy_status'
            title_long = f'rolling_average_{config["day_long"]}'
            title_small = f'rolling_average_{config["day_small"]}'
            temp_columns = [perct_difference, streak_length, buy_status, title_long, title_small] 

        elif config["type"] == "gradient_average":
             name = "_".join([config["column"]]) + f"_num_days_{'_'.join(map(str, config['num_days']))}_average"
             temp_columns = [name]
        all_columns= all_columns + temp_columns
    return all_columns