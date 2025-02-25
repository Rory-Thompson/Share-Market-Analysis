from dash import Dash, html, dcc
from dash.dependencies import State
import Dashboard_testing.ids as ids
from dash.dependencies import Input, Output
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from plotting import SharesPlotter


def render(app:Dash,codes:list[str],id_dropdown: str, Plotter: SharesPlotter) -> html.Div:
    children = []


    
    @app.callback(
    Output(ids.METRIC_DROPDOWN, "value"),
    [Input(ids.METRIC_DROPDOWN, "value"),
     Input(ids.METRICS_SHARE_DROPDOWN,"value")
    ],
    State(ids.METRIC_DROPDOWN, "options")
    )
    def enforce_minimum_selection(selected_metrics,selected_share,available_options):
        if selected_metrics is None or len(selected_metrics) not in [1,2]:
            if not selected_share or not available_options:
                return []
            
            share_metrics = Plotter.share_metric_df.loc[selected_share,:]
            print(f"defaulting selected metrics, {list(share_metrics.index[~share_metrics.isna()])[:2]}")
            return list(share_metrics[~share_metrics.isna()])[:2]  # Default selection, first 2 metrics not NA
        
        return selected_metrics
    
    
    @app.callback(
        #first callback, intended to check the share metric drop down to see what share is selected, to see possible metrics to select.
        Output(ids.METRIC_DROPDOWN, "options"),
        Input(ids.METRICS_SHARE_DROPDOWN, "value")
    )
    def update_metrics(selected_share):
        if not selected_share:
            return []  # Reset options if no share is selected
        share_metrics = Plotter.share_metric_df.loc[selected_share,:]
        available_metrics = list(share_metrics.index[~share_metrics.isna()].values)
        
        print(f"available metrics, {available_metrics}")
        return [{"label": metric, "value": metric} for metric in available_metrics]
    


    children.append(html.H6("Select a single share code:"))
    children.append(
            dcc.Dropdown(
                id = ids.METRICS_SHARE_DROPDOWN,
                multi = False,
                options = [{"label": code, "value": code} for code in codes],
                value = None
            ))
    children.append(html.H6("From your selected share, select 2 metrics to see how they compare to others in the industry."))
    children.append(
        dcc.Dropdown(
            id = ids.METRIC_DROPDOWN,
            multi = True,
            options = []
        )
    )
    return html.Div(children=children)
    