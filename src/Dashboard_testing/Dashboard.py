from dash import dcc, html,Output,Input
import importlib
from dash import Dash
import pandas as pd
import matplotlib.pyplot as plt
import Dashboard_testing.layout
from Dashboard_testing import ids
from Dashboard_testing.get_shares_api import get_columns
import os
import dash_bootstrap_components as dbc
import json


# Now re-import the class and test again
importlib.reload(Dashboard_testing.layout)
from Dashboard_testing.layout import create_layout



class Dashboard_creator:

    def __init__(self, api_location):
        #self.SharesPlotter = SharesPlotter
        self.api_location = api_location
        self.app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
        self.app.title = "Shares Analyis"
        #print(f"codes passed into layout from dashboard { self.codes}")
        self.app.layout = create_layout(self.app, self.api_location)
        self.register_callbacks()
        #self.app.run()
        
    def run(self, host="0.0.0.0", port=8050, debug=True):
        """Starts the Dash app."""
        self.app.run(host=host, port=port, debug=debug,use_reloader=False)
        #initial instantiation of the app, maybe should be seperate method?
    def register_callbacks(self):
        from Dashboard_testing.get_shares_api import get_shares_api
        from Share_back_end_module.dataframe_manager import shares_analysis
        from Share_back_end_module.model import TradingModel
        @self.app.callback(
            Output(ids.METRICDATA,'data'),
            Input('url','pathname')
        )
        #make the call parallel with other calls. 
        def fetch_metric_data(url):
            df_manager = shares_analysis(location_base=os.path.join(os.sep, "DiskStation","Data", "trading","files"),shares_df=pd.DataFrame({"updated_at":[],"code": []}))
            df_manager.get_cache_metric_df()
            return df_manager.share_metric_df.to_dict()
        @self.app.callback(
            Output(ids.SHAREDATASTORE_LATEST,'data'),
            Input('url', 'pathname'),
            prevent_initial_call = False
        )
        def fetch_data_on_page_load(pathname):
            print("fetching data on load")
            res = get_shares_api(f"{self.api_location}/shares/latest")
            print("res 0, ",res[0])
            return res#get all latest share data from initial call. 
        @self.app.callback(
            Output(ids.SHAREDATASTORE_JOBS,'data'),
            Input('url', 'pathname'),
            prevent_initial_call = False
        )
        def fetch_data_on_page_load_jobs(pathname):
            print("fetching jobs")
            jobs_all = get_shares_api(f"{self.api_location}/jobs")
            df=pd.DataFrame(jobs_all)
            res = df.config.tolist()
            for i in range(len(res)):
                res[i] = json.loads(res[i])
            print("jobs, ", res)
            return res#get all latest share data from initial call. 
        
        @self.app.callback(
            Output(ids.SHAREDATASTORE_LATEST_BUY,'data'),
            Input(ids.SHAREDATASTORE_LATEST,'data'),
            Input(ids.SHAREDATASTORE_JOBS, "data")
        )
        def get_latest_data(data,config):
            print("get latest data config: `",config)
            share_df = pd.DataFrame(data)
            print("begginging creation of df manager")
            df_manager = shares_analysis(location_base = os.path.join(os.sep, "DiskStation","Data", "trading","files"),shares_df = share_df)
            print("begginging creation of trading model.")
            
            trading_model = TradingModel(name = "This is the coolest model_temporary", shares_analysis = df_manager, config = config)
            extra_cols = get_columns(config)
            print("extra cols = ", extra_cols)
            
            df_manager.shares_df["RSI_window_14_periods_13"] = pd.to_numeric(df_manager.shares_df["RSI_window_14_periods_13"])
            df_manager.shares_df["9/21_model_%_difference"] = pd.to_numeric(df_manager.shares_df["9/21_model_%_difference"])
            print("shares df columns:", df_manager.shares_df.columns)
            print("dtypes: ", df_manager.model_res_df.dtypes)

            res = trading_model.share_test_values_get(df_manager.shares_df)
            print("shares to buy: ")
            res = df_manager.shares_df[res]
            print(res)
            if len(res)== 0:
                #return all the codes.
                print(res.to_dict("records"))
                return df_manager.shares_df.to_dict("records")
            
            return res.to_dict("records")



        

    #@property
    #def SharesPlotter(self):#not useful, would have to create a method for everything
        #return self.SharesPlotter

    

#create a call back that takes 



