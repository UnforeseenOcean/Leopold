#!/bin/sh
# Bootstrap code for Leopold
# Run "chmod 755 bootstrap.sh"
# Use crontab -e then add:
# "@reboot /path/to/your/bootstrap/script/file"
# @reboot /home/pi/Desktop/clock/bootstrap.sh
# Ensure the directory is on top of user-accessible directory
cd /
echo "Bootstrap code running"
# Go to the Pi desktop folder and enter the project folder
cd /home/pi/Desktop/clock
python init.py
echo "Process terminated"