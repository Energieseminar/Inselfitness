import pandas as pd
import serial
import time
# Serial communication setup for Raspberry Pi


# Initial data for plotting
data = pd.DataFrame(columns=['SolarCurrent', 'SolarVoltage', 'WindCurrent', 'WindVoltage',
                             'BatteryVoltage', 'BiogasPowerDraw', 'InverterPowerConsumption', 'WindSpeed',
                             'SolarRadiation', 'Temperature'])
data.to_csv("arduino_data.csv", sep=";", index_label="timestamp")



def get_fake_data():
    return  "SolarCurrent,100.50,SolarVoltage,24.00,WindCurrent,5.30,WindVoltage,12.00,BatteryVoltage,48.00,BiogasPowerDraw,120.00,InverterPowerConsumption,30.00,WindSpeed,8.50,SolarRadiation,800.00,Temperature,25.00".split(",")

def check_viablitiy(lines: list):
  print(len(lines)
  return 1

def get_data():
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=4) 
    lines = ser.readlines()
    time.sleep(4)
    decoded_lines = [line.decode() for line in lines]
    print(decoded_lines)
   #todo: rearrange lines to fit some layout 
    check_viablitiy(decoded_lines)
    
    return "Yes"
