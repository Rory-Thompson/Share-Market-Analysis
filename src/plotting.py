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

from matplotlib.colors import to_rgb




class SharesPlotter:
    def __init__(self, shares_analysis_instance):
        """Initialize with an instance of the shares_analysis class."""
        self.shares_analysis = shares_analysis_instance
    
    def plot_metric_comparison(self, code, metric_x, metric_y, size_metric="marketCap"):
        """
        Plots a scatter plot comparing two selected metrics for all stocks in the same sector as the given stock.
        
        Parameters:
        - code (str): The stock code to highlight.
        - metric_x (str): The metric for the x-axis.
        - metric_y (str): The metric for the y-axis.
        - size_metric (str): The metric determining dot size (default: market cap).
        """
        
        # Get the dataframe of fundamental metrics
        df = self.shares_analysis.share_metric_df.copy()

        # Ensure metrics exist
        

        sector = df.loc[code, "sector"]
        sector_df = df[df["sector"] == sector].dropna(subset=[metric_x, metric_y, size_metric])
        
        # Normalize sizes for better visibility
        min_size = 20
        max_size = 500
        sector_df["size"] = np.interp(sector_df[size_metric], (sector_df[size_metric].min(), sector_df[size_metric].max()), (min_size, max_size))

        # Create scatter plot
        plt.figure(figsize=(12, 8))
        
        threshold = 10
        
        sector_df = sector_df[~sector_df[metric_x].isin([np.inf, -np.inf])]
        
        sector_df = sector_df[~sector_df[metric_y].isin([np.inf, -np.inf])]
        
        
        mean_val_metric_x = sector_df[metric_x].mean()
        std_val_metric_x = sector_df[metric_x].std()
        upper_bound_metric_x = mean_val_metric_x + (threshold * std_val_metric_x)
        print(std_val_metric_x)
        print(mean_val_metric_x)
        
        mean_val_metric_y = sector_df[metric_y].mean()
        std_val_metric_y = sector_df[metric_y].std()
        upper_bound_metric_y = mean_val_metric_y + (threshold * std_val_metric_y)
        
        print(upper_bound_metric_y)
        print(upper_bound_metric_x)
        
        
        sector_df = sector_df[(sector_df[metric_x] <= upper_bound_metric_x)&(sector_df[metric_y] <= upper_bound_metric_y)]
        
        if metric_x not in df.columns or metric_y not in df.columns or size_metric not in df.columns:
            raise ValueError(f"One or more selected metrics are missing from the dataset: {metric_x}, {metric_y}, {size_metric}")

        # Get the sector of the selected stock
        if code not in df.index:
            raise ValueError(f"Code {code} not found in dataset.")


        top_stocks = list(sector_df.nlargest(3, size_metric).index)#for legend.
        print(top_stocks)
        if code not in top_stocks:
            top_stocks.append(code)
        hue_order = list(top_stocks) + ['Other']
        global test9
        palette = sns.color_palette("Set2", len(hue_order))#set initial palette
        test9 = palette
        
        sector_df["highlight"] = sector_df.index.map(lambda x: x if x in top_stocks else "Other")
        global test8
        test8 = sector_df
        
        dictionary_color = dict(zip(hue_order, palette))
        dictionary_color[code] = to_rgb('#880808')
        dictionary_color["Other"] = to_rgb('#F4E2A8')



       
        #get hue order from the dictionary, ensure it is the right order.
        hue_order, palette = zip(*dictionary_color.items())
        test9 = palette
        #for this function set the palett. it should be in order with the hue_order. palett order = hue_order to get correct coloring
        sns.set_palette(palette)
        
        print(f"hue_order_{hue_order}")
        scatter = sns.scatterplot(
            data=test8, x=metric_x, y=metric_y, size="size", sizes=(min_size, max_size), alpha=0.6, edgecolor="black",
            hue="highlight",hue_order = hue_order, legend = "brief"
        )
        
        
        ###do legend stuff
        #need to make final updates to the legend, remove the sizes, other and highlight variables.
        scatter.get_legend()

        handles, labels = scatter.get_legend_handles_labels()

        dictionary_color_2 = dict(zip(labels, handles))
        
        #remove other and highlight. 
        dictionary_color_2.pop('Other', None)
        dictionary_color_2.pop('highlight', None)

        labels, handles = zip(*dictionary_color_2.items())

        if 'size' in labels:
            #this is a bit of a hack job but thats aite
            #assumes same ordering
            #assumes the size labels are after the 'size' value in the list. 
            size_index = labels.index('size')  # Get index of 'size'
            filtered_handles = handles[:size_index]  # Keep only items before 'size'
            filtered_labels = labels[:size_index]    # Keep only labels before 'size'
        else:
            filtered_handles, filtered_labels = handles, labels  # No change if 'size' is missing

        print(filtered_handles)
        print(filtered_labels)
        # Set new legend
        scatter.legend(filtered_handles, filtered_labels, title="Filtered Shares")
        #
        
        
        # Highlight the selected stock
      
        # Add median reference lines
        plt.axvline(sector_df[metric_x].median(), linestyle="--", color="gray", alpha=0.7, label=f"Median {metric_x}")
        plt.axhline(sector_df[metric_y].median(), linestyle="--", color="gray", alpha=0.7, label=f"Median {metric_y}")

        # Labels and title
        plt.xlabel(metric_x)
        plt.ylabel(metric_y)
        plt.title(f"{metric_x} vs {metric_y} for {sector} Stocks", fontsize=14, fontweight="bold")
        
        
        plt.grid(True, linestyle="--", alpha=0.5)
        
        # Show plot
        plt.show()