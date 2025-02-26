

import argparse
from dataframe_manager import shares_analysis
from plotting import SharesPlotter
from model import TradingModel
from config import aest  # Import the global timezone variable


import requests
import pandas as pd
import json
import logging
from datetime import datetime
import os
from tqdm import tqdm
import pandas as pd
from pytz import timezone
import matplotlib.dates as mdates
import warnings
import numpy as np
import yfinance
import requests
aest = timezone('Australia/Sydney')
import traceback
import time
import seaborn as sns
import matplotlib.pyplot as plt
from Dashboard_testing.Dashboard import Dashboard_creator
from plotting import SharesPlotter
from dataframe_manager import shares_analysis
from matplotlib.colors import to_rgb
location_base = os.getenv("LOCATION", r"\\DiskStation\Data\trading\files")


def main():
    location = os.path.join(location_base, "asx")#does automatic join
    location_model_res = os.path.join(location_base, "rory_model_results")#not used for now .
    files = os.listdir(location)
    df_data = pd.DataFrame()
    uri_1_json = files[0]
    full_paths = [os.path.join(location, file) for file in files]


    def get_data_to_df(full_path):
        df_data = pd.DataFrame()
        temp = pd.read_json(full_path)
        df_data = pd.concat([temp,df_data], join = "outer")
        lst = []
        def lambda_func(a):
            if a['company_sector'] != None:
                #print(a['company_sector']['gics_sector'])
                ind = a.index
                lst.append(a['company_sector']['gics_sector'].replace(' ','_'))
            else:
                lst.append("No_industry")
        df_data.apply(lambda_func, axis = 1)
        df_data['sector']= lst
        return df_data

    


    for full_path in tqdm(full_paths):
    
        df_temp = get_data_to_df(full_path)
        df_data = pd.concat([df_data,df_temp])
        
    

    df_manager = shares_analysis(shares_df = df_data,location_base = location_base, get_cache_df = False)
    
    df_manager.calc_moving_average(num_days=50, min_periods = 30)
    df_manager.create_smoothing_function_model(day_long = 21,day_small = 9)
    df_manager.create_smoothing_function_model(day_long = 30,day_small = 10)
    df_manager.calc_gradient_average(num_days=[5,20,30,4,10,1],  columns=["last"])
    df_manager.calc_rsi()
    model_config = [
        {"type": "moving_average",
            'day_small': 9,
             'day_long': 21,# Difference % between high and low
             "difference_threshold_max": 7,  # Difference % between high and low
            "difference_threshold_min": 2,
            "buy_status": True,  
            "min_streak": 3,  
            "max_streak": 7  
        },
        {"type":"gradient_average",
         'column':'last',
            "num_days": [9, 20, 3, 4, 5, 6],  
            "greater_than": 0.5,  
            "less_than": 2.0  
        },
        {"type": "RSI",
         "min_periods": 13,
         "window":14,
        'rsi_min': 40}
    ]

    trading_model = TradingModel(name = "This is the coolest model", shares_analysis = df_manager, config = model_config)
    res = trading_model.share_test_values_get(df_series = df_manager.model_res_df)
    print("Recommended Shares to Purchase:")
    res_buy = res[res]
    print(res_buy)
    SharesPlotter_1 = SharesPlotter(shares_analysis_instance = df_manager,plot_website = True)
    if len(res_buy)==0:
        print("no shares to buy ya donkey")
    else:
        print(f"codes passed into Dashboard_creator, {list(res_buy.index)}")
        app = Dashboard_creator(codes = list(res_buy.index),Plotter = SharesPlotter_1)
        app.run()
        # try:

        #     SharesPlotter_1.plot_metric_comparison(code= list(res_buy.index)[0], metric_x= "trailingPE", metric_y='trailingEps')
        # except ValueError as e:
        #     print(f"code for {list(res_buy.index)[0]} failed, potentially try different metrics, full error: {e}")

        #     #temp = df_manager.share_metric_df.loc[code]
        #     #print(f"different metrics that are available for next run time: {temp[temp.isna()]}")
        # SharesPlotter_1.plot_averages(codes=[list(res_buy.index)[0]], averages= [30,10],plot_rsi= True)#this plot should always work. 

if __name__ == "__main__":
    main()