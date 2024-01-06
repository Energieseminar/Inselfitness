from flask import Flask
from dash import Dash, dcc, html, Input, Output
import serial

# Serial communication setup for Raspberry Pi
ser = serial.Serial('/dev/ttyACM0', 9600)  # Adjust the port and baud rate accordingly

# Flask app setup
server = Flask(__name__)
app = Dash(__name__, server=server)

# Initial data for printing
data = {'Sensor1': 1.0, 'Sensor2': 1.0, 'Sensor3': 1.0}

# Dash layout
app.layout = html.Div([
    html.H1("Arduino Sensor Values"),
    html.Div([
        html.P("Sensor 1: "),
        html.P(id='sensor1-value'),
    ]),
    html.Div([
        html.P("Sensor 2: "),
        html.P(id='sensor2-value'),
    ]),
    html.Div([
        html.P("Sensor 3: "),
        html.P(id='sensor3-value'),
    ]),
    dcc.Interval(id='interval-component', interval=10000, n_intervals=0)
])

# Callback to update sensor values
@app.callback(
    [Output('sensor1-value', 'children'),
     Output('sensor2-value', 'children'),
     Output('sensor3-value', 'children')],
    [Input('interval-component', 'n_intervals')]
)
def update_sensor_values(n):
    global data
    data_list = update_data()

    # Update data dictionary
    for key, value in zip(data.keys(), data_list):
        data[key] = value

    return f"{data['Sensor1']:.2f}", f"{data['Sensor2']:.2f}", f"{data['Sensor3']:.2f}"

# Function to read data from Arduino
def update_data():
    serial_data = ser.readline().decode().strip()
    print(f"Serial data is: {serial_data}")
    data_list = [float(value) for value in serial_data.split(',')]
    return data_list

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
