import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd

app = dash.Dash(__name__)

data = {'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [25, 30, 22],
        'City': ['New York', 'San Francisco', 'Los Angeles']}

df = pd.DataFrame(data)

app.layout = html.Div([
    html.H1("Simple DataFrame Viewer"),
    dcc.Graph(id='dataframe-graph',
              figure={'data': [{'x': df.columns, 'y': df.iloc[0], 'type': 'bar', 'name': 'Name'}],
                      'layout': {'title': 'Name Distribution'}})
])

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True)
