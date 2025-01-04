import moviepy
import pygame
import os

# Display size
WINDOW_WIDTH    = 320
WINDOW_HEIGHT   = 240
WINDOW_SURFACE  = pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_GRAY = (50, 50, 50)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_YELLOW = (255, 255, 0)

class Window:

    def __init__(self):
        os.putenv('SDL_FBDEV', '/dev/fb1')
        pygame.display.init()
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), WINDOW_SURFACE)

    def fill(self, obj = COLOR_GRAY):
        self.window.fill(obj)

    def close(self):
        pygame.display.quit()

    def get_window(self):
        return self.window

    def get_driver(self):
        return pygame.display.get_driver()

    def get_info(self):
        return pygame.display.Info()


class TextSprite(pygame.sprite.Sprite):

    def __init__(
            self, 
            text_str: str, 
            pos_x = 0, 
            pos_y = 0, 
            width = WINDOW_WIDTH, 
            height = WINDOW_HEIGHT, 
            font_name = None, 
            size = 18, 
            background = COLOR_WHITE, 
            color = COLOR_BLACK
        ):
        pygame.sprite.Sprite.__init__(self)

        self.font = pygame.font.SysFont(font_name, size)
        self.rect = pygame.Rect(pos_x, pos_y, width, height)
        self.image = pygame.Surface((self.rect.width, self.rect.height), pygame.HWSURFACE)
        self.image.fill(background)

        self.text_str = text_str
        self.width = width
        self.height = height
        self.color = color

    def set_text_str(self, new_text_str: str):
        self.text_str = new_text_str

    def close():
        pygame.font.quit()

    def update(self):
        text_surface = self.font.render(self.text_str, True, self.color)
        rect = text_surface.get_rect()
        self.image.blit(text_surface, [self.width // 2, self.height // 2])


class VideoSprite(pygame.sprite.Sprite):
    
    def __init__(self, pos_x = 0, pos_y = 0, width = WINDOW_WIDTH, height = WINDOW_HEIGHT):
        pygame.sprite.Sprite.__init__(self)

        rect = pygame.Rect(pos_x, pos_y, width, height)
        self.image = pygame.Surface((rect.width, rect.height), pygame.HWSURFACE)

        self.rect = self.image.get_rect()
        self.rect.x = rect.x
        self.rect.y = rect.y

        self.video = None
        self.video_pause = False

        self.duration = 0
        self.video_fps = 0

        self.elapsed = 0

    def set_elapsed(self, new_elapsed: float):
        self.elapsed = new_elapsed

    def update(self):
        if not self.video_pause:
            try:
                raw_image = self.video.get_frame(((self.elapsed) / 1000) % self.duration)  # /1000 for time in s
                self.image = pygame.image.frombuffer(raw_image, (self.rect.width, self.rect.height), 'RGB')
            except:
                self.close_clip()

    def set_video_pause(self, new_video_pause: bool):
        self.video_pause = new_video_pause

    def load_clip(self, filename: str, target_resolution=(WINDOW_WIDTH, WINDOW_HEIGHT)):
        self.video = moviepy.VideoFileClip(filename=filename, audio=False, target_resolution=target_resolution)
        self.duration = self.video.duration

    def get_clip(self):
        return self.video

    def close_clip(self):
        self.video.close()
