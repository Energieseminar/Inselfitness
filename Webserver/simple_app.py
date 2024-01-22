from flask import Flask
from dash import Dash, dcc, html, Input, Output, dash_table
import pandas as pd
import read_serial
import dash_bootstrap_components as dbc

# Flask app setup
server = Flask(__name__)
app = Dash(__name__, server=server)

app.layout = dbc.Container([
    dbc.Label('Click a cell in the table:'),
    dash_table.DataTable(read_serial.data.to_dict('records'),[{"name": i, "id": i} for i in read_serial.data.columns], id='tbl'),
    dbc.Alert(id='tbl_out'),
    html.H4(id="print_values_as_they_come", children=[]),
    dcc.Interval(id='interval-component', interval=5000, n_intervals=0)
])

@app.callback(Output('tbl_out', 'children'), Input('tbl', 'active_cell'))
def update_graphs(active_cell):
    return str(active_cell) if active_cell else "Click the table"


# Callback to update plots
@app.callback(
    [Output('tbl', 'data'),
     Output("print_values_as_they_come", "children")],
    [Input('interval-component', 'n_intervals')]
)
def update_table(n):
    read_data_from_mem = pd.read_csv("arduino_data.csv", delimiter=";", index_col="timestamp")
    #print(f"Read in dataframe: {read_data_from_mem}")
    ardu_df = update_data()
    # Update data dataframe
    updated_data = pd.concat([ardu_df, read_data_from_mem])
    #print(f"Dataframe after concat is: {updated_data}")
    updated_data.to_csv("arduino_data.csv", sep=";", index_label="timestamp")

    #get data as it comes:
    read_string = read_serial.get_data()
    print(read_string)

    return updated_data.to_dict("records"), read_string  # Return the updated data dictionary
# Function to read data from Arduino
def update_data():
    pairs = read_serial.get_fake_data()
    # Create a list of dictionaries from the key-value pairs
    data_dict = {pairs[i]: [float(pairs[i + 1])] for i in range(0, len(pairs), 2)}
    df = pd.DataFrame(data_dict, index=[str(pd.Timestamp.now())])
    # Print the resulting list of dictionaries
    return df

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
