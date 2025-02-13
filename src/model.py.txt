class TradingModel:
    
    '''
    A model is created with particular configurations
    configuration format is important.
    
    example model config file json. Multiple different gradients and moving averages can be had. 
    model_config = [
    {"type": "moving_average",
        "day_long": 21,
        "day_small":9,
        "difference_threshold_max": 5,  # Difference % between high and low
        "difference_threshold_min": 5,
        "buy_status": True,
        'column':'last',
        "min_streak": 3,  
        "max_streak": 7  
    },
    {"type":"gradient_average",
        "columns" = ['last'],
        "num_days": [9, 20, 3, 4, 5, 6],  
        "greater_than": 0.5,  
        "less_than": 2.0  
    }
]
    
    '''
    def __init__(self, name, config, shares_analysis):
        self.name = name
        self.config = config
        self.shares_analysis = shares_analysis  # Reference to the main class
        self.results = []  # Store evaluation results
        self.shares_analysis.models[self.name] = self
        
        #	10/30_model_%_difference example name 
        
        self.config_df = pd.DataFrame(self.config)
        self.create_model()
        
        
    
    def create_model(self):
        
        for model_val in self.config:
            if model_val['type'] =='moving_average':
                print(model_val['day_long'])
                print(model_val['day_small'])
                
                self.shares_analysis.create_smoothing_function_model(day_long = model_val['day_long'],
                                                                     day_small = model_val['day_small'])
            elif model_val['type'] =='gradient_average':
                self.shares_analysis.calc_gradient_average(num_days=model_val['num_days'],
                                                           columns=[model_val['column']])
            elif model_val['type'] =='rsi':
                self.shares_analysis.calc_rsi(self, window = model_val[window], min_periods = model_val[min_periods])
                
                
                
    def share_test_values_get(self,df_series):
        
        
        '''
        This should work for both series and individual shares.
        
        '''
        lst_cur_res = []
        for model_val in self.config:
            
            print(model_val['type'])
            if model_val['type'] =='moving_average':
                title = f'{model_val["day_small"]}/{model_val["day_long"]}_'
                #title_long = f'rolling average {day_long}'
                #title_small = f'rolling average {day_small}'
                #title = f'{day_small}/{day_long}_model_buy_status'
                #f'{day_small}/{day_long}_model_%_difference'
                
                
                difference_threshold = (
                (abs(df_series[title+'model_%_difference'])>= model_val["difference_threshold_min"]) & 
                (abs(df_series[title+'model_%_difference'])<= model_val["difference_threshold_max"])
                )
                
                
                streak_length = (
                (df_series[title+'streak_length'] >= model_val["min_streak"]) & 
                (df_series[title+'streak_length']<= model_val["max_streak"])
                )
                global test7
                test7=pd.concat([difference_threshold,streak_length], axis=1)
                res = streak_length & difference_threshold & df_series[title+'model_buy_status']
                
                lst_cur_res.append(res)
                
                
                
            
            elif model_val['type'] =='gradient_average':
                columns = [model_val["column"]]
                title = "_".join(columns) + f"_num_days_{'_'.join(map(str, model_val['num_days']))}_average"
                
                res = (
                (df_series[title] <= model_val['greater_than']) & 
                (df_series[title] <= model_val['greater_than'])
                )
                
                lst_cur_res.append(res)
            elif model_val['type'] =='RSI':
                #True if it is less than the RSI min value.
                title = f'RSI_window_{model_val["window"]}_periods_{model_val["min_periods"]}'

                res = df_series[title]<= model_val["rsi_min"]
                lst_cur_res.append(res)
        print(len(lst_cur_res))
                    
                
        final_res = pd.concat(lst_cur_res, axis=1)
        print(len(final_res.columns))
        global test5
        test5 = final_res
        global test6
        test6 = lst_cur_res
        final_res_2 = (final_res.sum(axis=1) == len(final_res.columns))
        self.results = final_res_2    
        return final_res_2#either returns a boolean or a True false value.
        
            
                
            
        
        
    def shares_to_buy_now(self):
        
        if self.shares_analysis.model_res_df:
            pass
                    
                
                
            
            
