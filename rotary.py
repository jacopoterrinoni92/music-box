import time
import RPi.GPIO as GPIO

from mixer import Mixer

"""
CLK (output A) is the primary output pulse used to determine the amount of rotation. 
Each time the knob is turned in either direction by just one detent (click), 
the ‘CLK’ output goes through one cycle of going HIGH and then LOW.
"""
CLK_PIN = 17

"""
DT (Output B) is similar to CLK output, 
but it lags behind CLK by a 90° phase shift. 
This output is used to determine the direction of rotation.
"""
DT_PIN = 23

"""
SW is the output of the push button switch (active low). 
When the knob is depressed, the voltage goes LOW.
"""
SW_PIN = 27

DIRECTION_CW = 0
DIRECTION_CCW = 1

class RotaryEncoder:

    def __init__(self, mixer):
        self.init_gpio()

        self.mixer = mixer

        self.value = 0
        self.direction = DIRECTION_CW

        self.state = '00'

        self.callback = None

        self.button_pressed = False
        self.prev_button_state = GPIO.HIGH

    def init_gpio(self) -> None:
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(CLK_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(DT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(SW_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(CLK_PIN, GPIO.BOTH, callback=self.rotary_callback)  
        GPIO.add_event_detect(DT_PIN, GPIO.BOTH, callback=self.rotary_callback)

        GPIO.add_event_detect(SW_PIN, GPIO.FALLING, callback=self.button_pressed)

    def button_pressed(self, channel):
        if GPIO.input(SW_PIN) == GPIO.LOW:
            if self.mixer.pause:
                self.mixer.music_unpause()
            else:
                self.mixer.music_pause()
        time.sleep(0.1)

    def rotary_callback(self, channel):
        current_clk_state = GPIO.input(CLK_PIN)
        current_dt_state = GPIO.input(DT_PIN)
        newState = "{}{}".format(current_clk_state, current_dt_state)

        if self.state == "00": # Resting position
            if newState == "01": # Turned right 1
                self.direction = DIRECTION_CW
            elif newState == "10": # Turned left 1
                self.direction = DIRECTION_CCW
        elif self.state == "01": # R1 or L3 position
            if newState == "11": # Turned right 1
                self.direction = DIRECTION_CW
            elif newState == "00": # Turned left 1
                if self.direction == DIRECTION_CCW:
                    self.value = self.value - 1
                    self.mixer.music_set_volume(value=-5)
                    if self.callback is not None:
                        self.callback(self.value, self.direction)
        elif self.state == "10": # R3 or L1
            if newState == "11": # Turned left 1
                self.direction = DIRECTION_CCW
            elif newState == "00": # Turned right 1
                if self.direction == DIRECTION_CW:
                    self.value = self.value + 1
                    self.mixer.music_set_volume(value=5)
                    if self.callback is not None:
                        self.callback(self.value, self.direction)
        else: # self.state == "11"
            if newState == "01": # Turned left 1
                self.direction = DIRECTION_CCW
            elif newState == "10": # Turned right 1
                self.direction = DIRECTION_CW
            elif newState == "00": # Skipped an intermediate 01 or 10 state, but if we know direction then a turn is complete
                if self.direction == DIRECTION_CCW:
                    self.value = self.value - 1
                    self.mixer.music_set_volume(value=-5)
                    if self.callback is not None:
                        self.callback(self.value, self.direction)
                elif self.direction == DIRECTION_CW:
                    self.value = self.value + 1
                    self.mixer.music_set_volume(value=5)
                    if self.callback is not None:
                        self.callback(self.value, self.direction)
        
        self.state = newState
        
        

    def clean_channels(self):
        GPIO.cleanup()

    def get_value(self):
        return self.value