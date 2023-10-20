import board
import digitalio

class Led:
    def __init__(self):
        self.mainLedPin = digitalio.DigitalInOut(board.LED)
        self.mainLedPin.direction = digitalio.Direction.OUTPUT
        self.extraLedPin = None
        self.rgbLed = None

    def setExtraLed(self, pin):
        self.extraLedPin = digitalio.DigitalInOut(pin)
        self.extraLedPin.direction = digitalio.Direction.OUTPUT

    def setLedState(self, state):
        self.mainLedPin.value = state

        if self.extraLedPin != None:
            self.extraLedPin.value = state
