import moviepy
import pygame
import os

# Display size
WINDOW_WIDTH    = 320
WINDOW_HEIGHT   = 240
WINDOW_SURFACE  = pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE

class VideoSprite(pygame.sprite.Sprite):
    def __init__(self, rect, filename):
        pygame.sprite.Sprite.__init__(self)
        os.putenv('SDL_FBDEV', '/dev/fb1')
        pygame.display.init()
        self.window = pygame.display.set_mode( ( WINDOW_WIDTH, WINDOW_HEIGHT ), WINDOW_SURFACE )
        self.image = pygame.Surface((rect.width, rect.height), pygame.HWSURFACE)
        self.rect = self.image.get_rect()
        self.rect.x = rect.x
        self.rect.y = rect.y
        self.video = moviepy.VideoFileClip(filename)
        self.video_stop = False

    def update(self):
        time=pygame.time.get_ticks()
        if not self.video_stop:
            try:
                raw_image = self.video.get_frame(time / 1000)  # /1000 for time in s
                self.image = pygame.image.frombuffer(raw_image, (self.rect.width, self.rect.height), 'RGB')
            except:
                self.video_stop = True

    def close(self):
        pygame.display.quit()

    def get_window(self):
        return self.window

    def get_driver(self):
        return pygame.display.get_driver()

    def get_info(self):
        return pygame.display.Info()
