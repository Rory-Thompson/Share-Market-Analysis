from dash import Dash, html, dcc
import Dashboard_testing.ids as ids
from dash.dependencies import Input, Output,State
from Share_back_end_module.dataframe_manager import shares_analysis
from Share_back_end_module.dataframe_manager import shares_analysis
def render(app:Dash,id_dropdown,id_select_all = None) -> html.Div:
    
    children = []
    #print(f"codes passed into the render function of shares_dropdown, {codes}")
    children.append(html.H6("Select share code:"))
    children.append(
            dcc.Dropdown(
                id = id_dropdown,
                multi = True,
                #options = [{"label": code, "value": code} for code in codes],
                options = [],
                value = []
                #value = codes                
            ))
    @app.callback(Output(id_dropdown,'options'),
                  Input(ids.SHAREDATASTORE_LATEST_BUY,'data')
                  )
    def update_codes(data):
        #makes the options be all the codes that are to buy right now.
        #updates when sharedatastore latest buy updates.
        print("data passed: ",data)
        return [{"value": code["code"], "label": code["code"]+ " " + (code["title"] if code["title"] is not None else "")} for code in data]

    @app.callback(
    Output(id_dropdown,"value",allow_duplicate=True),
    Input(id_select_all,"n_clicks"),
    State(ids.SHAREDATASTORE_LATEST_BUY, 'options'),
    prevent_initial_call=True
    )

    def select_all_shares(_: int, all_options: list[dict]) -> list[str]:
        #selects all shares.
        lst = []
        for item in all_options:
            lst.append(item['label'])
            
        return lst
    children.append(html.Button(
            className = "dropdown-button",
            id = ids.SELECT_ALL_SHARES,
            children = ["Select All"]
        ))
        
        
    return html.Div(
        children = children
    )