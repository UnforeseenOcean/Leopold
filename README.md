# Leopold
Talking clock project made in just 3 weeks

# Introduction
This is a simple talking clock that focuses on hackability than practicality -- this thing is real hacky and it should not be used for examples of "good embedded devices programming"

The entire thing is written in Python and designed for Raspberry Pi 3.

# Hardware
You will need the following, but since this project is so simple this could be adapted and modified for other hardware, such as Raspberry Pi Zero or Orange Pi.
- DS3231 Real Time Clock module
    - Warning: If you are using a non-rechargeable CR2032 battery, cut the trace above the diode or remove the diode to disable the charging circuit, or the battery may explode.
    - Alternatively, you can use a rechargeable lithium battery which is designed for this circuit, but isn't made clear in the listing.
- Aosong AM2320 I2C temperature and humidity sensor
    - This could easily be substituted for other more accurate sensors.
- YwRobot I2C 16*2 character LCD
    - You can substitute this with other displays that use I2C interface or SPI. This code will exclusively use this display.
- Raspberry Pi 3 or Raspberry Pi 3+
- Class 10 MicroSD card with capacity of at least 16GB
    - This code utilizes segmented audio, so fast access to files is important.
- 5V 2.5A~ USB power supply
    - If you are seeing the yellow lightning bolt on the display, the power supply is too weak and it may cause RPi to crash when the speaker and/or the relay is activated!
- Mini 5V 1W amplifier board
    - A version with variable volume is recommended.
    - If you don't care about the Bluetooth speaker portion or if you are okay with low quality and low volume audio, you can just use the cheap $1 speaker from your local store.
- 2 channel 5V relay module
    - Some modules are active low -- you will need to account for this when wiring this up.
    - If you don't want to have a Bluetooth speaker functionality, you can omit this.
