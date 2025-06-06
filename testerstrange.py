import sys
import pygame
from pygame.locals import *
 
pygame.init()
 
screen = pygame.display.set_mode((640,480))
 
# Game loop.
while True:
    screen.fill((0, 0, 0))
    
    for event in pygame.event.get():
        print(event)
        if event.type == QUIT:
            pygame.quit()
            sys.exit()



















