from dash import html, dcc
import dash_bootstrap_components as dbc

BUTTON_LAYOUT = [
    dcc.Link(
        dbc.Button('Overview', id='overview-button', color="primary", className='me-1'),
        href='/'
    ),
    dcc.Link(
        dbc.Button('Detailed Analysis', id='detailed-button', color="primary", className='me-1'),
        href='/detailed'
    ),
    dcc.Link(
        dbc.Button('Seasonal Plots', id='seasonal-button', color="primary", className='me-1'),
        href='/seasonal'
    )
]