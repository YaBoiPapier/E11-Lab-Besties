import adafruit_bme680
import time
import board
import argparse
import sys
import datetime
# Air quality sensor modules
import busio
from digitalio import DigitalInOut, Direction, Pull
from adafruit_pm25.i2c import PM25_I2C

# Weather Sensor script setup
i2c = board.I2C()
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)

bme680.sea_level_pressure = 1013.25

# air quality sensor script setup
reset_pin = None

import serial
uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=0.95)

from adafruit_pm25.uart import PM25_UART
pm25 = PM25_UART(uart, reset_pin)

print(sys.argv)

# csv file setup
f = open("pmdata.csv", "w")
meta_data = ["Time","Temperature (C)","Gas (ohms)","Humidity (%)","Pressure (hPa)","Altitude (m)","PM10 Standard (mirogram/m^3)", "PM25 Standard (mirogram/m^3)", "PM100 Standard (mirogram/m^3)"]
for entry in meta_data:
    f.write(entry + ',')
f.write('\n')

start_time = time.time()
run_time = int(sys.argv[1])
itime = start_time

while itime < (start_time + run_time):
    # Weather sensor
    itime = time.time()
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print("\nTime: " + current_time + "- Temperature: %0.1f C | Gas: %d ohm(s) | Humidity : %0.1f %% | Pressure: %0.3f hPa. | Altitude = %0.2f meters." % (bme680.temperature, bme680.gas, bme680.relative_humidity, bme680.pressure, bme680.altitude))
    # Air quality sensor
    try:
        aqdata = pm25.read()
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
    data = [itime, bme680.temperature, bme680.gas, bme680.relative_humidity, bme680.pressure, bme680.altitude, aqdata["pm10 standard"], aqdata["pm25 standard"], aqdata["pm100 standard"]]
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
    time.sleep(1)
f.close()
print("Data saved to .csv file in directory")
