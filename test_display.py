import pygame
import os


#os.putenv('SDL_VIDEODRIVER', "directfb")
os.putenv('SDL_FBDEV', "/dev/fb1")

pygame.display.init()

with open("/dev/fb1", "wb") as f:
    pass

width = pygame.display.Info().current_w

print("Width: = %d", width)
print(pygame.display.get_num_displays())
print(pygame.display.get_driver())
print(pygame.display.Info())
