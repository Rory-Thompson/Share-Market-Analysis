from dash import Dash, dcc, html, Input, Output, State, callback
import Dashboard_testing.ids as ids
from datetime import datetime
import traceback
import pandas as pd

def render(app:Dash, model,Plotter) -> html.Div:
    children = [
                html.H3("Remake cache button. Note will take time"),
                html.Button("Remake cache", id = ids.UPDATEBUTTON, n_clicks = 0),
                html.Div(id = ids.UPDATECACHERES , children = "Are you gay")
                ]
    @app.callback(
        [
            Output(ids.UPDATECACHERES,'children'),#update text below to indicate shares to buy now
            Output(ids.SHARES_DROPDOWN, "options"),
            Output(ids.SHARES_DROPDOWN, "value",allow_duplicate=True),
            Output(ids.CURRSHARESTOBUY,'children')

        ],#update the Options for Share_dropdown for line graph
        [
            Input(ids.UPDATEBUTTON,'n_clicks'),
            Input(ids.SHARES_DROPDOWN,'options')
        ],
        State(ids.CURRSHARESTOBUY, 'children'),
        prevent_initial_call = True
    )
    def update_cache(n_clicks,shares_dropdown_options,current_content):
        print(f"Callback triggered: n_clicks = {n_clicks}, shares_dropdown_options = {shares_dropdown_options}")
        shares_dropdown_options = shares_dropdown_options or []
        try:
            Plotter.shares_analysis.update_cache()#need to pass the df maanger
            #I am fairly confident this works so we shall see. 
            model.create_model()#does recalculation,. should hopefully update  the model res df which is what we must pass 
            print("model_values_updated")
            res = model.share_test_values_get(df_series = Plotter.model_res_df)
            print(f"res has been set {len(res)}")
            res = res[res]
            Plotter.shares_analysis.save_day_df_cache()
            print(f"cache saved as csv.")
            shares_lst = list(res.index)
            res_str = f"shares to buy from most recent update time: {datetime.now()}. shares = {shares_lst} updates attempted: {n_clicks}"
            current_content_res = [f"current shares to buy: {', '.join(shares_lst)}"]
        except Exception as e:
            print(f"update failed. error = {traceback.format_exc()}")
            current_content_res = current_content
            res_str = f"update failed. Unlucky boss. no update occurred. error: {e} updates attempted: {n_clicks}"
            shares_lst = []
        print("update cache to now be returned. ")
        Plotter.shares_analysis.df_is_updated = False#We no longer want any updates to occur. hacky, should be fixed. should be individual storage for each metric type.
        #all sorted by df_manager.
        
        share_options = pd.DataFrame(shares_dropdown_options)
        share_options = list(share_options['value'])
        codes = list(set(share_options)|set(shares_lst))
        options = [{"label": code, "value": code} for code in codes]
        return res_str, options, shares_lst,current_content_res
    

    return html.Div(
        children = children
    )
    