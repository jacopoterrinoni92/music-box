import os
import pygame
import subprocess

# Display size
WINDOW_WIDTH    = 160
WINDOW_HEIGHT   = 128
WINDOW_SURFACE  = pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE

FFMPEG_BIN = "/usr/bin/ffmpeg"

class WindowSprite(pygame.sprite.Sprite):

    def __init__(self, rect, file_name, fps = 30):
        pygame.sprite.Sprite.__init__(self)
        os.putenv('SDL_FBDEV', '/dev/fb1')
        pygame.display.init()
        self.window = pygame.display.set_mode( ( WINDOW_WIDTH, WINDOW_HEIGHT ), WINDOW_SURFACE )
        command = [ FFMPEG_BIN,
                    '-loglevel', 'quiet',
                    '-i', file_name,
                    '-f', 'image2pipe',
                    '-s', '%dx%d' % (rect.width, rect.height),
                    '-pix_fmt', 'rgba',
                    '-vcodec', 'rawvideo', '-' ]
        self.bytes_per_frame = rect.width * rect.height * 3
        self.proc   = subprocess.Popen( command, stdout=subprocess.PIPE, bufsize=self.bytes_per_frame*3 )
        self.image  = pygame.Surface( ( rect.width, rect.height ), pygame.HWSURFACE )
        self.rect   = self.image.get_rect()
        self.rect.x = rect.x
        self.rect.y = rect.y
        # Used to maintain frame-rate
        self.last_at     = 0           # time frame starts to show
        self.frame_delay = 1000 / fps  # milliseconds duration to show frame
        self.video_stop  = False
        
    def close(self):
        pygame.display.quit()
        
    def get_window(self):
        return self.window
        
    def update( self ):
        if ( not self.video_stop ):
            time_now = pygame.time.get_ticks()
            if ( time_now > self.last_at + self.frame_delay ):   # has the frame shown for long enough
                self.last_at = time_now
                try:
                    raw_image = self.proc.stdout.read( self.bytes_per_frame )
                    self.image = pygame.image.frombuffer(raw_image, (self.rect.width, self.rect.height), 'RGB')
                    #self.proc.stdout.flush()  - doesn't seem to be necessary
                except:
                    # error getting data, end of file?  Black Screen it
                    self.image = pygame.Surface( ( self.rect.width, self.rect.height ), pygame.HWSURFACE )
                    self.image.fill( ( 0,0,0 ) )
                    self.video_stop = True
        
    def flip(self):
        pygame.display.flip()
        
    def get_driver(self):
        return pygame.display.get_driver()
    
    def get_info(self):
        return pygame.display.Info()


