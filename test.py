# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This will show some Linux Statistics on the attached display. Be sure to adjust
to the display you have connected. Be sure to check the learn guides for more
usage information.

This example is for use on (Linux) computers that are using CPython with
Adafruit Blinka to support CircuitPython libraries. CircuitPython does
not support PIL/pillow (python imaging library)!
"""

import time
import subprocess
import digitalio
import board
import busio
from gpiod.line import Direction, Value
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import ili9341
from adafruit_rgb_display import st7789  # pylint: disable=unused-import
from adafruit_rgb_display import hx8357  # pylint: disable=unused-import
import st7735  # pylint: disable=unused-import
from adafruit_rgb_display import ssd1351  # pylint: disable=unused-import
from adafruit_rgb_display import ssd1331  # pylint: disable=unused-import

# Configuration for CS and DC pins (these are PiTFT defaults):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D24)

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 24000000

# Setup SPI bus using hardware SPI:
spi = busio.SPI(board.SCLK)

# pylint: disable=line-too-long
# Create the display:
# disp = st7789.ST7789(spi, rotation=90,                            # 2.0" ST7789
# disp = st7789.ST7789(spi, height=240, y_offset=80, rotation=180,  # 1.3", 1.54" ST7789
# disp = st7789.ST7789(spi, rotation=90, width=135, height=240, x_offset=53, y_offset=40, # 1.14" ST7789
# disp = st7789.ST7789(spi, rotation=90, width=172, height=320, x_offset=34, # 1.47" ST7789
# disp = st7789.ST7789(spi, rotation=270, width=170, height=320, x_offset=35, # 1.9" ST7789
# disp = hx8357.HX8357(spi, rotation=180,                           # 3.5" HX8357
# disp = st7735.ST7735R(spi, rotation=90,                           # 1.8" ST7735R
# disp = st7735.ST7735R(spi, rotation=270, height=128, x_offset=2, y_offset=3,   # 1.44" ST7735R
# disp = st7735.ST7735R(spi, rotation=90, bgr=True, width=80,       # 0.96" MiniTFT Rev A ST7735R
# disp = st7735.ST7735R(spi, rotation=90, invert=True, width=80,    # 0.96" MiniTFT Rev B ST7735R
# x_offset=26, y_offset=1,
# disp = ssd1351.SSD1351(spi, rotation=180,                         # 1.5" SSD1351
# disp = ssd1351.SSD1351(spi, height=96, y_offset=32, rotation=180, # 1.27" SSD1351
# disp = ssd1331.SSD1331(spi, rotation=180,                         # 0.96" SSD1331
disp = st7735.ST7735(
    port=0,
    rotation=90,  # 2.2", 2.4", 2.8", 3.2" ILI9341
    cs=st7735.BG_SPI_CS_FRONT,
    dc="GPIO25",
    rst="GPIO24",
    backlight="GPIO22",
    spi_speed_hz=4000000,
)
# pylint: enable=line-too-long
disp.reset()
disp.display_on()
#disp.set_backlight(Value.INACTIVE)
# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = 160  
width = 128

image = Image.new("RGB", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(255, 255, 255))
disp.display(image)

# First define some constants to allow easy positioning of text.
padding = -2
x = 0

# Load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
try:
    while True:
        # Draw a black filled box to clear the image.
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        
                # Draw a purple rectangle with yellow outline.
        draw.rectangle((10, 10, width - 10, height - 10), outline=(255, 255, 0), fill=(255, 0, 255))

        # Draw some shapes.
        # Draw a blue ellipse with a green outline.
        draw.ellipse((10, 10, width - 10, height - 10), outline=(0, 255, 0), fill=(0, 0, 255))

        # Draw a white X.
        draw.line((10, 10, width - 10, height - 10), fill=(255, 255, 255))
        draw.line((10, height - 10, width - 10, 10), fill=(255, 255, 255))

        # Draw a cyan triangle with a black outline.
        draw.polygon([(width / 2, 10), (width - 10, height - 10), (10, height - 10)], outline=(0, 0, 0), fill=(0, 255, 255))

        # Shell scripts for system monitoring from here:
        # https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
        cmd = "hostname -I | cut -d' ' -f1"
        IP = "IP: " + subprocess.check_output(cmd, shell=True).decode("utf-8")
        cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
        CPU = subprocess.check_output(cmd, shell=True).decode("utf-8")
        cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%s MB  %.2f%%\", $3,$2,$3*100/$2 }'"
        MemUsage = subprocess.check_output(cmd, shell=True).decode("utf-8")
        cmd = 'df -h | awk \'$NF=="/"{printf "Disk: %d/%d GB  %s", $3,$2,$5}\''
        Disk = subprocess.check_output(cmd, shell=True).decode("utf-8")
        cmd = "cat /sys/class/thermal/thermal_zone0/temp |  awk '{printf \"CPU Temp: %.1f C\", $(NF-0) / 1000}'"  # pylint: disable=line-too-long
        Temp = subprocess.check_output(cmd, shell=True).decode("utf-8")
        
        print(f"${IP} ${CPU} ${MemUsage} ${Disk} ${Temp}")

        # Write four lines of text.
        y = padding
        draw.text((x, y), IP, font=font, fill="#FFFFFF")
        y += font.getbbox(IP)[1]
        draw.text((x, y), CPU, font=font, fill="#FFFF00")
        y += font.getbbox(CPU)[1]
        draw.text((x, y), MemUsage, font=font, fill="#00FF00")
        y += font.getbbox(MemUsage)[1]
        draw.text((x, y), Disk, font=font, fill="#0000FF")
        y += font.getbbox(Disk)[1]
        draw.text((x, y), Temp, font=font, fill="#FF00FF")

        # Display image.
        disp.display(image)
        time.sleep(60)
except KeyboardInterrupt:
    pass
finally:
    disp.reset()