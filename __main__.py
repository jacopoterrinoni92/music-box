from display_sprite import Window, TextSprite, VideoSprite, BarSprite, FadeOutSprite
from rotary import REncoder, RotaryLoader, FEncoder
from mixer import Mixer

import argparse
import logging
import pathlib
import pygame
import time
import sys
import os

GIF_FILE = "/home/pi/8-music-box.gif"
VIDEO_FILE = "/home/pi/in_your_dreams.avi"
MUSIC_FILE = "/home/pi/music/in_your_dreams.mp3"

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

    return clock.tick_busy_loop(fps) #if not pause else 0.0

def music_box_loader(window: Window, sprite_group: pygame.sprite.Group):
    logger.info("Setting up rotary encoder...")
    encoder = FEncoder()

    logger.info("Creating text sprite...")
    text_sprite_1 = TextSprite(text_str='Premi per spegnere', pos_y=150, width=320, height=30, size=16)
    text_sprite_2 = TextSprite(text_str='10', pos_y=180, width=320, height=30, size=16)

    logger.info("Adding sprites to the group...")
    sprite_group.add(text_sprite_1)
    sprite_group.add(text_sprite_2)

    logger.info("Starting the clock...")
    clock = pygame.time.Clock()
    elapsed = 0

    time = 10

    try:
        while not encoder.get_pressed() and time >= 1:
            update_sprite_1(window=window, sprite_group=sprite_group)
            text_sprite_2.update_text(time)
            time -= 1
            elapsed += clock.tick_busy_loop(1)
    except Exception as e:
        logger.error(f"Caught error {e.__class__}, {e}")

    logger.info("Releasing resources...")
    sprite_group.remove(text_sprite_1)
    sprite_group.remove(text_sprite_2)
    encoder.close()

    return encoder.get_shutdown()

def start_music_box(window: Window, sprite_group: pygame.sprite.Group, completed: bool):
    logger.info("Creating the video sprite...")
    video_sprite = VideoSprite()
    video_sprite.load_clip(VIDEO_FILE)
    clip = video_sprite.get_clip()

    #logger.info("Creating the fade out sprite...")
    #fade_out = FadeOutSprite(window=window.get_window())

    logger.debug(f"Duration: {clip.duration}, FPS: {clip.fps}")

    sprite_group.add(video_sprite)
    #sprite_group.add(fade_out)

    logger.info("Setting up the mixer...")
    mixer = Mixer()
    rotary_encoder = REncoder(mixer=mixer)
    mixer.music_load(song_file)
    mixer.music_play()

    logger.info("Setting up the clock...")
    clock = pygame.time.Clock()
    elapsed = 0

    #logger.info(f"Looping for {loaded_time}s")

    try:
        while (elapsed / 1000) <= clip.duration:
            logger.debug(f"Elapsed: {elapsed}")
            video_sprite.set_elapsed(elapsed=elapsed)
            elapsed += update_sprite_2(clock=clock, sprite_group=sprite_group, window=window, fps=clip.fps, pause=rotary_encoder.get_pause())
    except Exception as e:
        logger.error(f"Caught error {e}")

    logger.info("Releasing resources...")
    mixer.mixer_quit()
    rotary_encoder.close()
    video_sprite.close_clip()
    sprite_group.remove(video_sprite)

    shutdown = music_box_loader(window=window, sprite_group=sprite_group)

    '''
    logger.info("Creating the text sprite...")

    text_sprite_1 = TextSprite(text_str='...', size=16)
    sprite_group.add(text_sprite_1)

    update_sprite_1(window=window, sprite_group=sprite_group)

    encoder = FEncoder()
    encoder.wait_press()
    '''

    if shutdown:
        logger.info("Shutting down...")
        return True
        #os.system("sudo shutdown now")
    else:
        return False


if __name__ == "__main__":
    logger.info("Music-box application started")

    pygame.init()

    logger.info("Parsing argument...")
    song_file = pathlib.Path(MUSIC_FILE)

    logger.info("Setting up display...")
    window = Window()

    logger.info("Creating sprite group...")
    sprite_group = pygame.sprite.Group()

    completed = False

    try:
        while True:
            #logger.info("Starting the loader...")
            #loaded_time = music_box_loader(window=window, sprite_group=sprite_group, duration=2.30*60)
            logger.info("Start the music box...")
            if start_music_box(window=window, sprite_group=sprite_group, completed=completed):
                break

    except Exception as e:
        logger.error(f"Caught error {e}")
    finally:
        window.close()
        pygame.quit()
        
        logger.info("Shutting down...")
        os.system("sudo shutdown now")
