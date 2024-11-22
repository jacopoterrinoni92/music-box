import time
import RPi.GPIO as GPIO

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

    def __init__(self):
        init_gpio()

        self.counter = 0
        self.direction = DIRECTION_CW
        self.clk_state = 0
        self.dt_state = 0
        self.prev_clk_state = GPIO.input(CLK_PIN)
        self.prev_dt_state = GPIO.input(DT_PIN)
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
        print("Channel: %s, CLK_PIN: %s, DT_PIN: %s", channel, GPIO.input(SW_PIN))
        if GPIO.input(SW_PIN) == GPIO.LOW:
            print("Button pressed")
        time.sleep(0.1)

    def rotary_callback(self, channel):
        print("Channel: %s, CLK_PIN: %s, DT_PIN: %s", channel, GPIO.input(CLK_PIN), GPIO.input(DT_PIN))