# Initialization script for Leopold
# Initializes the GPIO and tests audio output
# Warning: This code is nasty
# -*- coding: utf-8 -*-
# requires RPi_I2C_driver.py
import RPi_I2C_driver
from time import *
import subprocess
import sys
import os
import io
import subprocess
import threading
lcd = RPi_I2C_driver.lcd()
# Splash screen
lcd.lcd_clear()
lcd.lcd_display_string("Leopold V1.7", 1)
lcd.lcd_display_string("github.com/Unfor", 2)
sleep(0.5)
lcd.lcd_display_string("thub.com/Unfores", 2)
sleep(0.5)
lcd.lcd_display_string("/UnforeseenOcean", 2)
sleep(0.5)
lcd.lcd_display_string("eenOcean/Leopold", 2)
sleep(0.5)
lcd.lcd_display_string("/Leopold        ", 2)
sleep(0.5)
lcd.lcd_display_string("                ", 2)
sleep(0.5)
# Get the absolute path for compatibility
ap = os.path.dirname(os.path.abspath(__file__))
# Import Raspberry Pi GPIO library as "GPIO"
import RPi.GPIO as GPIO
# Set GPIO pin mapping to the actual board pins
GPIO.setmode(GPIO.BOARD)
# Set pin 13 as output (goes to the relay)
GPIO.setup(13, GPIO.OUT)
# Set pin 7 (goes to the button) as input and make the pull-down resistor active
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# Pull the output low
GPIO.output(13, GPIO.LOW)
sleep(1)
# This audio will not play since the amp is switched to AUX
os.system("aplay " + ap + "/state/init.wav")
sleep(1)
# Turn on the relay
GPIO.output(13, GPIO.HIGH)
# Wait a bit to make sure the amp is ready
sleep(0.25)
# Play the startup sound
os.system("aplay " + ap + "/state/startup.wav")
# Making sure the file buffer is cleared
sleep(0.1)
# Turn off the relay
GPIO.output(13, GPIO.LOW)
# Spawn jesse.py thread with stay-resident version
# This uses os.spawnlp which may be dangerous
os.spawnlp(os.P_NOWAIT, "python", "", "jesse_sr.py")
print "Initialization done"
# Start key monitor
execfile("keymon.py")