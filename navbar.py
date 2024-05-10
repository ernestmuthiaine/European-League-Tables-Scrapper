from dash import html, dcc, callback
from dash.dependencies import State, Input, Output
import dash_bootstrap_components as dbc

navbar = dbc.Navbar(

    dbc.Container([
        dcc.Store(id='results-store', storage_type='local'),
        # html.A(
        #     dbc.Row([
        #         dbc.Col(html.Img(src='assets/football.jpg', height='35px'))
        #     ])
        # ),

        dbc.NavbarToggler(id='navbar-toggler', n_clicks=0),

        dbc.Collapse(
            html.A(
                dbc.Row([
                    dbc.Col(
                        dbc.NavLink('Standings', href='/standings', style={'font-size': '26px',
                                                                       'color': 'black'}), className='ms-2'),

                ]), style={"textDecoration": "none", "display": "flex"}
            ), id="navbar-collapse", is_open=False, navbar=True
        )
    ]), color="white", dark=False, expand="md", sticky='top',
)


@callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open
