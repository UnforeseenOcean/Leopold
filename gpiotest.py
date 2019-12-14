# GPIO test

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setup(13, GPIO.OUT)
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while (1 == 1):
    time.sleep(1)
    state = GPIO.input(7)
    if (state == 1):
        print "GPIO 4 TRIGGERED"
        GPIO.output(13, GPIO.HIGH)
    else:
        GPIO.output(13, GPIO.LOW)