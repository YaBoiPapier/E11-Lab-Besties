# coding=utf-8
 
import RPi.GPIO as GPIO
import time

#pin setup
count = 0
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#define callback
def pulse_counter(channel):
    global count
    count+= 1
   
    print("Count increase detected at:", time.time())

#user input runtime
exec_time = int(input("Enter execution time in seconds: "))
filename = input("File name: ")

#execute callback
GPIO.add_event_detect(23, GPIO.FALLING, callback=pulse_counter)


f = open(filename + ".csv", "w")
meta_data = ["Time","Counts per minute"]
for entry in meta_data:
    f.write(entry + ',')
f.write('\n')

try:
    count = 0
    start_time = time.monotonic()
    end_time = start_time + exec_time

    while time.monotonic() < end_time:
        time.sleep(1)
    
        if time.monotonic() - start_time >= 10:
            print("Number of counts in last minute:", count)
            data = [time.time(), count]
            for idata in data:
                f.write(str(idata)+ ',')
            f.write('\n')
            count = 0
            start_time = time.monotonic()

except KeyboardInterrupt:
        GPIO.cleanup()
f.close()
print("File saved to directory")
