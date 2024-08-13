import pygame
from pygame.locals import *

SIZE = 500, 200
RED = (255, 0, 0)
GRAY = (150, 150, 150)

pygame.init()
screen = pygame.display.set_mode(SIZE)

rect = Rect(50, 60, 200, 80)
print(f'x={rect.x}, y={rect.y}, w={rect.w}, h={rect.h}')
print(f'left={rect.left}, top={rect.top}, right={rect.right}, bottom={rect.bottom}')
print(f'center={rect.center}')
rect0 = Rect.copy()

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        
        if event.type == KEYDOWN:
            if event.key in dir:
                v = dir[event.key]
                rect.inflate_ip(v)

    screen.fill(GRAY)
    pygame.draw.rect(screen, GRAY, rect0, 1)
    pygame.draw.rect(screen, RED, rect, 4)
    pygame.display.flip()

pygame.quit()