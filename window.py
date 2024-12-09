import pygame
import pygame.freetype

class Window:
    
    instance = None
    
    def __new__(cls, *args, **kwds):
        if Window.instance is not None:
            return Window.instance
        
        self = object.__new__(cls)
        pygame.display.init()
        self.screen = pygame.display.set_mode((160, 128))
        Window.instance = self
        
        return self
    
    def __init__(self):
        pass
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False
    
    def close(self):
        pygame.display.quit()
        Window.instance = None


