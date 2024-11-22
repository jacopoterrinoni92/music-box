from rotary import RotaryEncoder
from mixer import Mixer

import argparse
import pathlib
import time
import sys

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

    mixer.music_load(song_file)
    mixer.music_play()
    
    try:
        while True:
            pass
    except KeyboardInterrupt:
        pass
    finally:
        rotary_encoder.clean_channels()