from dash import Dash, html
import shares_dropdown
def create_layout(app: Dash,codes) -> html.Div:
    return html.Div(
        className = "app-div",
        children = [
            html.H1(app.title),
            html.Hr(),
            html.Div(
                className = "dropdown-container",
                children = [
                    shares_dropdown.render(app,codes = codes)
                ]
            )
        ]
    )