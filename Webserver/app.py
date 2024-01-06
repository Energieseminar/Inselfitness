from flask import Flask
from dash import Dash, dcc, html, Input, Output
import serial
import pandas as pd

# Serial communication setup for Raspberry Pi
ser = serial.Serial('/dev/ttyACM0', 9600)  # Adjust the port and baud rate accordingly

# Flask app setup
server = Flask(__name__)
app = Dash(__name__, server=server)

# Initial data for plotting
data = pd.DataFrame(columns=['Timestamp', 'SolarCurrent', 'SolarVoltage', 'WindCurrent', 'WindVoltage',
                             'BatteryVoltage', 'BiogasPowerDraw', 'InverterPowerConsumption', 'WindSpeed',
                             'SolarRadiation', 'Temperature'])

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
    global data
    data_list = update_data()

    # Update data dataframe
    data = data.append(pd.Series(data_list, index=data.columns), ignore_index=True)

    # Solar Plot
    solar_plot = {
        'data': [
            {'x': data['Timestamp'], 'y': data['SolarCurrent'], 'type': 'line', 'name': 'Solar Current'},
            {'x': data['Timestamp'], 'y': data['SolarVoltage'], 'type': 'line', 'name': 'Solar Voltage'},
        ],
        'layout': {
            'title': 'Solar Panel Data',
            'xaxis': {'title': 'Timestamp'},
            'yaxis': {'title': 'Values'},
        }
    }

    # Wind Plot
    wind_plot = {
        'data': [
            {'x': data['Timestamp'], 'y': data['WindCurrent'], 'type': 'line', 'name': 'Wind Current'},
            {'x': data['Timestamp'], 'y': data['WindVoltage'], 'type': 'line', 'name': 'Wind Voltage'},
            {'x': data['Timestamp'], 'y': data['WindSpeed'], 'type': 'line', 'name': 'Wind Speed'},
        ],
        'layout': {
            'title': 'Wind Turbine Data',
            'xaxis': {'title': 'Timestamp'},
            'yaxis': {'title': 'Values'},
        }
    }

    # Power Plot
    power_plot = {
        'data': [
            {'x': data['Timestamp'], 'y': data['BatteryVoltage'], 'type': 'line', 'name': 'Battery Voltage'},
            {'x': data['Timestamp'], 'y': data['BiogasPowerDraw'], 'type': 'line', 'name': 'Biogas Power Draw'},
            {'x': data['Timestamp'], 'y': data['InverterPowerConsumption'], 'type': 'line', 'name': 'Inverter Power Consumption'},
        ],
        'layout': {
            'title': 'Power Data',
            'xaxis': {'title': 'Timestamp'},
            'yaxis': {'title': 'Values'},
        }
    }

    return solar_plot, wind_plot, power_plot

# Function to read data from Arduino
def update_data():
    global ser
    serial_data = ser.readline().decode().strip()
    data_list = [float(value) if value.replace('.', '', 1).isdigit() else value for value in serial_data.split(',')]
    data_list.insert(0, pd.Timestamp.now())  # Add timestamp
    return data_list

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
