from gpiozero import RotaryEncoder, Button

from mixer import Mixer

import logging

logger = logging.getLogger(__name__)

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


class RotaryLoader:

    def __init__(self):
        self.init_gpio()
        self.loaded_time = 0
        self.pressed = False

    def init_gpio(self) -> None:
        self.button = Button(SW_PIN)
        self.r_loader = RotaryEncoder(CLK_PIN, DT_PIN)

        self.button.when_pressed = self.button_pressed
        self.r_loader.when_rotated_clockwise = self.load

    def load(self, object) -> None:
        self.loaded_time += 5

    def button_pressed(self, object) -> None:
        self.pressed = True

    def get_loaded_time(self) -> int:
        return self.loaded_time

    def get_pressed(self) -> bool:
        return self.pressed

    def reset(self) -> None:
        self.pressed = False
        self.loaded_time = 0

    def close(self) -> None:
        self.rotor.close()
        self.button.close()


class REncoder:

    def __init__(self, mixer: Mixer):
        self.init_gpio()
        self.mixer = mixer
        self.pause = False

    def init_gpio(self) -> None:
        self.button = Button(SW_PIN)
        self.rotary_encoder = RotaryEncoder(CLK_PIN, DT_PIN)
        
        self.button.when_pressed = self.button_pressed
        self.rotary_encoder.when_rotated_clockwise = self.increase_volume
        self.rotary_encoder.when_rotated_counter_clockwise = self.decrease_volume

    def increase_volume(self, object) -> None:
        self.mixer.music_set_volume(value=1)

    def decrease_volume(self, object) -> None:
        self.mixer.music_set_volume(value=-1)

    def button_pressed(self, object) -> None:
        if self.pause:   
            self.pause = False
            self.mixer.music_unpause()
        else:
            self.pause = True
            self.mixer.music_pause()

    def get_pause(self) -> bool:
        return self.pause

    def close(self) -> None:
        self.button.close()
        self.rotary_encoder.close()
