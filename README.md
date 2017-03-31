Parts list:
Case - printed from Rasmushauschild's 3d models on my Prusa Mk2
Button covers (Dpad, ABXY, Start, Select, Menu, Underside Buttons) - printed from Rasmushauschild's 3d models on my Prusa Mk2
Buttons - CO-RODE Tact Button Switch 6x6x5mm Pack of 100 - https://www.amazon.com/gp/product/B00W0YUV1W 
Joystick - PSP 1000 Joystick Analog Stick Assembly Replacement - https://www.amazon.com/gp/product/B00170JDZU 
Display - BW 3.5 Inch TFT LCD Monitor for Car / Automobile - https://www.amazon.com/gp/product/B0045IIZKU 
Speakers - Ringer Speaker (Set of 2) for Nintendo DS Lite - https://www.amazon.com/gp/product/B0071AF9F8 
Circuit Board - PIXNOR 7*9 cm Solder Finished Prototype PCB for DIY Circuit Board Breadboard Pack of 10 https://www.amazon.com/gp/product/B01DKAC7BG 
Audio Amplifier - ADAFRUIT MONO 2.5W CLASS D AUDIO AMPLIFIER - PAM8302 - https://www.adafruit.com/product/2130 
Thumbwheel Potentiometer - 10K Ohm Thumbwheel Potentiometer Pack of 5 - http://www.ebay.com/itm/381143599904 
Battery - Lithium Ion Polymer Battery - 3.7v 2500mAh - https://www.adafruit.com/products/328 
Power Supply - PowerBoost 1000 Charger - Rechargeable 5V Lipo USB Boost @ 1A - 1000C - https://www.adafruit.com/products/2465 
Power Button - Rugged Metal On/Off Switch with White LED Ring - 16mm White On/Off - https://www.adafruit.com/products/917 
Jumper Wires - Premium Female/Female Jumper Wires - 40 x 6" - https://www.adafruit.com/products/266 
A/D Converter - MCP3008 - 8-Channel 10-Bit ADC With SPI Interface - https://www.adafruit.com/products/856 or http://www.ebay.com/itm/111254096078 
Raspberry Pi 3 Model B 2016 Single Board Computer with High Performance Heatsink Set - https://www.amazon.com/gp/product/B01CMC50S0
SD Card - ADATA Premier 16GB microSDHC/SDXC UHS-I U1 Memory Card with Adapter (AUSDH16GUICL10-RA1) - https://www.amazon.com/gp/product/B00BSRETVK

Wiring Instructions

Digital Controls
Wire Buttons (Dpad, X, Y, A, B, Start, Select, Menu, L Shoulder, R Shoulder) to GPIO Input Pins (& GND GPIO Pin)  (GPIO pins identified in driver file)

Power
Wire PowerBoost 1000 C output to 5V & GND GPIO Pins (pins 2, 6)
Wire Power Button Contacts so that EN & GND Pins on PowerBoost 1000 C are shorted when button is not pressed and open when button is pressed (contacts C1 & NC1 (2,4) on button)
Connect Battery JST to PowerBoost 1000 C battery JST 

Sound
Position thumbwheel so it passes through slot on left side of case, used to control speaker volume
Wire pin 1 of thumbwheel to GND GPIO Pin on RPi
Wire pin 3 of thumbwheel to pads X, Y on bottom of RPi (note - converts headphone jack to mono audio)
Wire pin 2 of thumbwheel to audio+ input of PAM8302  
Wire PAM8302 ground to pad Z on bottom of RPi
Wire PAM8302 power to 3.3V GPIO Pin on RPi (pin 1)
Wire PAM8302 audio- input to PAM8302 ground 
Turn PAM8302 amplifier to maximum
Wire Output of PAM8302 to speakers

Video
On Display circuit board, remove power converter chip
Wire 5V pin from power converter chip spot on display circuit board to 5V GPIO Pin on RPi (pin 4)
Wire yellow wire from Display to pad X on bottom of Raspberry Pi
Wire black (ground) wire from Display to pad X on bottom of Raspberry Pi

Joystick
Wire pins 16-9 of MCP3008 (VDD, VREF, AGND, CLK, DOUT, DIN, CS/SHDN, DGND) to SPI GPIO Pins on RPi (pins 17, 19, 21, 23, 25, 26) (see https://learn.adafruit.com/raspberry-pi-analog-to-digital-converters/mcp3008)
Wire Joystick +V to 3.3 V GPIO Pin on RPi (or VDD/VREF Pins 16/15 on MCP3008)
Wire Joystick ground to GND GPIO Pin on RPi
Wire Joystick x-axis to CH0 of MCP3008 (Pin 1)
Wire Joystick y-axis to CH2 of MCP3008 (Pin 3)

Software 
RetroPie - https://retropie.org.uk/

Driver for Buttons and Joystick (Python)

Install Adafruit MCP3008 Python Library
https://learn.adafruit.com/raspberry-pi-analog-to-digital-converters/mcp3008

Make sure uinput is installed
sudo apt-get install uinput

Driver Program Source Code
MCP3008-GPIO_joystick.py

Run Driver Program on Startup
edit /etc/rc.local to add:
python MCP3008-GPIO_joystick.py

Links I found useful during driver programming
https://github.com/tuomasjjrasanen/python-uinput/blob/master/examples/joystick.py
https://github.com/cpswan/Python/blob/master/rpi-gpio-jstk.py
http://blog.thestateofme.com/2012/08/10/raspberry-pi-gpio-joystick/
http://www.hertaville.com/interfacing-an-spi-adc-mcp3008-chip-to-the-raspberry-pi-using-c.html

Special thanks to the efforts of Rasmushauschild, Adafruit, Chris Swan, hertaville.com
