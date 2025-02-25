from dash import Dash,dcc, html
import plotly.express as px
import Dashboard_testing.ids as ids
from dash.dependencies import Input, Output
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from plotting import SharesPlotter


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
MEDAL_DATA = px.data.medals_long()
def render(app: Dash,Plotter:SharesPlotter) -> html.Div:
    
    @app.callback(
        Output(ids.LINEGRAPH,"children"),
        Input(ids.SHARES_DROPDOWN,"value")
    )
    def update_linegraph(codes: list[str]) -> html.Div:
        print(f"codes passed into render in linegraph update_linegraph callback, {codes}")
        #fig = px.bar(filtered_data, x = 'medal', y = "count", color = "nation",text = "nation")
        img_src = Plotter.plot_averages(codes = codes, averages = [21,30], plot_rsi = True,min_periods =13,window = 14)
        return html.Div(html.Img(src=img_src, style=style_image))
    

    return html.Div(id = ids.LINEGRAPH)