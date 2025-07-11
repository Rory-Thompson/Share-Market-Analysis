import pandas as pd
from dash import dash_table,Input, Output, State, callback
import Dashboard_testing.ids as ids


style_header={
        "backgroundColor": "#444",
        "color": "white",
        "fontWeight": "bold",
        "borderBottom": "2px solid #666",
        "padding": "10px"
    }
style_table={
        "overflowX": "auto",
        "overflowY": "auto",
        "maxHeight": "600px",
        "width": "100%",
        "margin": "0 auto",
        "border": "none"
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
def render(app):
    #data_df = Plotter.model_res_df[["title", "last","change", "ytd_percent_change",'month_percent_change',"week_percent_change", "sector","updated_at"]].reset_index()
    
    @app.callback(
        Output(ids.SELECTEDSHARE, "data"),
        Input(ids.DATATABLE, 'active_cell'),
        State(ids.DATATABLE, 'derived_viewport_data')
    )
    def update_linegraph(active_cell: dict,data: list[dict]): 
        print("data row:", active_cell["row"], "type: ", type(active_cell["row"]))
        print("virtual__data: ", pd.DataFrame(data))
        print("res: ", pd.DataFrame(data).iloc[active_cell["row"], :]["code"])
        codes = [pd.DataFrame(data).iloc[active_cell["row"], :]["code"]]
        print("codes: ", codes)
        return codes


    
    return dash_table.DataTable(
                                columns = [{'id':"nodata", 'name':'nodata'},
                                           {'id':'nodata2','name': 'nodata2'}],
                             id = ids.DATATABLE,
                             #style_table=style_table,  # Ensures the table occupies the full width
                             style_cell=style_cell,  # Consistent padding for cells
                             #style_header=style_header,
                             style_data=style_data,
                             style_data_conditional=style_data_conditional,
                             page_size = 50,
                             filter_action= 'native',
                             sort_action ='native',
                             page_action="native",
                             page_current=0,
                             style_table = style_table
    )
   
    
    #style={"width": "80%", 'margin': 'auto','display': 'flex', 'justifyContent': 'left', 'alignItems': 'left','textAlign':'left', 'height': '100vh', 'padding': '10px'}) 