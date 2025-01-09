from display_sprite import Window, TextSprite, VideoSprite, BarSprite
from rotary import REncoder, RotaryLoader
from mixer import Mixer

import argparse
import logging
import pathlib
import pygame
import time
import sys

GIF_FILE = "/home/pi/8-music-box.gif"
VIDEO_FILE = "/home/pi/video_320.mp4"
MUSIC_FILE = ""

WIDTH = 320
HEIGHT = 240

logging.basicConfig(format="%(funcName)s:%(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

def update_sprite_1(window: Window, sprite_group: pygame.sprite.Group) -> None:
    logger.debug("Updating the group...")
    
    sprite_group.update()
    sprite_group.draw(window.get_window())
    pygame.display.flip()

def update_sprite_2(window: Window, clock: pygame.time.Clock, sprite_group: pygame.sprite.Group, fps: float, pause = False) -> float:
    logger.debug("Updating the group...")

    sprite_group.update()
    sprite_group.draw(window.get_window())
    pygame.display.flip()

    return clock.tick_busy_loop(fps) if not pause else 0.0

def music_box_loader(window: Window, sprite_group: pygame.sprite.Group, duration:int) -> float:
    logger.info("Setting up rotary encoder...")
    rotary_loader = RotaryLoader()
    
    logger.info("Creating text sprite...")
    text_sprite = TextSprite(text_str='Gira in senso orario per caricare', pos_y=180, width=320, height=30)

    logger.info("Creating bar sprite...")
    bar_sprite = BarSprite(pos_y=210, width=WIDTH, height=30)

    logger.info("Creating video sprite...")
    video_sprite = VideoSprite(width=WIDTH, height=HEIGHT-60)
    video_sprite.load_clip(filename='/home/pi/8-music-box.gif', target_resolution=(WIDTH, HEIGHT-60))
    clip = video_sprite.get_clip()

    logger.info("Adding sprites to the group...")
    sprite_group.add(text_sprite)
    sprite_group.add(bar_sprite)
    sprite_group.add(video_sprite)

    logger.info("Starting the clock...")
    clock = pygame.time.Clock()
    elapsed = 0

    try:
        while not rotary_loader.get_pressed() and rotary_loader.get_loaded_time() <= duration:
            progress = rotary_loader.get_loaded_time() / duration
            logger.debug(f"Progress: {progress}, Duration: {duration}")
            bar_sprite.set_progress(progress=progress)
            video_sprite.set_elapsed(elapsed=elapsed)
            elapsed += update_sprite_2(window=window, clock=clock, sprite_group=sprite_group, fps=clip.fps)
    except Exception as e:
        logger.error(f"Caught error {e.__class__}, {e}")

    logger.info("Loading complete...")

    sprite_group.remove(text_sprite)
    sprite_group.remove(video_sprite)
    sprite_group.remove(bar_sprite)

    logger.info("Sprite group updated...")

    loaded = rotary_loader.get_loaded_time()
    rotary_loader.reset()

    update_sprite_1(window=window, sprite_group=sprite_group)

    logger.info(f"Loaded {loaded}s")

    logger.info("Setting up resources...")
    text_sprite = TextSprite(text_str="Caricamento...", width=WIDTH, height=HEIGHT-100)
    bar_sprite = BarSprite(pos_y=140, width=WIDTH, height=HEIGHT-140)

    sprite_group.add(text_sprite)
    sprite_group.add(bar_sprite)

    clock = pygame.time.Clock()
    elapsed = 0

    while (elapsed / 1000) <= 10:
        bar_sprite.set_progress((elapsed/1000)/10)
        sprite_group.update()
        sprite_group.draw(window.get_window())
        pygame.display.flip()
        elapsed += clock.tick_busy_loop(1)

    sprite_group.remove(text_sprite)
    sprite_group.remove(bar_sprite)

    logger.info("Releasing resources...")
    rotary_loader.close()
    video_sprite.close_clip()

    return loaded

def start_music_box(window: Window, sprite_group: pygame.sprite.Group):
    logger.info("Creating the video sprite...")
    video_sprite = VideoSprite()
    video_sprite.load_clip("/home/pi/video_320.mp4")
    clip = video_sprite.get_clip()

    logger.debug(f"Duration: {clip.duration}, FPS: {clip.fps}")

    sprite_group.add(video_sprite)

    logger.info("Setting up the mixer...")
    mixer = Mixer()
    rotary_encoder = REncoder(mixer=mixer)
    mixer.music_load(song_file)
    mixer.music_play()

    logger.info("Setting up the clock...")
    clock = pygame.time.Clock()
    elapsed = 0

    logger.info(f"Looping for {loaded_time}s")

    try:
        while (elapsed / 1000) <= loaded_time:
            less_than_10 = loaded_time - (elapsed / 1000)

            if less_than_10 <= 10:
                mixer.music_set_volume(-less_than_10)
                
            video_sprite.set_elapsed(elapsed=elapsed)
            elapsed += update_sprite_2(clock=clock, sprite_group=sprite_group, window=window, fps=clip.fps, pause=rotary_encoder.get_pause())
    except Exception as e:
        logger.error(f"Caught error {e}")
    
    logger.info("Releasing resources...")
    mixer.mixer_quit()
    rotary_encoder.close()
    video_sprite.close_clip()
    sprite_group.remove(video_sprite)


if __name__ == "__main__":
    logger.info("Music-box application started")
    
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

    pygame.init()

    logger.info("Parsing argument...")
    song_file = args.file

    logger.info("Setting up display...")
    window = Window()

    logger.info("Creating sprite group...")
    sprite_group = pygame.sprite.Group()

    try:
        while True:
            logger.info("Starting the loader...")
            loaded_time = music_box_loader(window=window, sprite_group=sprite_group, duration=2.30*60)

            logger.info("Start music box...")
            start_music_box(window=window, sprite_group=sprite_group)
    except Exception as e:
        logger.error(f"Caught error {e}")
    finally:
        window.close()
        pygame.quit()
