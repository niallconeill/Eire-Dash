import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash import Dash,  html, dcc

from src.data_utils import get_data
#from src.plot_functions import plot_map_data
import src.layouts as l

app = Dash(__name__,
           external_stylesheets=[dbc.themes.SOLAR],
           suppress_callback_exceptions=True
           )

data = get_data()
years = data.year.unique()
months = data.month.unique()
dates = data.date.unique()

metrics = {
    'Percipitation Amount mm (rain)': 'rain',
    'Air Temperature °C (temp)': 'temp',
    'Wet Bulb Air Temperature °C (wetb)': 'wetb',
    'Dew Point Air Temperature °C (dewpt)': 'dewpt',
    'Vapour Pressure hpa (vappr)': 'vappr',
    'Relative Humidity % (rhum)': 'rhum',
    'Mean Sea Level Pressure hPa (msl)': 'msl',
    'Mean Hourly Wind Speed kt (wdsp)': 'wdsp',
    'Predominant Hourly Wind Direction deg (wddir)': 'wddir'
}


overview_layout = html.Div([
    html.Br(),
    dbc.Col(html.Div(l.BUTTON_LAYOUT), width=20, style={'margin-left': '1vw'}),
    html.Br(),
    html.H4('Select a date and metrics to see the weather statistics for each station', style={
            'margin-left': '1vw'}),
    html.Div([dbc.Row(
        [
            dbc.Col(dbc.Spinner(
                id="loading-1",
                color="success",
                children=dcc.Graph(
                    id='map-plot',
                    style={'width': '45vw',
                           'margin-left': '1vw',
                           'margin-bottom': '90vh'}
                ))),
            dbc.Col(html.Div(
                dbc.Stack([
                    dcc.Dropdown(
                        years, years[0], id='year-dropdown', clearable=False, style={'width': '30vw'}),
                    dcc.Dropdown(
                        months, months[0], id='month-dropdown', clearable=False, style={'width': '30vw'}),
                    dcc.Dropdown(
                        dates, dates[0], id='date-dropdown', clearable=False, style={'width': '30vw'}),
                    dcc.Dropdown(options=[{'label': metric, 'value': val} for metric, val in metrics.items()],
                                 multi=True,
                                 id='metric-dropdown', clearable=False,
                                 style={'width': '30vw'})
                ], gap=3)
            )
            )
        ]
    )
    ])
])

detailed_layout = html.Div([
    html.Br(),
    dbc.Col(html.Div(l.BUTTON_LAYOUT), width=20, style={'margin-left': '1vw'}),
    html.H3('This is the Detailed Layout'),
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div("One of three columns"), md=4),
                    dbc.Col(html.Div("One of three columns"), md=4),
                    dbc.Col(html.Div("One of three columns"), md=4),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(html.Div("One of four columns"), width=6, lg=3),
                    dbc.Col(html.Div("One of four columns"), width=6, lg=3),
                    dbc.Col(html.Div("One of four columns"), width=6, lg=3),
                    dbc.Col(html.Div("One of four columns"), width=6, lg=3),
                ]
            ),
        ]
    )
])

seasonal_layout = html.Div([
    html.Br(),
    dbc.Col(html.Div(l.BUTTON_LAYOUT), width=20, style={'margin-left': '1vw'}),
    html.H3('This is the Seasonal Layout')
])


# Update the index
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/detailed':
        return detailed_layout
    elif pathname == '/seasonal':
        return seasonal_layout
    else:
        return overview_layout


@app.callback(
    Output("map-plot", "figure"),
    [
        Input("year-dropdown", "value"),
        Input("month-dropdown", "value"),
        Input("date-dropdown", "value"),
        Input("metric-dropdown", "value"),
    ])
def plot_map_data(year, month, date, metrics):

    df = data.query('date == @date and month == @month and year == @year')
    fig = px.scatter_mapbox(df, lat='latitude', lon='longitude', hover_name='station',
                            hover_data=metrics,
                            color_discrete_sequence=['blue'], zoom=5.8, height=650)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig


def main() -> None:
    app.layout = html.Div(children=[
        html.Br(),
        html.H1(children='Ireland Weather Data Dashboard',
                style={'margin-left': '1vw'}),
        html.Hr(),
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content')
    ])
    app.run_server(debug=True)


if __name__ == '__main__':
    main()
