from dash import Dash,dcc, html
import plotly.express as px
import Dashboard_testing.ids as ids
from dash.dependencies import Input, Output, State
import sys
import os
import pandas as pd
from Dashboard_testing.get_shares_api import get_shares_api
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Share_back_end_module.plotting import SharesPlotter
from Share_back_end_module.dataframe_manager import shares_analysis

style_image = {
        "width": "90%",              # Adjust width (e.g., 80% of the parent div)
        "max-width": "900px",        # Limit max width
        "height": "auto",            # Keep aspect ratio
        "border": "2px solid black", # Add a black border
        "border-radius": "10px",     # Round corners
        "padding": "10px",           # Add padding around the image
        #"background-color": "#f8f9fa", # Light gray background
        "box-shadow": "5px 5px 15px rgba(0, 0, 0, 0.3)", # Add a shadow
        "margin": "0"            # doesnt do anything, this is where the stuff happens. 
        }

# style_division = {
#         "display": "flex",
#         "justify-content": "flex_start",  # Center to the left horizontal
#         "align-items": "center",      # Center middle verticle
#         "height": "auto",            # Adjust div height
#         "border": "1px solid #ccc",   # Optional border around div
#         "background-color": "#eee",   # Light gray background
#         "padding": "20px"             # Padding inside div
#         }
def render(app: Dash,api_location) -> html.Div:
    
    @app.callback(
        Output(ids.LINEGRAPH,"children"),
        Input(ids.SELECTEDSHARE, "data")
    )
    def update_linegraph(codes) -> html.Div:
        print(f"codes passed into render in linegraph update_linegraph callback, {codes}")
        #fig = px.bar(filtered_data, x = 'medal', y = "count", color = "nation",text = "nation")
        call = f"{api_location}/shares/timeseries?codes={','.join(codes)}"

        res = get_shares_api(call)
        shares_df = pd.DataFrame(res)
        df_manager = shares_analysis("nothing", shares_df)
        df_manager.create_day_df()
        Plotter = SharesPlotter(shares_analysis_instance = df_manager,plot_website = True)
        img_src = Plotter.plot_averages(codes = codes, averages = [9,21], plot_rsi = True,min_periods =13,window = 14)
        return html.Div(html.Img(src=img_src, style=style_image))
    

    return html.Div(id = ids.LINEGRAPH)