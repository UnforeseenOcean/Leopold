# Leopold Main Speech Synthesis Code
# -*- coding: utf-8 -*-


# Copyright 2019 Blackbeard Softworks, all rights reserved
# Warning! This uses voices from Asterisk. Please replace the voice samples with the one you have license to redistribute!

# Prereqs are required! Run the commands below in sequence:
# sudio apt-get install portaudio19-dev
# pip install PyAudio
# sudo apt-get install mplayer

# If you get audio errors, check if the interface is set correctly
# (Specifically, HDMI audio if you're using analog output)
# Or install ALSA tools and drivers:
# sudo apt-get install alsa-tools alsa-utils
# Then if you get low volume or no audio:
# alsactl init
# alsamixer

# To test different date and time:
# Run the following command and reboot
# systemctl disable systemd-timesyncd.service
# Then set a new time using:
# date -s yyyy-mm-dd hh:mm:ss
# The time will update every few minutes
# To reenable NTP service, run:
# systemctl enable systemd-timesyncd.service
# Reboot and wait

# Install I2C tools:
# sudo apt-get install -y python-smbus
# sudo apt-get install -y i2c-tools
# Then run sudo i2cdetect -y 1 to detect I2C devices
# If it shows nothing or doesn't show all devices, run sudo i2cdetect -y -r 1
# If it still doesn't show anything try power-cycling the I2C devices

# Test AM2320 by running python am2320test.py
# Code: github.com/Shoe-Pi/AM2320_Pi
# AM2320 will go to sleep when not used -- it will appear during the first 3 seconds of boot

# https://www.andreavinci.it/blog/en/2018/02/22/rapberry-pi-3-ds3231-real-time-clock/
# Add the following to /boot/config.txt
# dtoverlay=i2c-rtc,ds3231
# Comment out the following from /lib/udev/hwclock-set
# if [ -e /run/systemd/system ] ; then
#     exit 0
# fi
# Check if the clock is working by using sudo hwclock -r
# If it doesn't match, use sudo hwclock -w to write a new time to RTC module
# non-SU command will fail because it's used by the driver!

# The code is highly unoptimized and is only for demonstration purposes
# If you want to optimize this, please be my guest

from datetime import datetime as dt
import sys
import os
import io
import json
import subprocess
import RPi_I2C_driver
import time
import AM2320
# Import Raspberry Pi GPIO library as "GPIO"
import RPi.GPIO as GPIO
# Define "sensor" as alias for AM2320
sensor = AM2320.AM2320()
# Set GPIO pin mapping to the actual board pins
GPIO.setmode(GPIO.BOARD)
# Set pin 13 as output (goes to the relay)
GPIO.setup(13, GPIO.OUT)
# Set pin 7 (goes to the button) as input and make the pull-down resistor active
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# Get the absolute path for compatibility
ap = os.path.dirname(os.path.abspath(__file__))

cur = dt.now()
pauses = "aplay " + ap + "/silence1.wav"
pausem = "aplay " + ap + "/silence2.wav"
pausel = "aplay " + ap + "/silence3.wav"

# Read the config
with open('config.json') as json_file:
    data = json.load(json_file)
    print data['tempUnit']
# In debug mode, use the value in the config
if (data['debug'] == 'true'):
    temp = data['debugTemp']
    humid = data['debugHumid']
else:
    sensor.get_data()
    temp = str(sensor.temperature)
    humid = str(sensor.humidity)

# Convert string into float then round it, then convert it into int
# Using just int will throw away anything below 1 which is not what we want
# Using round on this will throw an error since it's a string so we do need float()
# Using int directly will ruin the value as previously stated

# int(9.65) == 9
# int(round(9.65)) == 10

# Use this code for later
temp = int(round(float(temp)))
humid = int(round(float(humid)))
print "Debug: temp:", temp, "humid:", humid, type(temp), type(humid)

# Sanity check, check if the sensor is reporting crazy values like 5000C or 900% RH
# This is 102 due to the round() function
if (humid < 0) or (humid > 102):
    os.system("aplay " + ap + "/state/oops.wav")
    sys.exit("Sensor error (Humidity is too low or too high)! Exiting.")
# This is 82 because of the round() function
if (temp < -40) or (temp > 82):
    os.system("aplay " + ap + "/state/oops.wav")
    sys.exit("Sensor error (Temperature is too low or high)! Exiting.")

# Read the unit setting
unit = data['tempUnit']
if unit == 'k':
    print "Unit is Kelvin."
    # K = C + 273.15
    tempo = temp + 273.15
    # And convert it to int 
    tempa = int(round(tempo))
    tempb = str(tempa)
elif unit == 'f':
    print "Unit is Fahrenheit."
    # Formula for C to F conversion
    # (C * 9/5) + 32 = F
    tempo = (temp*9/5)+32
    tempa = int(round(tempo))
    tempb = str(tempa)
else:
    # Assume everything else is Celsius
    print "Unit is Celsius or invalid, assuming C."
    # Put a default value here just in case, overwriting it
    unit = 'c'
    # Since we already converted everything to int properly we don't need to do anything
    # Just plug the value directly into the function
    tempa = temp
    tempb = str(tempa)

def readTemp():
    # If the unit is Fahrenheit
    if (unit == 'f'):
        print "Temperature is", tempa, "F"
        if (tempa > 99):
            print "Temperature is above 99F."
            # Get the second and third number for reading
            tempc = tempb[1:3]
            # Since the temperature will never go over 180F we will not care about anything above it
            os.system("aplay " + ap + "/temp/100.wav")
            os.system("aplay " + ap + "/temp/" + tempc + ".wav")
            os.system("aplay " + ap + "/temp/fahrenheit.wav")
        elif (tempa < 0):
            print "Temperature is below 0F."
            # Convert value to str, apply strip() to remove the negative sign
            # strip() cannot be used on anything other than string
            tempn = tempb.strip('-')
            os.system("aplay " + ap + "/temp/minus.wav")
            # We will not care about anything below 40 because it will be limited
            os.system("aplay " + ap + "/temp/" + tempn + ".wav")
            os.system("aplay " + ap + "/temp/fahrenheit.wav")
        elif (tempa < 99) and (tempa > 0):
            print "Temperature is between 1 and 99F."
            # Get the second and third number for reading
            os.system("aplay " + ap + "/temp/" + tempb + ".wav")
            os.system("aplay " + ap + "/temp/fahrenheit.wav")
        else:
            # This else statement should never fire
            os.system("aplay " + ap + "/state/oops.wav")
            sys.exit("Programming error (func: readTemp(), fahrenheit)! Exiting.")
            
    # If the unit is Kelvin
    elif (unit == 'k'):
        print "Temperature is", tempa, "K"
        # There should be no more than 3 digits because the number is between 233 and 353
        if (len(str(tempa)) == 3):
            # Get the second and third number for reading
            # Since it will never go below 200 we will not care about anything below 200
            kvn = tempb[0:1]
            tempc = tempb[1:3]
            # *50
            os.system("aplay " + ap + "/temp/" + kvn + ".wav")
            os.system("aplay " + ap + "/temp/100k.wav")
            os.system("aplay " + ap + "/temp/" + tempc + ".wav")
            os.system("aplay " + ap + "/temp/kelvin.wav")
        else:
            # This else statement should never fire
            os.system("aplay " + ap + "/state/oops.wav")
            sys.exit("Programming error (func: readTemp(), kelvin)! Exiting.")
        
    # If the unit is Celsius
    elif (unit == 'c'):
        print "Temperature is", tempa, "C"
        # Since the temperature never goes up above 80, we will not care about it
        if (tempa < 0):
            print "Temperature is below 0C."
            # Convert value to str, apply strip() to remove the negative sign
            # strip() cannot be used on anything other than string
            tempy = tempb.strip('-')
            os.system("aplay " + ap + "/temp/minus.wav")
            # We will not care about anything below 40 because it will be limited
            os.system("aplay " + ap + "/temp/" + tempy + ".wav")
            os.system("aplay " + ap + "/temp/celsius.wav")
        elif (tempa < 82) and (tempa > 0):
            print "Temperature is between 1 and 82C."
            # Get the second and third number for reading
            os.system("aplay " + ap + "/temp/" + tempb + ".wav")
            os.system("aplay " + ap + "/temp/celsius.wav")
        else:
            # This else statement should never fire
            os.system("aplay " + ap + "/state/oops.wav")
            sys.exit("Programming error (func: readTemp(), celsius)! Exiting.")
    
    # This else statement should never fire
    else:
        os.system("aplay " + ap + "/state/oops.wav")
        sys.exit("Programming error (func: readTemp(), unsafe)! Exiting.")
    # End of function
    
def readHumid():
    humids = str(humid)
    if (humid >= 100):
        print "Humidity is over or equal to 100, assuming 100."
        humids = "100"
        os.system("aplay " + ap + "/humid/humidity.wav")
        os.system("aplay " + ap + "/humid/" + humids + ".wav")
        os.system("aplay " + ap + "/humid/percent.wav")
    elif (humid < 0):
        print "Humidity is below 0, assuming 0."
        humids = "0"
        os.system("aplay " + ap + "/humid/humidity.wav")
        os.system("aplay " + ap + "/humid/" + humids + ".wav")
        os.system("aplay " + ap + "/humid/percent.wav")
    elif (humid < 101) and (humid > 0):
        print "Humidity is", humid, "%"
        os.system("aplay " + ap + "/humid/humidity.wav")
        os.system("aplay " + ap + "/humid/" + humids + ".wav")
        os.system("aplay " + ap + "/humid/percent.wav")
    else:
        os.system("aplay " + ap + "/state/oops.wav")
        sys.exit("Programming error (func: readHumid(), unsafe)! Exiting.")
    # End of function

def playAlert():
    # You're the best thing about Christmas!
    mfcm = cur.strftime("%m")
    dfcm = cur.strftime("%d")
    alert = "aplay " + ap + "/state/alert.wav"
    xmas = "aplay " + ap + "/state/christmas.wav"
    if (mfcm == '12') and (dfcm == '25'):
        os.system(xmas)
    else:
        os.system(alert)
    # End of function

def printTime():
    print " "
    print "The time is " + cur.strftime("%Y-%m-%d %H:%M:%S")
    print " "
    # End of function
    
def readYear():
    year = cur.strftime("%Y")
    # Bad programming, gets each letter of the year
    # * denotes the character being fetched, example year is 2019
    # **19
    yra = year[0:2]
    # 20**
    yrb = year[2:4]
    # *019
    yrn = year[0:1]
    # 2*19
    yrp = year[1:2]
    # 20*9
    yrs = year[2:3]
    # 201*
    yre = year[3:4]
    print yra, yrb, yrn, yrp, yrs, yre
    # If the year contains no other numbers at hundredth, tenth and below, such as "2000"
    if (yrp == '0') and (yrs == '0') and (yre == '0'):
        print "Year does not contain numbers below thousandth digit"
        os.system("aplay " + ap + "/year/the-year.wav")
        os.system("aplay " + ap + "/year/0" + yrn + ".wav")
        os.system("aplay " + ap + "/year/thousand.wav")
    # If the year contains no numbers at hundredth and tenth digit, such as "2009"
    elif (yrp == '0') and (yrs == '0') and (yre != '0'):
        print "Year does not contain numbers on thousandth and hundredth digit"
        os.system("aplay " + ap + "/year/0" + yrn + ".wav")
        os.system("aplay " + ap + "/year/thousand.wav")
        os.system("aplay " + ap + "/year/and.wav")
        os.system("aplay " + ap + "/year/0" + yre + ".wav")
    # If the year contains no numbers at hundredth digit, such as 2019 or 2319
    # Unix Epoch detector is built in
    elif (year > 1969):
        print "Year does not contain numbers on hundredth digit"
        # os.system("aplay " + ap + "/year/the-year.wav")
        os.system("aplay " + ap + "/year/" + yra + ".wav")
        os.system("aplay " + ap + "/year/" + yrb + ".wav")        
    # This else statement should never fire
    else:
        os.system("aplay " + ap + "/state/oops.wav")
        sys.exit("Programming error! Exiting.")
    # End of function
def readHour():
    hour = cur.strftime("%H")
    # Convert it to int so we can do math stuff
    hrtmp = int(cur.strftime("%H"))
    minute = cur.strftime("%M")
    hr = "aplay " + ap + "/hour/" + hour + ".wav"
    mn = "aplay " + ap + "/minute/" + minute + ".wav"
    print type(hour)
    mode = data['hourType']
    print type(mode)
    # If the config says it's 12 hour mode
    if (mode == 12):
        print "Hour: 12hr mode"
        # When it's past noon (12PM~11PM)
        if (hrtmp >= 12):
            print "It is past noon."
            # Subtract 12 to get a 12hr value (13:00 -> 1PM) 
            hrtemp = hrtmp - 12
            htt = str(hrtemp)
            os.system("aplay " + ap + "/hour/" + htt + ".wav")
            os.system(pauses)
            os.system(mn)
            os.system("aplay " + ap + "/minute/p-m.wav")
        # When it's 0:00 (12AM)
        elif (hrtmp == 0):
            print "It is midnight."
            # Add 12 to make it 12:00 AM
            hrtemp = hrtmp + 12
            htt = str(hrtemp)
            os.system("aplay " + ap + "/hour/" + htt + ".wav")
            os.system(pauses)
            os.system(mn)
            os.system("aplay " + ap + "/minute/a-m.wav")
        else:
            # Read it as-is since it's same on all formats
            print "It is before noon."
            os.system("aplay " + ap + "/hour/" + hour + ".wav")
            os.system(pauses)
            os.system(mn)
            os.system("aplay " + ap + "/minute/a-m.wav")
            # End of if-else logic
    else:
        # If it's in 24hr mode, ignore the logic and read the time as-is
        print "Hour: 24hr mode"
        os.system(hr)
        os.system(pauses)
        os.system(mn)
    # End of function

# A function to update the time variable
def updateTime():
    # Get current time
    print "Updating time..."
    cur = dt.now()
    # Format the date and time, does what it says
    # Refer to: https://docs.python.org/2/library/datetime.html
    hour = cur.strftime("%H")
    minute = cur.strftime("%M")
    day = cur.strftime("%d")
    month = cur.strftime("%m")
    year = cur.strftime("%Y")
    # Filter out illegal year since Python uses Unix Epoch time, which is limited to 00:00:00 January 1, 1970
    if (year < 1970):
        os.system("aplay " + ap + "/state/error_invalid_time.wav")
        sys.exit("Time is invalid! Exiting.")
    # Returns the weekday as integer, Sunday is 0, Saturday is 6
    weekday = cur.strftime("%w")
    print "mm dd yyyy H:M nth weekday", month, day, year, hour, minute, weekday
    
    # Append absolute path
    
    # hr = "aplay " + ap + "/hour/" + hour + ".wav"
    dayis = "aplay " + ap + "/month/today-is.wav"
    wd = "aplay " + ap + "/weekday/" + weekday + ".wav"
    mo = "aplay " + ap + "/month/" + month + ".wav"
    dat = "aplay " + ap + "/day/" + day + ".wav"
    
    # yr = "aplay " + ap + "/year/" + year + ".wav"
    
    
    # Play alert sound
    playAlert()
    # Read the hour and minute
    readHour()
    # Pause for 0.5s
    os.system(pausem)
    # "Today is"
    os.system(dayis)
    # Read weekday
    os.system(wd)
    # Pause for 0.25s
    os.system(pauses)
    # Read month
    os.system(mo)
    # Pause for 0.25s
    #os.system(pauses)
    # Read day
    os.system(dat)
    # Pause for 0.5s
    os.system(pausem)
    # Read the year
    readYear()
    # End of function

# os.system is not supposed to be used here but it doesn't work otherwise

# End of function definition

# Turn on the relay
GPIO.output(13, GPIO.HIGH)
# Read time
updateTime()
# Print time
printTime()
os.system(pausem)
readTemp()
readHumid()
# Turn off the relay
GPIO.output(13, GPIO.LOW)