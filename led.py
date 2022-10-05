import board
import digitalio

class Led:
    def __init__(self):
        self.mainLedPin = digitalio.DigitalInOut(board.LED)
        self.mainLedPin.direction = digitalio.Direction.OUTPUT
        self.extraLedPin = None

    def setExtraLed(self, pin):
        self.extraLedPin = pin
        self.extraLedPin.Direction = digitalio.Direction.OUTPUT

    def setLedState(self, state):
        self.mainLedPin.value = not state

        if self.extraLedPin != None:
            self.extraLedPin.value = not state
