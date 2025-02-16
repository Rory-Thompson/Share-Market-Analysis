from dash import Dash, html, dcc

def render(app:Dash, codes) -> html.Div:
    return html.Div(
        children = [
            html.H6("Share code"),
            dcc.Dropdown(
                id = "share-dropdown",
                multi = True,
                options = [{"label": code, "value": code} for code in codes],
                value = codes
            )

        ]
    )