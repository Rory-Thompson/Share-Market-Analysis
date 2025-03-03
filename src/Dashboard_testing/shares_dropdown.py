from dash import Dash, html, dcc
import Dashboard_testing.ids as ids
from dash.dependencies import Input, Output,State
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
    Output(id_dropdown, "value"),
    Input(id_dropdown, "value")
    )
    def enforce_minimum_selection_func(selected_share):
        if not selected_share:
            return []
        if len(selected_share)>3:
            selected_share_res = selected_share[:2]
        
        
        return selected_share_res   # Default selection, first 2 metrics not NA
        
        
    @app.callback(
    Output(id_dropdown,"value",allow_duplicate=True),
    Input(id_select_all,"n_clicks"),
    prevent_initial_call=True
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