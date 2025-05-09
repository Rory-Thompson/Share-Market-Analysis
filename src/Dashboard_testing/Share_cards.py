from dash import Dash, Input, Output, html
import dash_bootstrap_components as dbc
from Share_back_end_module import plotting
import Dashboard_testing.ids as ids
import requests
import pandas as pd
style = {
    "backgroundColor": "black",
    "border": "1px solid black",
    "borderRadius": "10px",
    "boxShadow": "0 2px 10px rgba(60,60,60,1)",
    "padding": "0.5rem",
    "marginBottom": "1rem",
    "width": "100%",
    "height": "100%",  # fill row height but respect max
    "display": "flex",
    "flexDirection": "column",
    "alignItems": "center",
    "justifyContent": "center",  # centers image vertically
}

def create_my_card(className, image_id):
    

    
    return dbc.Card(
        [
            html.Img(src="https://www.imgenerate.com/generate?width=300&height=200&text=No+Data&bg=cccccc&text_color=666666",id = image_id,style={
                "width": "auto",
                "height": "auto",       # or try "80%" if you want smaller
                "maxHeight": "100%",  # control the image height
                "maxWidth": "100%",
                "objectFit": "contain"
            })
        ],
    style = style
    )
def render(app):
    @app.callback(
        Output("xao-image", "src"),
        Output("xjo-image", "src"),
        Input('url','pathname')
    )
    def update_Card(url):
        headers = {
            ":authority": "www.listcorp.com",
            ":method": "GET",
            ":path": "/_api/services/company/get-price-data?code=ASX:XRO",
            ":scheme": "https",
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9",
            "priority": "u=1, i",
            "referer": "https://www.listcorp.com/",
            "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36"
        }
        filtered_headers = {k: v for k, v in headers.items() if not k.startswith(":")}
        r = requests.get("https://www.listcorp.com/_api/services/market/get-market-overview?exchange=ASX",headers = filtered_headers)
        if r.status_code != 200:
            raise ValueError("The api call retrieval failed ")
        res = r.json()
        #hopefullt order doesnt change. could probs  code it to be dynamic but ceebs.
        print("values recieved: ",round(float(res['data'][0]['percent_change']),2))
        img_xao = plotting.plot_mover("XAO","All Ordinaries", round(float(res['data'][0]['percent_change']),2),round(float(res['data'][0]['last_trade_price']),2),plot_website = True)
        img_xjo = plotting.plot_mover("XJO","ASX Top 200", round(float(res['data'][1]['percent_change']),2),round(float(res['data'][1]['last_trade_price']),2),plot_website = True)
        return img_xao,img_xjo
    
    @app.callback(
            #probs not the best to do it all in one callback. could design better.
        Output("biggest-winner-img","src"),
        Output("biggest-loser-img","src"),
        Output("biggest-market-cap-img","src"),
        Input(ids.SHAREDATASTORE_LATEST, "data")
    )
    def update_images(data):
        df = pd.DataFrame(data)
        #max_change
        max_change_idx = df["change"].idxmax()
        max_change_code = df.loc[max_change_idx, "code"]
        max_change = df.loc[max_change_idx, "change_percent"]
        max_change_title = df.loc[max_change_idx, "title"]
        max_change_last = df.loc[max_change_idx, "last"]
        max_change_img = plotting.plot_mover(max_change_code,max_change_title,max_change,max_change_last,plot_website = True)
        #min change 
        min_change_idx = df["change"].idxmin()
        min_change_code = df.loc[min_change_idx, "code"]
        min_change = df.loc[min_change_idx, "change_percent"]
        min_change_title = df.loc[min_change_idx, "title"]
        min_change_last = df.loc[min_change_idx, "last"]
        min_change_img = plotting.plot_mover(min_change_code,min_change_title,min_change,min_change_last,plot_website = True)
        max_market_cap_idx = df["market_cap"].idxmax()
        max_market_cap_code = df.loc[max_market_cap_idx, "code"]
        max_market_cap_change = df.loc[max_market_cap_idx, "change_percent"]
        max_market_cap_change_title = df.loc[max_market_cap_idx, "title"]
        max_market_cap_last = df.loc[max_market_cap_idx, "last"]
        max_market_cap_change_img = plotting.plot_mover(max_market_cap_code,max_market_cap_change_title,max_market_cap_change,max_market_cap_last,plot_website = True)
        return max_change_img,min_change_img, max_market_cap_change_img
    return dbc.Row([
            dbc.Col(create_my_card("xao-card","xao-image")),
            dbc.Col(create_my_card("xjo-card","xjo-image")),
            dbc.Col(create_my_card("biggest-winner", "biggest-winner-img")),
            dbc.Col(create_my_card("biggest-loser","biggest-loser-img")),
            dbc.Col(create_my_card("biggest-market-cap", "biggest-market-cap-img"))
            ],
            style={
                "height": "250px",  # or try 300px; keeps cards in check
                "overflow": "hidden",
            }
    )