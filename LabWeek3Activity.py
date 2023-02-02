import adafruit_bme680
import time
import board

i2c = board.I2C()
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)

bme680.sea_level_pressure = 1013.25

t_end = time.time() + 60 * 15
while time.time() < t_end:
#	print("\nTemperature: %0.1f C" % bme680.temperature)
#	print("Gas %d ohm" % bme680.gas)
#	print ("Humidity : %0.1f %%" % bme680.relative_humidity)
#	print("Pressure: %0.3f hPa" % bme680.pressure)
#	print("Altitude = %0.2f meters" % bme680.altitude)
#	print(current_time)
	t = time.localtime()
	current_time = time.strftime("%H:%M:%S", t)
	print("\nTime: " + current_time + "- Temperature: %0.1f C | Gas: %d ohm | Humidity : %0.1f %% | Pressure: %0.3f hPa. | Altitude = %0.2f meters." % (bme680.temperature, bme680.gas, bme680.relative_humidity, bme680.pressure, bme680.altitude))
	time.sleep(1)
	
