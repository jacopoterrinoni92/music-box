import board
import busio
import digitalio

from adafruit_rgb_display import st7735


class Display:

    def __init__(
        self,
        cs=board.CE0,
        dc=board.D25, 
        backlight=board.D22, 
        rst=board.D24,
        width=160,
        height=128,
        rotation:int=90,
        offset_left=None,
        offset_top=None,
        invert=True,
        bgr=True, 
        spi_speed_hz=2400000):
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
        self.cs = digitalio.DigitalInOut(cs)
        self.dc = digitalio.DigitalInOut(dc)
        self.rst = digitalio.DigitalInOut(rst)
        self.rst.switch_to_output()

        self.mosi = board.MOSI
        self.sck = board.SCK
        self.spi = board.SPI()
        self.disp = st7735.ST7735(self.spi, cs=self.cs, dc=self.dc, rst=self.rst, width=width, height=height, rotation=rotation, baudrate=spi_speed_hz)

        self.led = digitalio.DigitalInOut(backlight)
        self.led.switch_to_output()
        
        self.w = width
        self.h = height
        self.rot = rotation

    def turn_on_backlight(self):
        self.led.value = True

    def turn_off_backlight(self):
        self.led.value = False

    def reset(self):
        self.disp.reset()

    def clean_resources(self):
        self.spi.deinit()
        self.cs.deinit()
        self.dc.deinit()
        self.rst.deinit()
        self.led.deinit()

    @property
    def width(self):
        return self.w

    @property
    def height(self):
        return self.h
    
    def rotation(self):
        return self.rot

    def get_display(self):
        return self.disp

    def display_image(self, image):
        self.disp.image(img=image)
