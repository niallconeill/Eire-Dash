import pandas as pd
import plotly.express as px 
from dash import Dash, html, dcc, Input, Output

from src.data_utils import get_data

data = get_data()

# TODO: Finish off writing this function 
# def render(app: Dash, data: pd.DataFrame) -> html.Div:
#     @app.callback(
#     Output("map-plot", "children"),
#     [
#        Input("year-dropdown", "value"),
#        Input("month-dropdown", "value"),
#        Input("date-dropdown", "value"),
#        Input("metric-dropdown", "value"),
#     ])
def plot_map_data():
    
    date=1
    month='January'
    year=2017
    df = data.query('date == @date and month == @month and year == @year')
    fig = px.scatter_mapbox(df, lat='latitude', lon='longitude', hover_name='station',
                        hover_data=['rain', 'temp', 'wdsp', 'rhum'],
                        color_discrete_sequence=['blue'], zoom=5.8, height=650)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":10, "t":10, "l":10, "b":10})
    return dcc.Graph(figure=fig)
        
#    return html.Div(id='map-plot')