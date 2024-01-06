from flask import Flask
from dash import Dash, dcc, html, Input, Output
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import serial

# Serial communication setup for Windows
ser = serial.Serial('COM3', 9600)  # Adjust the COM port and baud rate accordingly


# Function to read data from Arduino
def update_data():
    serial_data = ser.readline().decode().strip()
    data_list = [float(value) for value in serial_data.split(',')]
    return data_list

# Flask app setup
server = Flask(__name__)
app = Dash(__name__, server=server)

# Initial data for plotting
data = {'Sensor1': [], 'Sensor2': [], 'Sensor3': []}

# Dash layout
app.layout = html.Div([
    dcc.Graph(id='live-plot'),
    dcc.Interval(id='interval-component', interval=1000, n_intervals=0)
])

# Callback to update live plot
@app.callback(Output('live-plot', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_plot(n):
    global data
    data_list = update_data()

    # Update data dictionary
    for key, value in zip(data.keys(), data_list):
        data[key].append(value)

    # Plot data
    plt.clf()
    plt.plot(data['Sensor1'], label='Sensor1')
    plt.plot(data['Sensor2'], label='Sensor2')
    plt.plot(data['Sensor3'], label='Sensor3')
    plt.title('Live Sensor Data')
    plt.xlabel('Time')
    plt.ylabel('Sensor Values')
    plt.legend()

    # Convert Matplotlib plot to Plotly format
    fig = plt.gcf()
    plotly_fig = dict(data=fig2plotly(fig))

    return plotly_fig

# Function to convert Matplotlib plot to Plotly format
def fig2plotly(fig):
    import plotly.graph_objs as go
    import numpy as np

    data = []
    for trace in fig.get_axes():
        y = trace.get_ydata()
        x = np.arange(len(y))
        name = trace.get_label()

        data.append(go.Scatter(x=x, y=y, name=name))

    layout = go.Layout(title=fig.get_axes()[0].get_title(),
                       xaxis=dict(title=fig.get_axes()[0].get_xlabel()),
                       yaxis=dict(title=fig.get_axes()[0].get_ylabel()))

    return dict(data=data, layout=layout)

if __name__ == '__main__':
    app.run_server(debug=True)
