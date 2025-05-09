from dash import Dash, html, dcc
from dash.dependencies import State
import Dashboard_testing.ids as ids
from dash.dependencies import Input, Output
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Share_back_end_module.plotting import SharesPlotter
from Share_back_end_module.dataframe_manager import shares_analysis


def render(app:Dash,id_dropdown: str) -> html.Div:
    children = []

    
    
    @app.callback(
    Output(ids.METRIC_DROPDOWN, "value"),
    [Input(ids.METRIC_DROPDOWN, "value"),
     Input(ids.SELECTEDSHARE,"data")
    ],
    State(ids.METRIC_DROPDOWN, "options"),
    prevent_initial_call = True
    )
    def enforce_minimum_selection(selected_metrics,selected_share,available_options):
        if selected_metrics is None or len(selected_metrics) not in [1,2]:
            if not selected_share or not available_options:
                return []
            
            selected_share = selected_share[0]
            df_manager = shares_analysis(location_base=os.path.join(os.sep, "DiskStation","Data", "trading","files"),shares_df=pd.DataFrame({"updated_at":[],"code": []}))
            df_manager.get_cache_metric_df()
            Plotter = SharesPlotter(shares_analysis_instance=df_manager, plot_website=True)
            share_metrics = Plotter.share_metric_df.loc[selected_share,:]
            print(f"defaulting selected metrics, {list(share_metrics.index[~share_metrics.isna()])[:2]}")
            return list(share_metrics[~share_metrics.isna()])[:2]  # Default selection, first 2 metrics not NA
        
        return selected_metrics
    
    @app.callback(
        #first callback, intended to check the share metric drop down to see what share is selected, to see possible metrics to select.
        Output(ids.METRIC_DROPDOWN, "options"),
        Input(ids.SELECTEDSHARE, "data"),
        State(ids.METRICDATA, "data")
    )
    def update_metrics(codes, metric_data):
        
        if not codes:
            return []  # Reset options if no share is selected
        
        selected_share = codes[0]#finds the ccode of the first (and only code selected)
        df_manager = shares_analysis(location_base=os.path.join(os.sep, "DiskStation","Data", "trading","files"),shares_df=pd.DataFrame({"updated_at":[],"code": []}))
        df_manager.share_metric_df = pd.DataFrame(metric_data)
        Plotter = SharesPlotter(shares_analysis_instance=df_manager, plot_website=True)
        share_metrics = Plotter.share_metric_df.loc[selected_share,:]
        available_metrics = list(share_metrics.index[~share_metrics.isna()].values)
        
        print(f"available metrics, {available_metrics}")
        return [{"label": metric, "value": metric} for metric in available_metrics]
    
    children.append(html.H6("From your selected share, select 2 metrics to see how they compare to others in the industry."))
    children.append(
        dcc.Dropdown(
            id = ids.METRIC_DROPDOWN,
            multi = True,
            options = [{"label":"None","value":"None"}],
            value="None"
        )
    )
    return html.Div(children=children)
    