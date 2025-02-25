from dash import Dash, html, dcc
import Dashboard_testing.ids as ids
from dash.dependencies import Input, Output
def render(app:Dash, codes,id_dropdown,id_select_all = None) -> html.Div:
    
    children = []
    print(f"codes passed into the render function of shares_dropdown, {codes}")
    children.append(html.H6("Select share code:"))
    children.append(
            dcc.Dropdown(
                id = id_dropdown,
                multi = True,
                options = [{"label": code, "value": code} for code in codes],
                value = codes
            ))
    
    
    @app.callback(
    Output(id_dropdown,"value"),
    Input(id_select_all,"n_clicks")
    )

    def select_all_shares(_: int) -> list[str]:
        return codes
    children.append(html.Button(
            className = "dropdown-button",
            id = ids.SELECT_ALL_SHARES,
            children = ["Select All"]
        ))
        
        
    return html.Div(
        children = children
    )