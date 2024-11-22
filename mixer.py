import pygame
import pathlib

class Mixer:
    """ This class is used to manage pygame.Mixer"""

    def __init__(
        self, 
        frequency: int = 44100, 
        size: float = -16, 
        channels: int = 2, 
        buffer: int = 512, 
        devicename: str = None, 
        allowedchanges=pygame.AUDIO_ALLOW_FREQUENCY_CHANGE | pygame.AUDIO_ALLOW_CHANNELS_CHANGE,
        volume: int = 0.5
    ):

        self.frequency = frequency
        self.size = size
        self.channels = channels
        self.buffer = buffer
        self.devicename = devicename
        self.allowedchanges = allowedchanges

        self.mixer = pygame.mixer.pre_init(frequency, size, channels, buffer, devicename, allowedchanges)
        self.mixer = pygame.mixer.init()

        self.sound = None
        self.volume = volume

        self.pause = False

    """
    This will uninitialize pygame.mixerpygame module for loading and playing sounds. 
    All playback will stop and any loaded Sound objects may not be compatible with the mixer if it is reinitialized later.
    """
    def quit(self) -> None:
        self.mixer.quit()

    """
    This will stop all playback of all active mixer channels.
    """
    def stop(self) -> None:
        self.mixer.stop()

    """
    This will temporarily stop all playback on the active mixer channels.
     The playback can later be resumed with pygame.mixer.unpause()
    """
    def pause(self) -> None:
        self.pause = True
        self.mixer.pause()

    """
    This will resume all active sound channels after they have been paused.
    """
    def unpause(self) -> None:
        self.pause = False
        self.mixer.unpause()

    """
    This returns the status of the player
    """
    def get_pause(self) -> bool:
        return self.pause

    """
    Returns True if the mixer is busy mixing any channels. 
    If the mixer is idle then this return False.
    """
    def get_busy(self) -> bool:
        self.mixer.get_busy()

    """
    Load a new sound buffer from a filename, a python file object or a readable buffer object.
    args:
        file_path: The path of the mp3 song that should be played.
    """
    def sound(self, file_path: pathlib.Path) -> None:
        self.sound = pygame.mixer.Sound(file=file_path)

    """
    Begin playback of the Sound (i.e., on the computer's speakers) on an available Channel.
    args:
        loops: controls how many times the sample will be repeated after being played the first time.
        maxtime: can be used to stop playback after a given number of milliseconds.
        fade_ms: make the sound start playing at 0 volume and fade up to full volume over the time given. 
    """
    def sound_play(self, loops=0, maxtime=0, fade_ms=0) -> pygame.mixer.Channel:
        return self.sound.play(loops=loops, maxtime=maxtime, fade_ms=fade_ms)

    """
    This will stop the playback of this Sound on any active Channels.
    """
    def sound_stop(self) -> None:
        self.sound.stop()

    """
    This will stop playback of the sound after fading it out over the time argument in milliseconds.
    args:
        time: The amount of time for the fadeout.
    """
    def sound_fadeout(self, time=0) -> None:
        self.sound.fadeout(time=time)

    """
    Set the playback volume for this Sound
    args:
        volume: Volume in the range of 0.0 to 1.0 (inclusive)
    """
    def sound_set_volume(self, volume: float) -> None:
        self.sound.set_volume(value=volume)

    """
    Return a value from 0.0 to 1.0 representing the volume for this Sound.
    """
    def sound_get_volume(self) -> float:
        return self.sound.get_volume()

    """
    This will load a music filename/file object and prepare it for playback
    """
    def music_load(self, file_name: str) -> None:
        pygame.mixer.music.load(file_name)

    """
    Unload the currently loaded music to free up resources
    """
    def music_unload(self) -> None:
        pygame.mixer.music.unload()

    """
    This will play the loaded music stream. If the music is already playing it will be restarted.
    """
    def music_play(self, loops: int=0, start: float=0.0, fade_ms: int=0) -> None:
        pygame.mixer.music.play(loops, start, fade_ms)

    """
    Temporarily stop playback of the music stream.
    """
    def music_pause(self) -> None:
        self.pause = True
        pygame.mixer.music.pause()

    """
    This will resume the playback of a music stream after it has been paused.
    """
    def music_unpause(self) -> None:
        self.pause = False
        pygame.mixer.music.unpause()

    """
    This returns True if the channel is in pause or False otherwise.
    """
    def music_get_pause(self) -> None:
        pygame.mixer.music.get_busy()

    """
    Set the volume of the music playback.
    """
    def music_set_volume(self, value: int) -> None:
        pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + value/100)

    """
    Returns the current volume for the mixer. The value will be between 0.0 and 1.0.
    """ 
    def music_get_volume(self) -> None:
        return pygame.mixer.music.get_volume() * 100

    """
    Returns True when the music stream is actively playing. When the music is idle this returns False.
    """
    def music_get_busy(self) -> bool:
        return pygame.mixer.music.get_busy()