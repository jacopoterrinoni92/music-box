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
    This will uninitialize pygame.mixer pygame module for loading and playing sounds. 
    All playback will stop and any loaded Sound objects may not be compatible with the mixer 
    if it is reinitialized later.
    """
    def mixer_quit(self) -> None:
        pygame.mixer.quit()

    """
    This returns the status of the player
    """
    def get_pause(self) -> bool:
        return self.pause

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

    
