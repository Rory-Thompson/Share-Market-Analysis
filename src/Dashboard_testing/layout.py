from dash import Dash, html,dcc
import dash_bootstrap_components as dbc
import Dashboard_testing.shares_dropdown as shares_dropdown
import Dashboard_testing.metrics_dropdown as metrics_dropdown
import Dashboard_testing.linegraph as linegraph
import Dashboard_testing.ids as ids
import Dashboard_testing.metric_plot as metric_plot
import Dashboard_testing.toggle_all as toggle_all
#import Dashboard_testing.reset_model_button as reset_model_button
import os
import sys
import Dashboard_testing.Data_table as Data_table
import Dashboard_testing.metrics_table as metrics_table
import Dashboard_testing.Share_cards as Share_cards

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



def create_layout(app: Dash,api_location) -> html.Div:
   
    return html.Div(
        className = "app-div",
        children = [
            dcc.Location(id="url"),
            dcc.Store(id=ids.SHAREDATASTORE_LATEST),
            dcc.Store(id=ids.SHAREDATASTORE_JOBS),
            dcc.Store(id=ids.SHAREDATASTORE_LATEST_BUY),
            dcc.Store(id=ids.METRICDATA,storage_type = 'local'),
            dcc.Store(id = ids.SELECTEDSHARE),
            html.H1(app.title),
            # html.Hr(),
            # html.Div(
            #     className = "dropdown-container",
            #     children = [
            #         shares_dropdown.render(app, id_dropdown=ids.SHARES_DROPDOWN, id_select_all=ids.SELECT_ALL_SHARES)
            #     ]
            #),
            html.Div([dbc.Container(Share_cards.render(app), fluid = True)]),
            html.Div(children = ["To create a linegraph with the moving averages and RSI. Please click a row in the data table below and a graph will be rendered."]),
            linegraph.render(app,api_location),
            #html.Div(id = ids.CURRSHARESTOBUY, children = [f"current shares to buy: "]),
            html.Div([toggle_all.render(app)], className = "dash-toggle-container"),
            html.H2("Data table"),
            html.Div([Data_table.render(app)], className="dash-table-container"),
            html.Div(
                className ="dropdown-container-metric" ,
                children = [
                    metrics_dropdown.render(app,id_dropdown = ids.METRIC_DROPDOWN)
                ]
            ),
            html.Div([metrics_table.render(app)], className = "dash-container-metrics-table"),
            metric_plot.render(app = app,id_share_dropdown=ids.METRICS_SHARE_DROPDOWN,id_metric_dropdown=ids.METRIC_DROPDOWN)

        ]

    )