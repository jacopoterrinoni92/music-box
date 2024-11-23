import st7735

CS = 24
DC = 18
RESET = 22
MOSI = 19
SCK = 23
LED = 15

class Display:
    
    def __init__(
        self, 
        port:int=0, 
        cs=0, 
        dc:int=DC, 
        backlight:int=LED, 
        rst=RESET,
        width=0,
        height=0,
        rotation:int=90,
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
        
        self.display = st7735.ST7735(port=port, cs=cs, dc=dc, backlight=backlight, rst=rst, width=width, height=height, rotation=rotation, spi_speed_hz=spi_speed_hz)
        
        self.width = width
        self.height = height
        
    def initialize(self):
        self.display.begin()
        
    def reset(self):
        self.display.reset()
        
    def display_off(self):
        self.display.display_off()
        
    def display_on(self):
        self.display.display_on()
        
    def sleep(self):
        self.display.sleep()
        
    def wake(self):
        self.display.wake()
        
    @property
    def width(self):
        return self.display.width()

    @property
    def height(self):
        return self.display.height()
        
    def send(self, data, is_data=True, chunk_size=4096):
        """Write a byte or array of bytes to the display. Is_data parameter
        controls if byte should be interpreted as display data (True) or command
        data (False).  Chunk_size is an optional size of bytes to write in a
        single SPI transaction, with a default of 4096.
        """
        self.display.send(data, is_data, chunk_size)
        
    def set_window(self, x0=0, y0=0, x1=None, y1=None):
        """Set the pixel address window for proceeding drawing commands. x0 and
        x1 should define the minimum and maximum x pixel bounds.  y0 and y1
        should define the minimum and maximum y pixel bound.  If no parameters
        are specified the default will be to update the entire display from 0,0
        to width-1,height-1.
        """
        self.display.set_window(x0, y0, x1, y1)

    def display(self, image):
        """Write the provided image to the hardware.

        :param image: Should be RGB format and the same dimensions as the display hardware.

        """
        self.display.display()
        
    