from gpiozero import RotaryEncoder, Button

from mixer import Mixer

"""
CLK (output A) is the primary output pulse used to determine the amount of rotation.
Each time the knob is turned in either direction by just one detent (click),
the ‘CLK’ output goes through one cycle of going HIGH and then LOW.
"""
CLK_PIN = 16

"""
DT (Output B) is similar to CLK output,
but it lags behind CLK by a 90° phase shift.
This output is used to determine the direction of rotation.
"""
DT_PIN = 5

"""
SW is the output of the push button switch (active low).
When the knob is depressed, the voltage goes LOW.
"""
SW_PIN = 27


class Rotor:

    def __init__(self, mixer):
        self.init_gpio()
        self.mixer = mixer

    def init_gpio(self) -> None:
        self.rotor = RotaryEncoder(CLK_PIN, DT_PIN)
        self.button = Button(SW_PIN)
        self.rotor.when_rotated_clockwise = self.increase_volume
        self.rotor.when_rotated_counter_clockwise = self.decrease_volume
        self.button.when_pressed = self.button_pressed

    def increase_volume(self, object):
        self.mixer.music_set_volume(value=1)

    def decrease_volume(self, object):
        self.mixer.music_set_volume(value=-1)

    def button_pressed(self, object):
        print("Button pressed")

    def close(self):
        self.rotor.close()
        self.button.close()
