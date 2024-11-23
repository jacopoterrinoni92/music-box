from rotary import RotaryEncoder
from animation import Display
from mixer import Mixer

from PIL import Image, ImageDraw, ImageFont

import argparse
import pathlib
import time
import sys

def draw_image() -> Image:
    img = Image.new("RGB", (WIDTH, HEIGHT), color=(255, 0, 0))

    draw = ImageDraw.Draw(img)
    
    # Draw a purple rectangle with yellow outline.
    draw.rectangle((10, 10, WIDTH - 10, HEIGHT - 10), outline=(255, 255, 0), fill=(255, 0, 255))

    # Draw some shapes.
    # Draw a blue ellipse with a green outline.
    draw.ellipse((10, 10, WIDTH - 10, HEIGHT - 10), outline=(0, 255, 0), fill=(0, 0, 255))

    # Draw a white X.
    draw.line((10, 10, WIDTH - 10, HEIGHT - 10), fill=(255, 255, 255))
    draw.line((10, HEIGHT - 10, WIDTH - 10, 10), fill=(255, 255, 255))

    # Draw a cyan triangle with a black outline.
    draw.polygon([(WIDTH / 2, 10), (WIDTH - 10, HEIGHT - 10), (10, HEIGHT - 10)], outline=(0, 0, 0), fill=(0, 255, 255))

    # Load default font.
    font = ImageFont.load_default()

    # Alternatively load a TTF font.
    # Some other nice fonts to try: http://www.dafont.com/bitmap.php
    # font = ImageFont.truetype("Minecraftia.ttf", 16)
    
    return img

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
    rotary_encoder = RotaryEncoder(mixer=mixer)
    display = Display()

    mixer.music_load(song_file)
    mixer.music_play()
    
    img = draw_image()
    
    try:
        while True:
            display.display(img)
    except KeyboardInterrupt:
        pass
    finally:
        rotary_encoder.clean_channels()
        display.display_off()