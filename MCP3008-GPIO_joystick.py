import uinput
import time
import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

#set up GPIO Pins for up, down, left, right, select, start, a, b, x, y, lt, rt, esc
GPIO.setmode(GPIO.BOARD)
GPIO.setup(35, GPIO.IN, pull_up_down=GPIO.PUD_UP) #up
GPIO.setup(36, GPIO.IN, pull_up_down=GPIO.PUD_UP) #down
GPIO.setup(37, GPIO.IN, pull_up_down=GPIO.PUD_UP) #left
GPIO.setup(38, GPIO.IN, pull_up_down=GPIO.PUD_UP) #right
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_UP) #select
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP) #start
GPIO.setup(29, GPIO.IN, pull_up_down=GPIO.PUD_UP) #a
GPIO.setup(31, GPIO.IN, pull_up_down=GPIO.PUD_UP) #b
GPIO.setup(32, GPIO.IN, pull_up_down=GPIO.PUD_UP) #x
GPIO.setup(33, GPIO.IN, pull_up_down=GPIO.PUD_UP) #y
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP) #lt
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_UP) #rt
GPIO.setup(40, GPIO.IN, pull_up_down=GPIO.PUD_UP) #esc/enter

#set up SPI for analog joystick
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

#set up virtual gamepad buttons
events = (
	uinput.BTN_JOYSTICK, 
	uinput.ABS_X + (0, 255, 0, 0),
	uinput.ABS_Y + (0, 255, 0, 0),
	uinput.BTN_DPAD_UP,
	uinput.BTN_DPAD_DOWN,
	uinput.BTN_DPAD_LEFT,
	uinput.BTN_DPAD_RIGHT,
	uinput.BTN_SELECT,
	uinput.BTN_START,
	uinput.BTN_A,
	uinput.BTN_B,
	uinput.BTN_X,
	uinput.BTN_Y,
	uinput.BTN_TL,
	uinput.BTN_TR,
	uinput.KEY_ESC,
	uinput.KEY_ENTER
	)

device = uinput.Device(events)

# Bools to keep track of button presses
up_button = False
down_button = False
left_button = False
right_button = False
select_button = False
start_button = False
a_button = False
b_button = False
x_button = False
y_button = False
Ltrig = False
Rtrig = False
Esc = False

X_AXIS = 0 #x-axis on MCP3008 connected to CH0
Y_AXIS = 2 #y-axis on MCP3008 connected to CH2

x_max = 700 #empirically determined maximum 10 bit x value
x_mid_high = 435 #empirically determined upper center 10 bit x value
x_mid_low = 365 #empirically determined lower center 10 bit x value
x_min = 100 #empirically determined minimum 10 bit x value
x_read = 400 #start x at center 

y_max = 740 #empirically determined maximum 10 bit y value
y_mid_high = 465 #empirically determined lower center 10 bit y value
y_mid_low = 435 #empirically determined lower center 10 bit y value
y_min = 140 #empirically determined minimum 10 bit y value
y_read = 450 #start y at center

# Center joystick output 
# syn=False to emit an "atomic" (128, 128) event.
x_value = 128 #8 bit center
y_value = 128 #8 bit center
device.emit(uinput.ABS_X, x_value, syn=False)
device.emit(uinput.ABS_Y, y_value)

while True:
	x_read = mcp.read_adc(X_AXIS) #read 10 bit x-axis position
	if x_mid_low <= x_read and x_read <= x_mid_high:	#x_read between x_mid_low and x_mid_high is automatically centered
		x_value = 128 
	if x_read < x_mid_low:	#x_read less than x_mid_low scaled between 0-127:x_min-x_mid_low
		x_value = 255-(x_read-x_min)*127/(x_mid_low-x_min)
	if x_read < x_min:	#x_read below x_min is autmatically minimum
		x_value = 255
	if x_read > x_mid_high:	#x_read greater than x_mid_high scaled between 128-255:x_mid_high-x_max
		x_value = 127-(x_read-x_mid_high)*127/(x_max-x_mid_high)
	if x_read > x_max:	#x_read above x_max is autmatically maximum
		x_value = 0
	device.emit(uinput.ABS_X, x_value) #output 8 bit x

	y_read = mcp.read_adc(Y_AXIS) #read 10 bit y-axis position
	if y_mid_low <= y_read and y_read <= y_mid_high:	#y_read between y_mid_low and y_mid_high is automatically centered
		y_value = 128 
	if y_read < y_mid_low:	#y_read less than y_mid_low scaled between 0-127:y_min-y_mid_low
		y_value = (y_read-y_min)*127/(y_mid_low-y_min)
	if y_read < y_min:	#y_read below y_min is autmatically minimum
		y_value = 0
	if y_read > y_mid_high:	#y_read greater than y_mid_high scaled between 128-255:y_mid_high-y_max
		y_value = 128+(y_read-y_mid_high)*127/(y_max-y_mid_high)
	if y_read > y_max:	#x_read above y_max is autmatically maximum
		y_value = 255
	device.emit(uinput.ABS_Y, y_value) #output 8 bit y

	if (not up_button) and (not GPIO.input(35)): #up button pressed
		up_button = True
		device.emit(uinput.BTN_DPAD_UP, 1)

	if up_button and GPIO.input(35): #up button released
		up_button = False
		device.emit(uinput.BTN_DPAD_UP, 0)

	if (not down_button) and (not GPIO.input(36)): #down button pressed
		down_button = True
		device.emit(uinput.BTN_DPAD_DOWN, 1)

	if down_button and GPIO.input(36): #down button released
		down_button = False
		device.emit(uinput.BTN_DPAD_DOWN, 0)

	if (not left_button) and (not GPIO.input(37)): #left button pressed
		left_button = True
		device.emit(uinput.BTN_DPAD_LEFT, 1)

	if left_button and GPIO.input(37): #left button released
		left_button = False
		device.emit(uinput.BTN_DPAD_LEFT, 0)

	if (not right_button) and (not GPIO.input(38)): #right button pressed
		right_button = True
		device.emit(uinput.BTN_DPAD_RIGHT, 1)

	if right_button and GPIO.input(38): #right button released
		right_button = False
		device.emit(uinput.BTN_DPAD_RIGHT, 0)

	if (not select_button) and (not GPIO.input(11)): #select button pressed
		select_button = True
		device.emit(uinput.BTN_SELECT, 1)

	if select_button and GPIO.input(11): #select button released
		select_button = False
		device.emit(uinput.BTN_SELECT, 0)

	if (not start_button) and (not GPIO.input(12)): #start button pressed
		start_button = True
		device.emit(uinput.BTN_START, 1)

	if start_button and GPIO.input(12): #start button released
		start_button = False
		device.emit(uinput.BTN_START, 0)

	if (not a_button) and (not GPIO.input(29)): #a button pressed
		a_button = True
		device.emit(uinput.BTN_A, 1)

	if a_button and GPIO.input(29): #a button released
		a_button = False
		device.emit(uinput.BTN_A, 0)

	if (not b_button) and (not GPIO.input(31)): #b button pressed
		b_button = True
		device.emit(uinput.BTN_B, 1)

	if b_button and GPIO.input(31): #b button released
		b_button = False
		device.emit(uinput.BTN_B, 0)

	if (not x_button) and (not GPIO.input(32)): #x button pressed
		x_button = True
		device.emit(uinput.BTN_X, 1)

	if x_button and GPIO.input(32): #x button released
		x_button = False
		device.emit(uinput.BTN_X, 0)

	if (not y_button) and (not GPIO.input(33)): #y button pressed
		y_button = True
		device.emit(uinput.BTN_Y, 1)

	if y_button and GPIO.input(33): #y button released
		y_button = False
		device.emit(uinput.BTN_Y, 0)

	if (not Ltrig) and (not GPIO.input(13)): #Left trigger pressed
		Ltrig = True
		device.emit(uinput.BTN_TL, 1)

	if Ltrig and GPIO.input(13): #Left trigger released
		Ltrig = False
		device.emit(uinput.BTN_TL, 0)

	if (not Rtrig) and (not GPIO.input(15)): #Right trigger pressed
		Rtrig = True
		device.emit(uinput.BTN_TR, 1)

	if Rtrig and GPIO.input(15): #Right trigger released
		Rtrig = False
		device.emit(uinput.BTN_TR, 0)

	if (not Esc) and (not GPIO.input(40)): #ESC button pressed
		Esc = True
		device.emit(uinput.KEY_ENTER, 1)
		device.emit(uinput.KEY_ESC, 1)

	if Esc and GPIO.input(40): #ESC button released
		Esc = False
		device.emit(uinput.KEY_ENTER, 0)
		device.emit(uinput.KEY_ESC, 0)

	time.sleep(0.02)
