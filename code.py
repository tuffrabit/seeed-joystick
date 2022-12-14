import board
import digitalio
import analogio
import usb_hid

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from hid_gamepad import Gamepad
from stickDeadzone import StickDeadzone
from stick import Stick
from led import Led
from startup import Startup
from kbMode import KbMode

# Key Bindings
BUTTON_JOYSTICK_1_KEY = 1
KEYBOARD_MODE_STICK_UP_KEY = Keycode.W
KEYBOARD_MODE_STICK_DOWN_KEY = Keycode.S
KEYBOARD_MODE_STICK_LEFT_KEY = Keycode.A
KEYBOARD_MODE_STICK_RIGHT_KEY = Keycode.D

# Configurable Values
KEYBOARD_MODE_X_START_OFFSET = 10
KEYBOARD_MODE_Y_START_OFFSET = 10

# Globals
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)
gp = Gamepad(usb_hid.devices)
stickDeadzone = StickDeadzone()
stick = Stick()
led = Led()
kbMode = KbMode()
startup = Startup()
deadzone = 0
isKeyboardMode = False

#Setup
kbMode.setXStartOffset(KEYBOARD_MODE_X_START_OFFSET)
kbMode.setYStartOffset(KEYBOARD_MODE_Y_START_OFFSET)
kbMode.setKeyboard(keyboard)
startup.setLed(led)

# Create some buttons. The physical buttons are connected
# to ground on one side and these and these pins on the other.
#buttonPins = (board.GP22)
button = digitalio.DigitalInOut(board.D2)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

#buttons = [digitalio.DigitalInOut(pin) for pin in buttonPins]
#for button in buttons:
#    button.direction = digitalio.Direction.INPUT
#    button.pull = digitalio.Pull.UP

# Connect an analog two-axis joystick to A4 and A5.
ax = analogio.AnalogIn(board.A0)
ay = analogio.AnalogIn(board.A1)

# Handle deadzone calc
led.setLedState(True)
stickDeadzone.initDeadzone(ax, ay)
deadzone = stickDeadzone.getDeadzone()
stick.setDeadzone(stickDeadzone)
led.setLedState(False)

# Handle startup flags
isKeyboardMode = startup.detectStartupFlags(button)

#print("Deadzone: " + str(deadzone))
#print("Upper Bound: " + str(stickDeadzone.getUpperBoundary()))
#print("Lower Bound: " + str(stickDeadzone.getLowerBoundary()))

while True:
    if button.value:
        gp.release_buttons(BUTTON_JOYSTICK_1_KEY)
        #print(" release", gamepadButtonNum, end="")
    else:
        gp.press_buttons(BUTTON_JOYSTICK_1_KEY)
        #print(" press", gamepadButtonNum, end="")

    stickValues = stick.doStickCalculations(ax, ay, True)

    if isKeyboardMode:
        pressedValues = kbMode.calculateStickInput(stickValues)
        kbMode.handleKeyboundModeKey(KEYBOARD_MODE_STICK_UP_KEY, pressedValues[0])
        kbMode.handleKeyboundModeKey(KEYBOARD_MODE_STICK_DOWN_KEY, pressedValues[1])
        kbMode.handleKeyboundModeKey(KEYBOARD_MODE_STICK_LEFT_KEY, pressedValues[2])
        kbMode.handleKeyboundModeKey(KEYBOARD_MODE_STICK_RIGHT_KEY, pressedValues[3])
    else:
        #print(stickValues)
        gp.move_joysticks(x=stickValues[0], y=stickValues[1])
