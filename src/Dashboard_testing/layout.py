from dash import Dash, html
import Dashboard_testing.shares_dropdown as shares_dropdown
import Dashboard_testing.metrics_dropdown as metrics_dropdown
import Dashboard_testing.linegraph as linegraph
import Dashboard_testing.ids as ids
import Dashboard_testing.metric_plot as metric_plot
import Dashboard_testing.reset_model_button as reset_model_button
import os
import sys
import Dashboard_testing.Data_table as Data_table
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



def create_layout(app: Dash,codes, Plotter,trading_model) -> html.Div:
    print(f"codes passed from layout into share_dropdown and metrics_dropdown, {codes}")
    return html.Div(
        className = "app-div",
        children = [
            html.H1(app.title),
            html.Hr(),
            html.Div(className = 'shares-update-cache',
                     children = [
                         reset_model_button.render(app = app, model = trading_model,Plotter = Plotter)
                         ]
                         ),
                     
            html.Div(
                className = "dropdown-container",
                children = [
                    shares_dropdown.render(app,codes = codes,id_dropdown=ids.SHARES_DROPDOWN,id_select_all=ids.SELECT_ALL_SHARES)
                ]
            ),
            linegraph.render(app,Plotter = Plotter),
            html.Div(id = ids.CURRSHARESTOBUY, children = [f"current shares to buy: {', '.join(codes)}"]),
            html.Div([Data_table.render(app,Plotter = Plotter)], className="dash-table-container"),
            html.Div(
                className ="dropdown-container-metric" ,
                children = [
                    metrics_dropdown.render(app,codes = codes,id_dropdown = ids.METRIC_DROPDOWN, Plotter= Plotter)
                ]
            ),
            metric_plot.render(app = app,Plotter= Plotter,id_share_dropdown=ids.METRICS_SHARE_DROPDOWN,id_metric_dropdown=ids.METRIC_DROPDOWN)

        ]

    )