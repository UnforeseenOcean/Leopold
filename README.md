# Leopold
Talking clock project made in just 3 weeks

# Introduction
This is a simple talking clock that focuses on hackability than practicality -- this thing is real hacky and it should not be used for examples of "good embedded devices programming"

The entire thing is written in Python and designed for Raspberry Pi 3.

# Build guide
The following will describe the build process of this project.

## Hardware / Components
You will need the following, but since this project is so simple this could be adapted and modified for other hardware, such as Raspberry Pi Zero or Orange Pi.
- DS3231 Real Time Clock module
    - Warning: If you are using a non-rechargeable CR2032 battery, cut the trace above the diode or remove the diode to disable the charging circuit, or the battery may explode.
    - Alternatively, you can use a rechargeable lithium battery which is designed for this circuit, but isn't made clear in the listing.
- Aosong AM2320 I2C temperature and humidity sensor
    - This could easily be substituted for other more accurate sensors.
- YwRobot I2C 16\*2 character LCD
    - You can substitute this with other displays that use I2C interface or SPI. This code will exclusively use this display.
- Raspberry Pi 3 or Raspberry Pi 3+
- Class 10 MicroSD card with capacity of at least 16GB
    - This code utilizes segmented audio, so fast access to files is important.
    - I recommend getting a new card for this.
- 5V 2.5A~ USB power supply
    - If you are seeing the yellow lightning bolt on the display, the power supply is too weak and it may cause RPi to crash when the speaker and/or the relay is activated!
- 104 ceramic capacitors
    - This is to reduce the clicking noise from the speakers when the relay turns on and off.
    - Connect this between positive and negative power connection on the amplifier.
- 100uF electrolytic capacitors
    - This is to stabilize the power supply.
    - Note: This may cause the dreaded yellow lightning bolt to appear during the boot. If this causes problems, lower the value of the capacitor.
- PAM8403 Mini 5V 1W amplifier board 
    - A version with variable volume is recommended.
    - If you don't care about the Bluetooth speaker portion or if you are okay with low quality and low volume audio, you can just use the cheap $1 speaker from your local store.
- 2 channel 5V relay module
    - Some modules are active low -- This means the module will turn on when you pull the input low (i.e. sink the current, not source it), and you will need to account for this when wiring this up.
    - If you don't need a Bluetooth speaker functionality, you can omit this.
    - Warning: Some relay modules will have a secondary jumper which, if removed, isolates the power supply of the relay. DO NOT move the jumper to the secondary position! This will short Vcc with GND and this will fry your board!
    - My module uses 150mA when both channels are turned on, which is a bit too much in my opinion -- since we are dealing with very low voltages, just use smaller low-current relays. 
    - But do not use solid-state relays. They don't take the audio signal well.
- 74LS14 hex inverter IC
    - This is used to prevent the floating line problem (half-on) on Raspberry Pi.
    - If your relay does not have an inverted logic (non-isolated ones usually are) use two inverter channels to flip the logic back.
    - If your relay has an inverted logic (isolated ones usually are) use one inverter channel for each input.
- Bluetooth audio board
    - Since we are using the relay to switch the input of the amplifier, you should use one that does not have an amplifier on-board.
    - If you have a mono audio or if you don't want a stereo audio, simply tie two channels together, preferably through two low-value resistors, one for each channel.
- 3.5" audio plug
    - This is used to connect to the Raspberry Pi's audio port unintrusively.
    - You might be able to get away with bare wires soldered to the port.
    - For Raspberry Pi Zero, you need to build a simple audio driver circuit. Everything else remains the same.
- A pair of 1 kilohm resistors
    - This is used just in case the configuration of the relay board is incorrect and it pulls too much current from the Raspberry Pi board.
    - It's a good idea to include one on the input and output pins to safeguard against overcurrent.
- Bunch of hook-up wires
    - Generic search term to use is "Arduino jumper wire". It's sometimes referred to as "Dupont wire"
- Some tinned solid-core wires
    - 30AWG and 25AWG wires are the common ones and this is pretty useful on soldering components on Veroboard / Perfboard.

## Tools
- Wire stripper
    - Get a sharp one. Seriously. You will thank me later.
- Wire cutter (flush cutter)
    - Anything will do but I recommend using one designed for circuits and not cutting steel wires.
- Screwdriver
    - Get one of those pen-shaped screwdrivers with interchangeable tips.
- MicroSD card reader
    - Get one that doesn't overheat. Nothing is worse than having to buy a new card because the card reader overheated and the controller decided it's too unsafe to let anyone write to the card again.
    - How do I know? Well...

## Software
- An image of Raspbian Buster or Stretch
    - I recommend one with Desktop, though it's not a requirement (you can use Lite).
- A voice pack from Asterisk/FreePBX
    - Warning: If you decide to redistribute the complete image, make sure you replace the voice samples with one you have permission to include! I'm using it here because it's the best voice pack I can get my hands on.
    - Another alternative would be utilizing Google TTS or even Cameo (a voice actor commission website) to get some voice samples.
    - Now this is where your creativity and ingenuity comes into play -- Let your creativity run wild! Make this thing speak in Russian, in a voice of Reinhardt, or even in Klingon if you want!
    - This is pretty easy to modify, add and remove. So, customize the voices and sequences to fit your needs.
    - My code was originally designed to have a time-based greeting (good morning/afternoon/evening/night) but I've decided to not do that for the time being.
    - To avoid copyright issues, the voice samples are not included. Instead, a detailed file description is included for the making of the voice clips.
- All of the Python code in the project directory
    - Refer to installation guide to set it up.
- Audacity, GoldWave or other audio editing program
    - This will be used to make the voice segments for your clock.
    - Since I included the descriptions and what it was supposed to say in a text file, it should be easy to make something that automatically assembles the audio according to the text in the quote marks.

# Installation Guide
Install a fresh copy of Raspbian Buster or Stretch.

Enable SSH, VNC and I2C using Raspberry Config utility.

Reboot your Raspberry Pi.

Clone or download this project.

Make the voice clips according to the `sound_desc.txt` in each folder. They must be named exactly as listed.

Using VNC, copy the entire project, including the voice clips (do not remove the folders) to a folder named `clock` on your Desktop.

Open the terminal and run the commands below in sequence:
```
sudio apt-get install portaudio19-dev
pip install PyAudio
sudo apt-get install mplayer
```

If you get audio errors, check if the interface is set correctly.

(Specifically, it might be set to HDMI audio if you're using analog output)

Or install ALSA tools and drivers:
```
sudo apt-get install alsa-tools alsa-utils
```
If you get low volume or no audio, use the following commands to initialize ALSA:
```
alsactl init
alsamixer
```

Then, run the following to make sure I2C support is active:
```
sudo apt-get install -y python-smbus
sudo apt-get install -y i2c-tools
```
Then run `sudo i2cdetect -y 1` to detect I2C devices.

If it shows nothing or doesn't show all devices, run `sudo i2cdetect -y -r 1`.

If it still doesn't show anything try power-cycling the I2C devices. 

(Unplug the devices or shut down RPi, then **unplug the power source**)

Test AM2320 by running `python am2320test.py`. It will print out the current temperature and humidity seen by the sensor.

AM2320 will go to sleep when not used -- it will appear during the first 3 seconds of boot.

Add the following to /boot/config.txt
```
dtoverlay=i2c-rtc,ds3231
```
Comment out the following from /lib/udev/hwclock-set
```
if [ -e /run/systemd/system ] ; then
    exit 0
fi
```
Check if the clock is working by using `sudo hwclock -r`.
If it doesn't match, use `sudo hwclock -w` to write a new time to RTC module.

You're almost done. Navigate into the `clock` folder on your desktop by typing `cd Desktop/clock` on your terminal.

Run `chmod 755 bootstrap.sh` to make the bootstrap script executable.

Run `crontab -e` then add this to the end of the file:
```
@reboot /home/pi/Desktop/clock/bootstrap.sh
```
Save and reboot. If everything has gone well, you'll hear a chime. If the relay is not turned off, you'll hear two different chimes.

You'll see the time and date displayed on the LCD.

Press the button. You'll hear the relay turn on and if you prepared the voice clips correctly, it will start speaking.

---

To test different date and time:

Run the following command and reboot.
```
systemctl disable systemd-timesyncd.service
```
Then set a new time using:
```
date -s yyyy-mm-dd hh:mm:ss
```
The time will update every few minutes, so wait few seconds for it to update.

To reenable NTP service, run:
```
systemctl enable systemd-timesyncd.service
```
Then reboot your Raspberry Pi.

## Credits

DS3231 library was provided by the Raspberry Pi community.

DS3231 setup info was from https://www.andreavinci.it/blog/en/2018/02/22/rapberry-pi-3-ds3231-real-time-clock/

The I2C LCD code was from https://gist.github.com/DenisFromHR/cc863375a6e19dce359d

AM2320 library and script was from https://github.com/Shoe-Pi/AM2320_Pi

Christmas notification sound provided by https://notificationsounds.com/
