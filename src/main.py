import os
from dataframe_manager import shares_analysis
from plotting import SharesPlotter
from model import TradingModel
from config import aest  # Import the global timezone variable
from pytz import timezone
aest = timezone('Australia/Sydney')
from Dashboard_testing.Dashboard import Dashboard_creator
from plotting import SharesPlotter
from dataframe_manager import shares_analysis
from matplotlib.colors import to_rgb
location_base = os.getenv("LOCATION", r"\\DiskStation\Data\trading\files")


def main():
    location = os.path.join(location_base, "asx")#does automatic join
    location_model_res = os.path.join(location_base, "rory_model_results")#not used for now .
    print("main.py is runninng")

    df_manager = shares_analysis(location_base = location_base, get_cache_df = True)
    
    df_manager.calc_moving_average(num_days=50, min_periods = 30)
    df_manager.create_smoothing_function_model(day_long = 21,day_small = 9)
    df_manager.create_smoothing_function_model(day_long = 30,day_small = 10)
    df_manager.calc_gradient_average(num_days=[5,20,30,4,10,1],  columns=["last"])
    df_manager.calc_rsi()
    model_config = [
        {"type": "moving_average",
            'day_small': 9,
             'day_long': 21,# Difference % between high and low
             "difference_threshold_max": 10,  # Difference % between high and low
            "difference_threshold_min": 0,
            "buy_status": True,  
            "min_streak": 2,  
            "max_streak": 10  


            
        },
        {"type":"gradient_average",
         'column':'last',
            "num_days": [9, 20, 3, 4, 5, 6],  
            "greater_than": 0,  
            "less_than": 4.0  
        },
        {"type": "RSI",
         "min_periods": 13,
         "window":14,
        'rsi_max': 45}
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
        app = Dashboard_creator(codes = list(res_buy.index),Plotter = SharesPlotter_1,trading_model = trading_model)
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