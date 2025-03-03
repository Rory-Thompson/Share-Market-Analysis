import pandas as pd
from dash import Dash, html, dcc, dash_table,Input, Output, State, callback
import dash_bootstrap_components as dbc
import Dashboard_testing.ids as ids

style_header={
        "backgroundColor": "#444",
        "color": "white",
        "fontWeight": "bold",
        "borderBottom": "2px solid #666",
        "padding": "10px"
    }

style_cell={
        "backgroundColor": "#1b1a1a",
        "color": "#E0E0E0",
        "border": "1px solid #444",
        "textAlign": "left",
        "fontSize": "14px"
    }

style_data={
        "backgroundColor": "#333",
        "color": "#E0E0E0",
        "border": "1px solid #444",
    }

style_data_conditional=[
        {"if": {"row_index": "odd"}, "backgroundColor": "#2a2a2a"},
        {"if": {"state": "active"}, "backgroundColor": "#555", "color": "white"}  # Highlight on click
    ]
def render(app, Plotter):
    data_df = Plotter.model_res_df[["title", "last","change", "ytd_percent_change",'month_percent_change',"week_percent_change", "sector","updated_at"]].reset_index()
    
    @app.callback(
    Output(ids.DATATABLE, "data"),
    Input(ids.SHARES_DROPDOWN,'options')
    )
    def update_tables(shares_dropdown_options):
        print(f"passed shares_drop_down_options: {shares_dropdown_options}")
        shares_dropdown_options = shares_dropdown_options or []
        
        share_options = pd.DataFrame(shares_dropdown_options)
        share_options = list(share_options['value'])
        print(len(share_options))
        print("stuff has happened for data table call back")
        data_df = Plotter.model_res_df
        data_df = data_df[data_df.index.isin(share_options)]
        print(len(data_df))
        print(len(data_df.to_dict('records')))
        data_df = data_df.reset_index()
        return data_df.to_dict('records')


    
    return dash_table.DataTable(data_df.reset_index().to_dict('records'),[{"name":i,"id":i} for i in data_df.columns],
                             id = ids.DATATABLE,
                             #style_table=style_table,  # Ensures the table occupies the full width
                             style_cell=style_cell,  # Consistent padding for cells
                             #style_header=style_header,
                             style_data=style_data,
                             style_data_conditional=style_data_conditional,
                             page_size = 50,
                             filter_action= 'native',
                             sort_action ='native'
    )
   
    
    #style={"width": "80%", 'margin': 'auto','display': 'flex', 'justifyContent': 'left', 'alignItems': 'left','textAlign':'left', 'height': '100vh', 'padding': '10px'}) 