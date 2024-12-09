from rotary import RotaryEncoder
from window import Window
from mixer import Mixer

#from PIL import Image, ImageDraw, ImageFont

import subprocess
import argparse
import pathlib
import time
import sys
import os

WIDTH = 128
HEIGHT = 160
'''
def draw_image() -> Image:
    img = Image.new("RGB", (WIDTH, HEIGHT))

    draw = ImageDraw.Draw(img)
        
    padding = -2
    x = 0
    
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
    
    draw.rectangle((0, 0, WIDTH, HEIGHT), outline=0, fill=0)
    
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

    #time.sleep(0.1)
    return img
    '''

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Music-box CLI")

    parser.add_argument(
        "file",
        type=pathlib.Path,
        help=("Path of the song to play")
    )

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()

    args = parser.parse_args()

    song_file = args.file

    mixer = Mixer()
    #rotary_encoder = RotaryEncoder(mixer=mixer)
    mixer.music_load(song_file)
    mixer.music_play()
    
    window = Window()

    try:
        while mixer.music_get_busy():
            pass
    except KeyboardInterrupt:
        pass
    finally:
        window.close()
        #rotary_encoder.clean_channels()