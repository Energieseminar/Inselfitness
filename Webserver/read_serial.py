import pandas as pd
import serial
# Serial communication setup for Raspberry Pi


# Initial data for plotting
data = pd.DataFrame(columns=['SolarCurrent', 'SolarVoltage', 'WindCurrent', 'WindVoltage',
                             'BatteryVoltage', 'BiogasPowerDraw', 'InverterPowerConsumption', 'WindSpeed',
                             'SolarRadiation', 'Temperature'])
data.to_csv("arduino_data.csv", sep=";", index_label="timestamp")

def get_data():
    ser = serial.Serial('/dev/ttyACM0', 9600)  # Adjust the port and baud rate accordingly

    lines = [ser.readline() for _ in range(12)]
    return lines

def get_fake_data():
    return  "SolarCurrent,100.50,SolarVoltage,24.00,WindCurrent,5.30,WindVoltage,12.00,BatteryVoltage,48.00,BiogasPowerDraw,120.00,InverterPowerConsumption,30.00,WindSpeed,8.50,SolarRadiation,800.00,Temperature,25.00".split(",")
