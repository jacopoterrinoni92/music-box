import pygame
import os


#os.putenv('SDL_VIDEODRIVER', "drmkms")
os.putenv('SDL_FBDEV', "/dev/fb1")

pygame.display.init()

width = pygame.display.Info().current_w

print("Width: = %d", width)
print(pygame.display.get_num_displays())
print(pygame.display.get_driver())
print(pygame.display.Info())
