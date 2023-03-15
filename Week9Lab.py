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
    print(time.time())

#execute callback
GPIO.add_event_detect(23, GPIO.FALLING, callback=pulse_counter)

while True:
    try:
        count = 0
        time.sleep(60)
        print("Number of counts in last minute:", count)
        message = raw_input('\nPress any key to exit:\n')
    except KeyboardInterrupt:
        GPIO.cleanup()
      
print("Goodbye World!")
