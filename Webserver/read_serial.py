import pandas as pd
import serial
import time
# Serial communication setup for Raspberry Pi

#Example Serial decoded input: 
#['Messdaten Pin 2 - 14: \r\n', '(2) : 45\r\n', '(3) : 0\r\n', '(4) : 317\r\n', '(5) : 287\r\n', '(7) : 15\r\n', '(8) : 23\r\n', '(9) : 288\r\n', '(10) : 599\r\n', '(11) : 658\r\n', '(12) : 111\r\n', '(13) : 99\r\n']


# Initial data for plotting
data = pd.DataFrame(columns=['SolarCurrent', 'SolarVoltage', 'WindCurrent', 'WindVoltage',
                             'BatteryVoltage', 'BiogasPowerDraw', 'InverterPowerConsumption', 'WindSpeed',
                             'SolarRadiation', 'Temperature'])
data.to_csv("arduino_data.csv", sep=";", index_label="timestamp")

def get_fake_data():
    return  "SolarCurrent,100.50,SolarVoltage,24.00,WindCurrent,5.30,WindVoltage,12.00,BatteryVoltage,48.00,BiogasPowerDraw,120.00,InverterPowerConsumption,30.00,WindSpeed,8.50,SolarRadiation,800.00,Temperature,25.00".split(",")

def check_viablitiy(lines: list):
    print(len(lines))
    if len(lines)!=12:
      return False
    if lines[0]!="Messdaten Pin 2 - 14: \r\n":
      return False
    if lines[11][0:4]!= "(13)":
      return False
    return True

def get_data():
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=4) 
    lines = ser.readlines()
    time.sleep(4)
    decoded_lines = [line.decode().strip() for line in lines]
    print(decoded_lines)
   #todo: rearrange lines to fit some layout 
    if check_viablitiy(decoded_lines):
        stripped_lines = [dec.strip() for dec in decoded_lines]
    else: 
        striped_lines = None
    print(striped_lines)
    return ";".join(striped_lines)
