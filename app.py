import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import dash_bootstrap_components as dbc

from standings import standings

app = dash.Dash(__name__,
                external_stylesheets=['https://fonts.googleapis.com/css2?family=Poppins:wght@300;400&display=swap',
                                      dbc.themes.BOOTSTRAP],
                external_scripts=[
                    {'async src': 'https://www.googletagmanager.com/gtag/js?id=G-WFQYC4WBX9'},
                    {'src': 'https://cdn.polyfill.io/v2/polyfill.min.js'},
                ],
                meta_tags=[{'name': 'viewport', 'content': 'width=device-width,initial-scale=1.0'
                            }])

server = app.server
app.config.suppress_callback_exceptions = True
app.title = 'My Project'

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    pages = {
        '/players': standings
    }

    if pathname in pages:
        return pages[pathname]

    return standings


if __name__ == '__main__':
    app.run_server(debug=False)
