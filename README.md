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
- WS2812 "Neopixel" board (4 LEDs)
    - If you don't care about the lighting, you can omit this.
    - You can use as many or as few as you want, from none to 8. But keep the current consumption in mind!
- A pair of 1 kilohm resistors
    - This is used just in case the configuration of the relay board is incorrect and it pulls too much current from the Raspberry Pi board.
    - It's a good idea to include one on the input and output pins to safeguard against overcurrent.
- Bunch of hook-up wires
    - Generic search term to use is "Arduino jumper wire". It's sometimes referred to as "Dupont wire"
- Some tinned solid-core wires
    - 30AWG and 25AWG wires are the common ones and this is pretty useful on soldering components on Veroboard / Perfboard.
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
- All of the Python code in the `src` directory
    - Refer to installation guide to set it up.
