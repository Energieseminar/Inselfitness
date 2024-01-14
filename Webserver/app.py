from flask import Flask
from dash import Dash, dcc, html, Input, Output
import pandas as pd
import read_serial

# Flask app setup
server = Flask(__name__)
app = Dash(__name__, server=server)

# Initial data for plotting
data = pd.DataFrame(columns=['SolarCurrent', 'SolarVoltage', 'WindCurrent', 'WindVoltage',
                             'BatteryVoltage', 'BiogasPowerDraw', 'InverterPowerConsumption', 'WindSpeed',
                             'SolarRadiation', 'Temperature'])
data.to_csv("arduino_data.csv", sep=";", index_label="timestamp")
# Dash layout
app.layout = html.Div([
    dcc.Graph(id='solar-plot'),
    dcc.Graph(id='wind-plot'),
    dcc.Graph(id='power-plot'),
    dcc.Interval(id='interval-component', interval=5000, n_intervals=0)
])

# Callback to update plots
@app.callback(
    [Output('solar-plot', 'figure'),
     Output('wind-plot', 'figure'),
     Output('power-plot', 'figure')],
    [Input('interval-component', 'n_intervals')]
)
def update_plots(n):
    read_data_from_mem = pd.read_csv("arduino_data.csv", delimiter=";", index_col="timestamp")
    print(f"Read in dataframe: {read_data_from_mem}")
    data_list = update_data()
    # Update data dataframe
    index = data_list["timestamp"]
    data_list.pop("timestamp")
    read_data_from_mem = pd.concat([pd.DataFrame(data_list, index=[index]), read_data_from_mem])
    print(f"Dataframe after concat is: {read_data_from_mem}")
    read_data_from_mem.to_csv("arduino_data.csv", sep=";", index_label="timestamp")
    # Solar Plot
    solar_plot = {
        'data': [
            {'x': read_data_from_mem['timestamp'], 'y': read_data_from_mem['SolarCurrent'], 'type': 'line', 'name': 'Solar Current'},
            {'x': read_data_from_mem['timestamp'], 'y': read_data_from_mem['SolarVoltage'], 'type': 'line', 'name': 'Solar Voltage'},
        ],
        'layout': {
            'title': 'Solar Panel Data',
            'xaxis': {'title': 'timestamp'},
            'yaxis': {'title': 'Values'},
        }
    }

    # Wind Plot
    wind_plot = {
        'data': [
            {'x': read_data_from_mem['timestamp'], 'y': read_data_from_mem['WindCurrent'], 'type': 'line', 'name': 'Wind Current'},
            {'x': read_data_from_mem['timestamp'], 'y': read_data_from_mem['WindVoltage'], 'type': 'line', 'name': 'Wind Voltage'},
            {'x': read_data_from_mem['timestamp'], 'y': read_data_from_mem['WindSpeed'], 'type': 'line', 'name': 'Wind Speed'},
        ],
        'layout': {
            'title': 'Wind Turbine Data',
            'xaxis': {'title': 'timestamp'},
            'yaxis': {'title': 'Values'},
        }
    }

    # Power Plot
    power_plot = {
        'data': [
            {'x': read_data_from_mem['timestamp'], 'y': read_data_from_mem['BatteryVoltage'], 'type': 'line', 'name': 'Battery Voltage'},
            {'x': read_data_from_mem['timestamp'], 'y': read_data_from_mem['BiogasPowerDraw'], 'type': 'line', 'name': 'Biogas Power Draw'},
            {'x': read_data_from_mem['timestamp'], 'y': read_data_from_mem['InverterPowerConsumption'], 'type': 'line', 'name': 'Inverter Power Consumption'},
        ],
        'layout': {
            'title': 'Power Data',
            'xaxis': {'title': 'timestamp'},
            'yaxis': {'title': 'Values'},
        }
    }

    return solar_plot, wind_plot, power_plot

# Function to read data from Arduino
def update_data():
    pairs = read_serial.get_data()
    # Create a dictionary from the key-value pairs
    data_dict = {pairs[i]: [float(pairs[i + 1])] for i in range(0, len(pairs), 2)}

    # Print the resulting dictionary

    data_dict.update({"timestamp": pd.Timestamp.now()})  # Add timestamp
    return data_dict

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
