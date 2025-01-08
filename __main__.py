from display_sprite import Window, TextSprite, VideoSprite, BarSprite
from rotary2 import Rotor, LoadMusicBox
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

def update_sprite_1(sprite_group: pygame.sprite.Group, window: Window):
    logger.debug("Updating the group...")
    sprite_group.update()
    sprite_group.draw(window.get_window())
    pygame.display.flip()

def update_sprite_2(clock: pygame.time.Clock, sprite_group: pygame.sprite.Group, window: Window, video_sprite: VideoSprite, elapsed: float, fps: float, pause = False) -> float:
    logger.debug("Updating the group...")
    logger.debug(f"\t Elapsed time: {elapsed}")
    
    video_sprite.set_elapsed(elapsed)
    sprite_group.update()
    sprite_group.draw(window.get_window())
    pygame.display.flip()
    
    if not pause:
        return clock.tick_busy_loop(fps)
    
    logger.debug("Paused...")
    return 0.0

def music_box_loading(window: Window, load_music_box: LoadMusicBox, sprite_group: pygame.sprite.Group) -> float:
    logger.info("Creating text sprite...")
    text_sprite = TextSprite(text_str='Turn the knob to load...', pos_x=0, pos_y=180, width=320, height=30)
    
    logger.info("Creating bar sprite...")
    bar_sprite = BarSprite(pos_x=0, pos_y=210, width=WIDTH, height=30)
    
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
    duration = 2.30*60

    try:
        while not load_music_box.get_pressed() and load_music_box.get_loaded_time() <= duration:
            progress = load_music_box.get_loaded_time() / duration
            logger.debug(f"Progress: {progress}, Duration: {duration}")
            bar_sprite.set_progress(load_music_box.get_loaded_time() / duration)
            elapsed += update_sprite_2(clock, sprite_group, window, video_sprite, elapsed, clip.fps)
    except:
        pass

    sprite_group.remove(text_sprite)
    sprite_group.remove(video_sprite)
    sprite_group.remove(bar_sprite)
    
    update_sprite_1(sprite_group, window)
    
    #text_sprite = TextSprite(text_str=f"Loaded {load_music_box.get_loaded_time()}") 
    #sprite_group.add(text_sprite)
    
    #update_sprite_1(sprite_group, window)

    logger.info(f"Loaded {load_music_box.get_loaded_time()}s")

    #time.sleep(10)

    sprite_group.remove(text_sprite)
    sprite_group.remove(video_sprite)

    logger.info("Releasing resources...")
    load_music_box.close()
    video_sprite.close_clip()
    
    return load_music_box.get_loaded_time()

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

    logger.info("Setting up rotary encoder...")
    load_music_box = LoadMusicBox()

    logger.info("Creating sprite group...")
    sprite_group = pygame.sprite.Group()

    logger.info("Waiting for input...")
    loaded_time = music_box_loading(window, load_music_box, sprite_group)

    logger.info("Setting up resources...")
    text_sprite = TextSprite(text_str="Caricamento...", width=WIDTH, height=HEIGHT-100)
    bar_sprite = BarSprite(pos_x=0, pos_y=140, width=WIDTH, height=100)

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

    logger.info("Creating the video sprite...")
    video_sprite = VideoSprite()
    video_sprite.load_clip("/home/pi/video_320.mp4")
    clip = video_sprite.get_clip()

    logger.debug(f"Duration: {clip.duration}, FPS: {clip.fps}")

    sprite_group.add(video_sprite)

    logger.info("Setting up the mixer...")
    mixer = Mixer()
    rotary_encoder = Rotor(mixer=mixer)
    mixer.music_load(song_file)
    mixer.music_play()

    logger.info("Setting up the clock...")
    clock = pygame.time.Clock()
    elapsed = 0
    faded_out = False

    logger.info(f"Looping for {loaded_time}s")

    try:
        while (elapsed / 1000) <= loaded_time:
            less_than_10 = loaded_time - (elapsed / 1000)
            if less_than_10 <= 10 and not faded_out:
                logger.info(f"Fading out at: {elapsed}")
                mixer.mixer_fadeout()
                faded_out = True
            elapsed += update_sprite_2(clock, sprite_group, window, video_sprite, elapsed, clip.fps, rotary_encoder.get_pause())
    except Exception as e:
        logger.error(f"Caught error {e}")
    finally:
        logger.info("Releasing resources...")
        mixer.mixer_quit()
        rotary_encoder.close()
        video_sprite.close_clip()
        sprite_group.remove(video_sprite)
        window.close()
        pygame.quit()
