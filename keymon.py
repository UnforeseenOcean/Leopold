# Key monitor script for Leopold
# Another ugly hack

from time import *
import sys
import os
import io
import subprocess
# Get the absolute path for compatibility
ap = os.path.dirname(os.path.abspath(__file__))
# Import Raspberry Pi GPIO library as "GPIO"
import RPi.GPIO as GPIO
# Set GPIO pin mapping to the actual board pins
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while (1 == 1):
    sleep(0.25)
    state = GPIO.input(7)
    if (state == 1):
        os.system("python " + ap + "/leopold.py")
	sleep(1)