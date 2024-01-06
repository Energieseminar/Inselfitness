import serial

# Serial communication setup for Raspberry Pi
ser = serial.Serial('/dev/ttyACM0', 9600)  # Adjust the port and baud rate accordingly

try:
    while True:
        serial_data = ser.readline().decode().strip()
        print("Received data:", serial_data)

except KeyboardInterrupt:
    print("Script terminated by user.")
finally:
    ser.close()
