# Jesse - I2C LCD updater script
# -*- coding: utf-8 -*-
# https://gist.github.com/DenisFromHR/cc863375a6e19dce359d
# This is ugly, don't use this

# requires RPi_I2C_driver.py
import RPi_I2C_driver
from time import *
from datetime import datetime as dt
import sys
import os
import io
import json
import subprocess
import AM2320
sensor = AM2320.AM2320()
lcd = RPi_I2C_driver.lcd()
# This is a cut-down version the Morrison and Maui
# This will hopefully run in the background and update the LCD with new info

# Get the absolute path for compatibility
ap = os.path.dirname(os.path.abspath(__file__))
# Populate a global variable with current time
cur = dt.now()
# Various global variables
htt = ""
hru = ""
dispu = "C"
minute = ""
hrtmp = 0
temp = 0
humid = 0
tempo = 0
tempa = 0
tempb = ""
hmtmp = ""
# Read the config file, no need to update it every loop

with open('config.json') as json_file:
    data = json.load(json_file)
print "Jesse LCD Handler loaded."    
lcd.lcd_clear()
if (cur.strftime("%m%d") == "1225"):
    print "God Jul och Gott Nytt År! - Torbjörn"
    lcd.lcd_display_string("God Jul! :D", 1)
    lcd.lcd_display_string("- Torbj"+chr(239)+"rn", 2)
    sleep(3)
    lcd.lcd_clear()
def updateTime():
   cur = dt.now() 
def updateData():
    while (1 == 1):
        updateTime()
        cur = dt.now()
        unit = data['tempUnit']
        mode = data['hourType']
        # In debug mode, use the value in the config
        if (data['debug'] == 'true'):
            temp = data['debugTemp']
            humid = data['debugHumid']
        else:
            sensor.get_data()
            temp = str(sensor.temperature)
            humid = str(sensor.humidity)
            
        temp = int(round(float(temp)))
        humid = int(round(float(humid)))
        hmtmp = str(humid)
        # print "Debug: temp:", temp, "humid:", humid, type(temp), type(humid)
        
        # Sanity check, check if the sensor is reporting crazy values like 5000C or 900% RH
        # This is 102 due to the round() function
        if (humid < 0) or (humid > 102):
            os.system("aplay " + ap + "/state/oops.wav")
            sys.exit("Sensor error (Humidity is too low or too high)! Exiting.")
        # This is 82 because of the round() function
        if (temp < -40) or (temp > 82):
            os.system("aplay " + ap + "/state/oops.wav")
            sys.exit("Sensor error (Temperature is too low or high)! Exiting.")

        if unit == 'k':
            tempo = temp + 273.15
            tempa = int(round(tempo))
            tempb = str(tempa)
            dispu = "K"
        elif unit == 'f':
            tempo = (temp*9/5)+32
            tempa = int(round(tempo))
            tempb = str(tempa)
            dispu = "F"
        else:
            unit = 'c'
            tempa = temp
            tempb = str(tempa)
            dispu = "C"
            
        hour = cur.strftime("%H")
        # Convert it to int so we can do math stuff
        hrtmp = int(cur.strftime("%H"))
        minute = cur.strftime("%M")
        if (mode == 12):
            # When it's past noon (12PM~11PM)
            if (hrtmp > 12):
                # print "It is past noon."
                # Subtract 12 to get a 12hr value (13:00 -> 1PM) 
                hrtemp = hrtmp - 12
                if hrtemp < 10:
                    # If the result is less than 10, e.g. 09:00 PM
                    htt = "0" + str(hrtemp)
                else:
                    htt = str(hrtemp)
                hru = "PM"
            # When it's 0:00 (12AM)
            elif (hrtmp == 0):
                # print "It is midnight."
                # Add 12 to make it 12:00 AM
                hrtemp = hrtmp + 12
                htt = str(hrtemp)
                hru = "AM"
            elif (hrtmp <= 9):
                # 01:00~09:00
                hrtemp = hrtmp
                htt = "0" + str(hrtemp)
                hru = "AM"
            elif (hrtmp == 10) or (hrtmp == 11):
                # 10:00~11:00
                hrtemp = hrtmp
                htt = str(hrtemp)
                hru = "AM"
            elif (hrtmp == 12):
                # 12:00 
                hrtemp = hrtmp
                htt = str(hrtemp)
                hru = "PM"
            else:
                htt = hour
                hru = " "
                # End of if-else logic
        else:
            # If it's in 24hr mode, ignore the logic and read the time as-is
            if (hrtmp <= 9):
                # print "It is before noon."
                # Add 0 to make it 01:00 AM
                hrtemp = hrtmp
                htt = "0" + str(hrtemp)
                hru = " "
            htt = hour
            hru = " "
        # End of function

        # Update the display every 30 seconds
        lcd.lcd_clear()
        lcd.lcd_display_string(cur.strftime("%A"), 1)
        lcd.lcd_display_string(cur.strftime("%b %d %Y"), 2)
        sleep(3)
        lcd.lcd_clear()
        lcd.lcd_display_string(htt + ":" + minute + " " + hru, 1)
        if unit == 'k':
            lcd.lcd_display_string(tempb + dispu + " " + hmtmp + "% RH", 2)
        else:
            lcd.lcd_display_string(tempb + chr(223) + dispu + " " + hmtmp + "% RH", 2)
        sleep(7)

updateData()