import adafruit_bme680
import time
import board
import argparse
import datetime
# Air quality sensor modules
import busio
from digitalio import DigitalInOut, Direction, Pull
from adafruit_pm25.i2c import PM25_I2C

# Weather Sensor script
i2c = board.I2C()
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)

bme680.sea_level_pressure = 1013.25

t_end = time.time() + 60 * 15
while time.time() < t_end:
	t = time.localtime()
	current_time = time.strftime("%H:%M:%S", t)
	print("\nTime: " + current_time + "- Temperature: %0.1f C | Gas: %d ohm | Humidity : %0.1f %% | Pressure: %0.3f hPa. | Altitude = %0.2f meters." % (bme680.temperature, bme680.gas, bme680.relative_humidity, bme680.pressure, bme680.altitude))
	time.sleep(1)
  
# Week 4 script
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
Example sketch to connect to PM2.5 sensor with either I2C or UART.
"""

# pylint: disable=unused-import

reset_pin = None
# If you have a GPIO, its not a bad idea to connect it to the RESET pin
# reset_pin = DigitalInOut(board.G0)
# reset_pin.direction = Direction.OUTPUT
# reset_pin.value = False


# For use with a computer running Windows:
# import serial
# uart = serial.Serial("COM30", baudrate=9600, timeout=1)

# For use with microcontroller board:
# (Connect the sensor TX pin to the board/computer RX pin)
# uart = busio.UART(board.TX, board.RX, baudrate=9600)

# For use with Raspberry Pi/Linux:
import serial
uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=0.95)

# For use with USB-to-serial cable:
# import serial
# uart = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=0.25)

# Connect to a PM2.5 sensor over UART
from adafruit_pm25.uart import PM25_UART
pm25 = PM25_UART(uart, reset_pin)

# Create library object, use 'slow' 100KHz frequency!
# i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
# Connect to a PM2.5 sensor over I2C
# pm25 = PM25_I2C(i2c, reset_pin)

print("Found PM2.5 sensor, reading data...")
timeout = time.time() + 30 #30 seconds

# writing csv file
f = open("pmdata.csv", "w")
meta_data = ["Time","PM10 Standard (mirogram/m^3)", "PM25 Standard (mirogram/m^3)", "PM100 Standard (mirogram/m^3)"]
for entry in meta_data:
    f.write(entry + ',')
f.write('\n')

while True:
    time.sleep(1)
    if time.time() > timeout:
        break

    try:
        aqdata = pm25.read()
        # print(aqdata)
    except RuntimeError:
        print("Unable to read from sensor, retrying...")
        continue
    
    ct = datetime.datetime.now()
    ts = ct.timestamp()
    print("Current Time:-", ct)
    print("Timestamp:-", ts)
    print("Concentration Units (standard)")
    print("---------------------------------------")
    print(
        "PM 1.0: %d\tPM2.5: %d\tPM10: %d"
        % (aqdata["pm10 standard"], aqdata["pm25 standard"], aqdata["pm100 standard"])
    )
    # edit csv file during while loop
    data = [ts, aqdata["pm10 standard"], aqdata["pm25 standard"], aqdata["pm100 standard"]]
    for idata in data:
        f.write(str(idata)+ ',')
    f.write('\n')
    
    print("Concentration Units (environmental)")
    print("---------------------------------------")
    print(
        "PM 1.0: %d\tPM2.5: %d\tPM10: %d"
        % (aqdata["pm10 env"], aqdata["pm25 env"], aqdata["pm100 env"])
    )
    print("---------------------------------------")
    print("Particles > 0.3um / 0.1L air:", aqdata["particles 03um"])
    print("Particles > 0.5um / 0.1L air:", aqdata["particles 05um"])
    print("Particles > 1.0um / 0.1L air:", aqdata["particles 10um"])
    print("Particles > 2.5um / 0.1L air:", aqdata["particles 25um"])
    print("Particles > 5.0um / 0.1L air:", aqdata["particles 50um"])
    print("Particles > 10 um / 0.1L air:", aqdata["particles 100um"])
    print("---------------------------------------")
    
#while loop ends here
f.close()
print("Data saved to .csv file in directory")
