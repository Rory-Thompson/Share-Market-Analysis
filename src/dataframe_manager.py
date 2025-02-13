class shares_analysis:
    
    '''
    Notes to improve. This class must update the self.shares_df and self.model_res_df, and constantly has complex logic 
    copied and pasted, some sort of auxilary method that updates a column with an input of a series. Would make it alot cleaner. \
    
    
    '''
    
    def __init__(self, shares_df,model_res_df_location=r'\\DiskStation\Data\trading\files\rory_model_results\res_model_df.csv'):
        self.shares_df = shares_df
        self.model_res_df = pd.read_csv(model_res_df_location,index_col = "Unnamed: 0")
        aest = timezone('Australia/Sydney')
        self.shares_df['aest_time'] = self.shares_df['updated_at'].dt.tz_convert(aest)
        self.shares_df["aest_day"] = self.shares_df["aest_time"].dt.strftime('%d/%m/%Y')
        self.shares_df = self.shares_df.reset_index()
        self.moving_average = {}
        self.all_codes = shares_df['code'].unique()
        self.models = {}
        self.averages_calculated = []
        self.create_day_df()
        self.update_price_model_res_df()
        self.completed_tickers = []
        self.share_metric_df= pd.read_csv(r"\\DiskStation\Data\trading\files\rory_model_results\yfinance_results.csv",index_col = "code")
        #be
#     def update_column_series(model_res_df = True, day_df = True, df_to_update):
#method potentially not required. 
#         if model_res_df = True:
            
#             for col in list(df_to_update.columns):
#                 if col not in self.model_res_df.columns:
#                     df_to_update

    

    def update_price_model_res_df(self):
        
        '''
        updates the 'last 
        
        '''
        
        idx = self.day_df.groupby('code')['aest_day_datetime'].idxmax()
        temp_df = self.day_df.loc[idx]
        #we now have the latest for day for each code in the day df. 
        # get code
        temp_df = temp_df.set_index('code')
        self.model_res_df['last'] = temp_df['last']
        
        
        
            
    
    def create_day_df(self):
        idx = self.shares_df.groupby(["code","aest_day"])["aest_time"].idxmax()
        temp_df = self.shares_df.loc[idx]
        temp_df = temp_df.sort_values("aest_time")
        full_dates = pd.date_range(start=temp_df["aest_time"].min(), end=temp_df["aest_time"].max(), freq='B')
        
        
        ##create multi index dataframe
        full_df = pd.DataFrame(
            [(date.strftime('%d/%m/%Y'), code) for date in full_dates for code in self.all_codes],
            columns=['aest_day', 'code']
        )
        merged_df = pd.merge(full_df, temp_df, on = ["aest_day", "code"], how="left")
        self.day_df = merged_df
        self.day_df['aest_day_datetime'] = pd.to_datetime(self.day_df['aest_day'], format="%d/%m/%Y")
        return merged_df
        
        
    def calc_moving_average(self, num_days,min_periods,start_date =None, end_date= None, shares_codes=[]):
        if len(shares_codes) == 0:
            shares_codes = list(self.all_codes)
        
        '''
        input
        num_days = 50. means an average will be calculated using 50 days
        min_periods, the number of days requried for a valid entry (will exclude the missing days if above)
        min_periods is handy for when 1 day is missing. 
        share_codes = ["BHP"],
        start date. #not used
        end date. #not used. 
        
        a warning will be returned if the start  date and end date do not have enough days to be passed
        
        output: a dataframe, each row is an entry of a smoothed share proce for a particular code. 
        
        
        '''
        title = f'rolling average {num_days}'
        self.averages_calculated.append(num_days)
        self.day_df[title] = self.day_df.groupby('code')['last'].transform(lambda x: x.rolling(window=num_days, min_periods = min_periods).mean())

    
    def plot_averages(self,codes, averages= [50], plot_rsi=False):
        
        
        """
        codes = list. List of ASX codes. No error will be thrown for invalid codes.
        
        averages = list of averages. Calcualtion beforehand not required.
        
        output: graph with every combination of code and average.
        
        works best with only 1 code and multiple averages. 
        
        """

        for average in averages:
            #print(pd.Series(list(self.day_df.columns)))
            
            if str(average) not in pd.Series(list(self.day_df.columns)).str[-len(str(average)):].values:
                #the average has not been calculated yet
                print(f'calculating missing average {average}')
                self.averages_calculated.append(average)
                self.calc_moving_average(num_days = average, min_periods = int(average//1.4))
                
        # Filter the data for 'BHP'
        fig, ax1 = plt.subplots(figsize=(18, 12),
                                nrows=(2 if plot_rsi else 1),
                                sharex=True,
                                gridspec_kw={'height_ratios': [2, 1] if plot_rsi else [1]})
        if not isinstance(ax1, np.ndarray):
            ax1 = [ax1]  
        for code in codes:
            temp_df = curr_shares_df.day_df[curr_shares_df.day_df['code'] == code]

            # Set up the plot
            
            # Plot the 'last' prices
            ax1[0].plot(temp_df["aest_day_datetime"].dt.tz_localize(None), temp_df["last"], label=f'Last Price for {code}', linewidth=2, marker='o')

        # Plot the rolling average
            for avg_col in averages:
            
                title = f'rolling average {avg_col}'
            
                ax1[0].plot(temp_df["aest_day_datetime"].dt.tz_localize(None), temp_df[title], label=f'{code} {title}', linewidth=2)
        
        # Format the x-axis to show dates nicely
        ax1[0].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax1[0].xaxis.set_major_locator(mdates.MonthLocator())

        # Titles and labels
        ax1[0].set_title('Stock Price & Moving Averages', fontsize=16, fontweight='bold')
        ax1[0].set_ylabel('Price', fontsize=12)#for better readability

        # Add gridlines for better readability
        ax1[0].grid(True, linestyle='--', alpha=0.5)
        ax1[0].legend(fontsize=12)

        # Add a legend
        if plot_rsi:
            self.plot_rsi(codes, ax=ax1[1])

        # Add a vertical line for the current date (optional)
        #         current_date = pd.Timestamp.now().date()
        #         if current_date in temp_df["aest_day"].values:
        #             plt.axvline(x=current_date, color='red', linestyle='--', label='Today')

        #         # Display the plot
        plt.tight_layout()  # Adjust layout to prevent overlap
        plt.show()
        
        if plot_rsi:
            self.plot_rsi(codes, ax=ax1[1])
    
    def plot_rsi(self, codes, window=14, min_periods = 13,ax=None):
        """
        Helper method to plot RSI for the given ASX codes.
        Plots the RSI with overbought (70) and oversold (30) lines.
        """
        if ax is None:
            fig, ax = plt.subplots(figsize=(14, 4))

        for code in codes:
            temp_df = self.day_df[self.day_df['code'] == code]

            # RSI column name
            #RSI_window_14_periods_13
            #rsi_column = f'RSI_window_{window}_periods_{window}'
            rsi_column = f'RSI_window_{window}_periods_{min_periods}'

            # Plot RSI
            ax.plot(temp_df["aest_day_datetime"].dt.tz_localize(None), temp_df[rsi_column], label=f'RSI for {code}', linewidth=2)

        # Add horizontal lines for overbought (70) and oversold (30) levels
        ax.axhline(y=70, color='r', linestyle='--', label='Overbought (70)')
        ax.axhline(y=30, color='g', linestyle='--', label='Oversold (30)')
        ax.fill_between(temp_df["aest_day_datetime"].dt.tz_localize(None), 30, 70, color='blueviolet', alpha=0.15)

        # Format the x-axis for the RSI plot
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Show dates in YYYY-MM-DD format
        ax.xaxis.set_major_locator(mdates.MonthLocator())  # Show ticks for each month
        ax.tick_params(axis='x', rotation=45)  # Rotate date labels for better readability

        # Add gridlines, title, labels, and legend to the RSI plot
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.set_title('Relative Strength Index (RSI)', fontsize=16, fontweight='bold')
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('RSI', fontsize=12)
        ax.legend(fontsize=12)

        # Display the plot
        if ax is None:
            plt.tight_layout()
            plt.show()
            
            
            
    def gen_share_lst(self,extra_metrics = [],codes_to_update =[]):
        
        base_metrics = ["longName","industry","sector","marketCap","trailingPE",'forwardPE','trailingEps','forwardEps','returnOnAssets','earningsGrowth','revenueGrowth','totalRevenue',
         'returnOnAssets','returnOnEquity','profitMargins','dividendYield']
        metrics = list(set(extra_metrics) | set(base_metrics))
        
        codes = self.model_res_df.index.unique().to_list()
        
        
        
        self.df_lst = []
        tickers = list(set(codes) - set(list(self.share_metric_df.index)))
        tickers = list(set(tickers) | set(codes_to_update))
        print()
        print(len(tickers))
        tickers = [code + '.AX' for code in tickers]
        for ticker_name in tickers:
            
            ticker_res = {}
            ticker_res["code"] = ticker_name[:-3]
            
            success = False
            retries = 0
            
            while not success and retries < 5:
                try:
                    ticker = yf.Ticker(ticker_name)
                    try:
                        hist = ticker.history(period="1d")
                        ticker_res["datetime"] = hist.index[-1] if not hist.empty else np.nan
                        
                    except Exception as e:
                        print(f"❌ History data failed for {ticker_name}: {e}")
                        ticker_res["datetime"] = np.nan
                        
                    ticker_info = ticker.info
                    
                    
                    for metric in metrics:
                        ticker_res[metric] = ticker_info.get(metric, np.nan)
                        
                    self.df_lst.append(ticker_res)
                    success = True
                    self.completed_tickers.append(ticker_name)
                    
                except Exception  as e:
                    print(f"❌ Full error for {ticker_name}: {e}")
                    print("Traceback details:")
                    traceback.print_exc()  # Prints the full traceback
                    #cannot find a way to know if it is a rate limit error. 
                      # Rate limit error
                    retries += 1
                    wait_time = 2 ** retries  # Exponential backoff
                    print(f"⚠️ Rate limit hit! Waiting {wait_time}s before retrying ({retries}/5)...")
                    time.sleep(wait_time)
                    #else:
                        #print(f"❌ Failed to fetch {ticker_name}: {e}")
                        #break  # Skip this ticker after other errors
        res = pd.DataFrame(self.df_lst)
        #res.set_index("code")
        
        #for some reason this code is cooked, needs to save as proper df before update can work
        self.gen_share_df()
        return res
    
    def gen_share_df(self):
        
        res = pd.DataFrame(self.df_lst)
        res.set_index("code")
        #now self.df_lst is updated completelty, but share metric df must not be, it should only be updated,
        #test this out, will obviously take some time
        self.share_metric_df.update(res)
        
        self.share_metric_df.to_csv(r"\\DiskStation\Data\trading\files\rory_model_results\yfinance_results.csv")
            
                    
                    
                    
        
        
    def create_smoothing_function_model(self,day_long, day_small):
        assert day_long > day_small, "day long must be greater than day small"
        
        '''
        note that the aest_time and aest_datetime are a bit flawed, it will update whenever run, but models that are not 
        updated will technically have the wrong datetime, so you need to update every model at each time to make this 
        value accurate. or you have seperate date time values for each model which makes more sense in my opinion. 
        '''
        if day_long not in self.averages_calculated:
            
            self.calc_moving_average(num_days = day_long, min_periods = int(day_long//1.4))
        if day_small not in self.averages_calculated:
            
            self.calc_moving_average(num_days = day_small, min_periods = int(day_small//1.4))
            
        #required averages have been calculated. 
        title_long = f'rolling average {day_long}'
        title_small = f'rolling average {day_small}'
        #if the shorter day period price is greater than the longer period price, it is a buy.
        self.day_df[f'{day_small}/{day_long}_model_buy_status'] = self.day_df[title_small]>self.day_df[title_long]
        self.day_df[f'{day_small}/{day_long}_model_difference'] = self.day_df[title_small]-self.day_df[title_long]
        self.day_df[f'{day_small}/{day_long}_model_%_difference'] = (self.day_df[f'{day_small}/{day_long}_model_difference']/(self.day_df['last']))*100
        
        
        ##these next lines are genius
        #ne returns the same dataframe of True False values.
        #shift, returns previous value, that means we need to sort by code and aest_day_datetime
        #this means it checks if the previous day is different from the sameday
        #cumsum (hehe) then adds 1 to a cumulative sum through the series whenever there was a change
        #we then create the buy streaks series that will show the size of each buy streak,
        #we can then join these buy streaks back into the dataset.
        title = f'{day_small}/{day_long}_model_buy_status'
        self.day_df = self.day_df.sort_values(by=['code', 'aest_day_datetime']).reset_index(drop=True)
        self.day_df[f'{day_small}/{day_long}_buy_streak'] = self.day_df.ne(self.day_df.shift())[title].cumsum()
        
        buy_streaks = self.day_df.groupby(['code', f'{day_small}/{day_long}_buy_streak']).size().reset_index(name=f'{day_small}/{day_long}_streak_length')
        
        
        if title not in list(self.model_res_df.columns):
            #inversion:
            #if the title exists in the model_df_columns it means it must exist in the day_df columns
            #if the title does not exist in the model_df_columns, then it must not exist in the day_df columns,
            #as day_df will update before the model df gets updated in the below logic.
            
            
            print(f"column does not exist. {title}")
            
            self.day_df = pd.merge(
                self.day_df, 
                buy_streaks, 
                how='left', 
                on=['code', f'{day_small}/{day_long}_buy_streak']
            )
            idx = self.day_df.groupby('code')['aest_day_datetime'].idxmax()
            temp_df = self.day_df.loc[idx]
            #temp_df now contains the latest values for each share only, then can be merged
            extra_cols = set(["aest_day","aest_day_datetime"])
            extra_cols_to_update = list(set(list(self.model_res_df.columns)) & extra_cols)
            
            print(extra_cols_to_update)
            print(list(extra_cols - set(extra_cols_to_update)))
            if len(extra_cols_to_update)>0:
                temp_df1= temp_df[["code"]+extra_cols_to_update]
                temp_df1 = temp_df1.set_index(["code"])
                self.day_df.update(temp_df1)
                
            #create the tuple maybe dont do this 
            #temp_df[f'{day_small}/{day_long}_result']
            temp_df = temp_df[["code",
                               f'{day_small}/{day_long}_model_buy_status',
                               f'{day_small}/{day_long}_model_difference', 
                               f'{day_small}/{day_long}_streak_length',
                              f'{day_small}/{day_long}_model_%_difference']+
                              list(extra_cols - set(extra_cols_to_update))]
            
            #now merge to the main df
            self.model_res_df = pd.merge(left = self.model_res_df, right = temp_df,
                     left_index= True, right_on = 'code', how = "outer").set_index("code")
        else:
            print(f"column exists, going down update pathway.  {title}")
            #logic if the column already exists. 
            #we want to somehow notify the user a change in status, honestly doesnt really matter though
            #maybe just overwrite the column anyway. 
            #perhaps see previous code to see how to do this, a merge will cause duplicate column.
            
            ##UPDATE TO IMPLEMENT, as long as index is the same it is allowed to use the df[col] = new_df[col]
            
            buy_streaks = buy_streaks.set_index(['code', f'{day_small}/{day_long}_buy_streak'])
            self.day_df = self.day_df.set_index(['code', f'{day_small}/{day_long}_buy_streak'])
            self.day_df.update(buy_streaks)
            self.day_df = self.day_df.reset_index()
            
            #now we update the model res df
            idx = self.day_df.groupby('code')['aest_day_datetime'].idxmax()
            temp_df = self.day_df.loc[idx]
            #temp_df now contains the latest values for each share only, then can be merged
            #create the tuple maybe dont do this 
            #temp_df[f'{day_small}/{day_long}_result']
            
            extra_cols = set(["aest_day","aest_day_datetime"])
            extra_cols_to_update = list(set(list(self.model_res_df.columns)) & extra_cols)
            
            
            if len(extra_cols_to_update)>0:
                temp_df1= temp_df[["code"]+extra_cols_to_update]
                temp_df1 = temp_df1.set_index(["code"])
                self.day_df.update(temp_df1)
            
            temp_df = temp_df[["code",
                               f'{day_small}/{day_long}_model_buy_status',
                               f'{day_small}/{day_long}_model_difference', 
                               f'{day_small}/{day_long}_streak_length']+
                              list(extra_cols - set(extra_cols_to_update))]
            
            temp_df.set_index('code', inplace=True)
            
            
            self.model_res_df.update(temp_df)
            codes_temp_df = pd.Series(list(temp_df.index))
            codes_temp_df_missing = codes_temp_df[codes_temp_df.isin(list(self.day_df.index))].values
            if len(list(codes_temp_df_missing))>0:
                #there is a missing new code that needs to be added.
                warnings.warn(f'There is codes {list(codes_temp_df_missing)}')
                ####
                #Logic to add the code, ? 
                ###
            
    def calc_gradient(self, num_days=[5], columns=[]):
        """
        Calculate the gradient (rate of change) for each share price over a given number of days.

        Parameters:
        num_days (int): The number of days to calculate the change. Default is 5.
        column must be a valid column inside of the day_df dataframe. 
        Returns:
        Adds a new column 'gradient_<num_days>' to self.day_df with the calculated gradient.
        
        due to the nature of it being column for column , we can assume that if this column already exists it will update fine. 
        
        
        """
        for day in num_days:
            self.day_df = self.day_df.sort_values(by=['code', 'aest_day_datetime']).reset_index(drop=True)
            col_names = []
            for col in columns:
                print(col)
                gradient_col_name = f'gradient_{col}_{day}'
                col_names.append(gradient_col_name)
                # Ensure the data is sorted by 'code' and 'aest_day_datetime'


                # Calculate the gradient using the difference in 'last' over the difference in days
                self.day_df[gradient_col_name] = self.day_df.groupby('code')[col].transform(
                    lambda x: (x - x.shift(day)) / day
                )


            #now we need to update the self.model_res_df
            idx = self.day_df.groupby('code')['aest_day_datetime'].idxmax()
            temp_df = self.day_df.loc[idx]
            temp_df = temp_df[["code","aest_day"]+col_names]
            #we now have the latest prices stored in the temp df 
            temp_df = temp_df.set_index("code")
            self.model_res_df
            self.model_res_df.update(temp_df)
            print(temp_df.columns)

            # Add new columns
            for col in temp_df.columns:

                if col not in self.model_res_df.columns:
                    self.model_res_df[col] = temp_df[col]
            
        

    
    
    
    def calc_gradient_average(self, num_days=[5], columns=[]):
        """
        Uses the calculate gradient method then averages over the different num day column pairs. 
        makes sense to only input 1 column at a time. 
        
    
        """
        self.calc_gradient(num_days = num_days, columns = columns)
        new_column_names = [f'gradient_{col}_{days}' for col in columns for days in num_days]
        
        name = "_".join(columns) + f"_num_days_{'_'.join(map(str, num_days))}_average"
        
        self.day_df[name] = self.day_df[new_column_names].mean(axis = 1)
        self.model_res_df[name] = self.model_res_df[new_column_names].mean(axis =1)
        
        
    def generate_results_to_day_df(self, model):
        model.create_model()#make sure columns are generated. 
        self.day_df[f'{model.name}_result'] = model.share_test_values_get(df_series = self.day_df)
        
        
                
            
    def calc_rsi(self, window = 14, min_periods = 13):
        
        def custom_func(rolling_window,calc_type ="avg_gain"):
            
            self.day_df = self.day_df.sort_values(by=['code', 'aest_day_datetime']).reset_index(drop=True)
            #ensure df is sorted.
            '''
            custom function to calculate avgloss and avg gain to be used via.apply to the day_df.
            returns a floating point value for every row.
            
            '''
    
            if calc_type == "avg_loss":

                is_loss = rolling_window<0
                res = rolling_window[is_loss].mean()
            elif calc_type == "avg_gain":
                is_gain = rolling_window>0

                res = rolling_window[is_gain].mean()
                #print(res)
            return res
        
        name_RSI = f'RSI_window_{window}_periods_{min_periods}'
        name_gain = f'avg_gain_window_{window}_periods_{min_periods}'
        name_loss = f'avg_loss_window_{window}_periods_{min_periods}'
        #get avg_gain
        print("starting calc gain")
        self.day_df['gain'] = self.day_df['change'].where(self.day_df['change'] > 0, 0)
        self.day_df['loss'] = self.day_df['change'].where(self.day_df['change'] < 0, 0).abs()
        print("starting calc loss")
        # Use rolling mean to calculate avg_gain and avg_loss
        self.day_df[name_gain] = self.day_df.groupby('code')['gain'].rolling(window=window, min_periods=min_periods).mean().reset_index(level=0, drop=True)
        self.day_df[name_loss] = self.day_df.groupby('code')['loss'].rolling(window=window, min_periods=min_periods).mean().reset_index(level=0, drop=True)
        
        #temp = self.day_df.groupby('code')['change'].rolling(window = window
                                                                #, min_periods = min_periods).apply(custom_func, args = ("avg_gain",))
        #temp = temp.reset_index(level = 0, drop = True)
        #self.day_df[name_gain] = temp
        
        #now get avg_loss
        #temp = self.day_df.groupby('code')['change'].rolling(window = window
                                                                #, min_periods = min_periods).apply(custom_func, args = ("avg_loss",))
        #temp = temp.reset_index(level = 0, drop = True)
        #self.day_df[name_loss] = temp
        
        
        #complete the first step
        #finds the ealiest day when the gain and the loss is not na
        print("doing the rest")
        temp = self.day_df[(~self.day_df[name_loss].isna())&(~self.day_df[name_loss].isna())]
        
        idx = temp.groupby('code')['aest_day_datetime'].idxmin()
        
        self.day_df['start_day_'+name_RSI] = self.day_df.index.isin(list(idx))
        #we now have each avg_loss and avg_gain
        self.day_df[name_RSI]= np.nan
        self.day_df.loc[self.day_df['start_day_'+name_RSI],name_RSI] = 100 -(100/(
            1+(self.day_df[name_gain]/self.day_df[name_loss])))
        #we now can assume the only entries in RSI is the first entry that 
        
        
        temp = self.day_df.groupby('code').shift(periods = 1)
        
        #create previous gain and previous loss columns
        self.day_df['previous_'+name_gain] = temp[name_gain]
        
        self.day_df['previous_'+name_loss] = temp[name_loss]
        
        #set update df to not include days that are the starting days.
        
        update_df = self.day_df[~self.day_df['start_day_'+name_RSI]]
        
        #do the calculation. 
        update_df[name_RSI] = 100-(100/(1+((update_df['previous_'+name_gain]*13+update_df[name_gain])/(
            update_df['previous_'+name_loss]*13+update_df[name_loss]))))
        
        
        #now we can update the dataframe
        
        self.day_df.loc[update_df.index,name_RSI] = update_df[name_RSI]
        
        
        #set model_res_df
        
        #
        idx = self.day_df.groupby('code')['aest_day_datetime'].idxmax()
        temp_df = self.day_df.loc[idx]
        
        #we now have the latest prices stored in the temp df 
        temp_df = temp_df.set_index("code")
        self.model_res_df[name_RSI] = temp_df[name_RSI]
        

    
        
        
        
        

    def test_model(self, model):
        '''
        input
        model. model is a function. input = share prices up to a given day. output= shares to buty
        
        output of this test. 
        using the original shares_df it will take different points in time, find what shares should be bought. 
        Then finally test the shares bought and see if they went up in price or not. to validate its efficacy. 
        
        '''
        pass
        
        
    