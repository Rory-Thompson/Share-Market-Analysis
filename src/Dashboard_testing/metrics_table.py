from dash import Dash, dash_table, html
import pandas as pd
import Dashboard_testing.ids as ids
from dash.dependencies import State, Input, Output


#some basic styling. 
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
    Output(ids.SHAREDATATABLE, "data"),
    Output(ids.SHAREDATATABLE,"columns"),
    Input(ids.SELECTEDSHARE,'data'),
    State(ids.METRICDATA, "data"),
    prevent_initial_call = False
    )
    #updates to be the same as the share dropdown options. 
    def update_tables(selected_code,metric_data):
        
        print("stuff has happened for data table  metrics tablecall back")
        if not selected_code:
            return []
        
        selected_code = selected_code[0]#is a list, find the first value .
        df = pd.DataFrame(metric_data)
        series = df.loc[selected_code,:]
        df_no_na = series[~series.isna()].to_frame().T
        print("dtypes of the metrics: ", df_no_na.dtypes)
        res = df.groupby("sector").mean(numeric_only= True).round(2)##returns the mean for each column in each sector. 
        sector = df.loc[selected_code,"sector"]
        print("res index: ", res.index)
        print("sector: ", sector)
        res_sector = res.loc[sector,:]#get this row, will be series.
        res_sector["sector"] = sector
        res_sector["code"] = "industry_averages"
        res_sectors = res_sector.to_frame().T
        print("res_sectors: ", res_sectors)
        res_sectors.index = res_sectors.index + '_industry_average'
        final_df = pd.concat([df_no_na,res_sectors])
        final_df = final_df.reset_index()
         
        return final_df.to_dict('records'),[{"id": x, "name": x} for x in list(final_df.columns)]


    
    return dash_table.DataTable(
                                columns = [{'id':"nodata", 'name':'nodata'},
                                           {'id':'nodata2','name': 'nodata2'}],
                             id = ids.SHAREDATATABLE,
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