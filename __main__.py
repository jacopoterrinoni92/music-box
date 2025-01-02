from rotary2 import Rotor
from moviepy_video import VideoSprite
from mixer import Mixer

import subprocess
import argparse
import pathlib
import pygame
import time
import sys
import os

WIDTH = 320
HEIGHT = 240
DARK_BLUE = (   3,   5,  54)

def load_time():


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

    window_sprite = VideoSprite(pygame.Rect( 0, 0, 320, 240 ), "/home/pi/video_320.mp4")
    clock = pygame.time.Clock()
    sprite_group = pygame.sprite.Group()
    sprite_group.add( window_sprite )
    window = window_sprite.get_window()

    mixer = Mixer()
    rotary_encoder = Rotor(mixer=mixer)
    mixer.music_load(song_file)
    mixer.music_play()

    try:
        while mixer.music_get_busy():
            sprite_group.update()
            window.fill( DARK_BLUE )
            sprite_group.draw( window )
            pygame.display.flip()
            clock.tick_busy_loop(30)
    except KeyboardInterrupt:
        pass
    finally:
        window_sprite.close()
        rotary_encoder.close()
