import board
import digitalio

from adafruit_rgb_display import st7735

CS = digitalio.DigitalInOut(board.D8)
DC = digitalio.DigitalInOut(board.D18)
RESET = digitalio.DigitalInOut(board.D22)
MOSI = digitalio.DigitalInOut(board.D19)
SCK = digitalio.DigitalInOut(board.D23)
LED = digitalio.DigitalInOut(board.D15)

class Display:
    
    def __init__(
        self, 
        port:int=0, 
        cs=CS, 
        dc:int=DC, 
        backlight:int=LED, 
        rst=RESET,
        width=160,
        height=128,
        rotation:int=0,
        offset_left=None,
        offset_top=None,
        invert=True,
        bgr=True, 
        spi_speed_hz=4000000):
        """Create an instance of the display using SPI communication.

        Must provide the GPIO pin label for the D/C pin and the SPI driver.

        Can optionally provide the GPIO pin label for the reset pin as the rst parameter.

        :param port: SPI port number
        :param cs: SPI chip-select number (0 or 1 for BCM
        :param backlight: Pin for controlling backlight
        :param rst: Reset pin for ST7735
        :param width: Width of display connected to ST7735
        :param height: Height of display connected to ST7735
        :param rotation: Rotation of display connected to ST7735
        :param offset_left: COL offset in ST7735 memory
        :param offset_top: ROW offset in ST7735 memory
        :param invert: Invert display
        :param spi_speed_hz: SPI speed (in Hz)

        """
        self.disp = st7735.ST7735(board.SPI(), cs=cs, dc=dc, rst=rst, width=width, height=height, rotation=rotation, baudrate=spi_speed_hz)
        self.backlight = LED
        self.backlight.switch_to_output()
        
    def turn_on_backlight(self):
        self.backlight.value = True
        
    def turn_off_backlight(self):
        self.backlight.value = False
        
    def reset(self):
        self.disp.reset()
                
    @property
    def width(self):
        return self.disp.width()

    @property
    def height(self):
        return self.disp.height()
        
    
