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

#execute callback
GPIO.add_event_detect(23, GPIO.FALLING, callback=pulse_counter)

#user input runtime
exec_time = int(input("Enter execution time in seconds: "))

try:
    count = 0
    start_time = time.monotonic()
    end_time = start_time + exec_time

    while time.monotonic() < end_time:
        time.sleep(1)
    
    print("Number of counts in last", exec_time, "seconds:", count)

except KeyboardInterrupt:
        GPIO.cleanup()
      
print("Goodbye World!")
