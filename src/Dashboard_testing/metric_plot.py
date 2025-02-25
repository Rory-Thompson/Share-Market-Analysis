from dash import Dash,dcc, html
import plotly.express as px
import Dashboard_testing.ids as ids
from dash.dependencies import Input, Output
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from plotting import SharesPlotter

style_image = {
        "width": "70%",              # Adjust width (e.g., 80% of the parent div)
        "max-width": "700px",        # Limit max width
        "height": "auto",            # Keep aspect ratio
        "border": "2px solid black", # Add a black border
        "border-radius": "10px",     # Round corners
        "padding": "10px",           # Add padding around the image
        #"background-color": "#f8f9fa", # Light gray background
        "box-shadow": "5px 5px 15px rgba(0, 0, 0, 0.3)", # Add a shadow
        "margin": "0"            # doesnt do anything, this is where the stuff happens. 
        }
def render(app: Dash,Plotter:SharesPlotter, id_share_dropdown= ids.METRICS_SHARE_DROPDOWN,id_metric_dropdown = ids.METRIC_DROPDOWN) -> html.Div:

    @app.callback(
        Output(ids.METRICPLOT,"children"),
        [Input(ids.METRIC_DROPDOWN,"value"),
         Input(ids.METRICS_SHARE_DROPDOWN,"value")]
    )
    def update_metric(metrics:list[str],code: str) -> html.Div:

        if len(metrics)!= 2:
            raise ValueError(f"2 metrics are required to enter into a metrics plot. {len(metrics)} metrics were passed.")
        print(f"Rendering metric plot. metric_x = {metrics[0]}, metric_y = {metrics[1]}, code = {code}")
        img_src = Plotter.plot_metric_comparison(code = code,metric_x = metrics[0],metric_y = metrics[1])
        return html.Div(html.Img(src=img_src, className="dash-image"))
    return html.Div(id = ids.METRICPLOT)