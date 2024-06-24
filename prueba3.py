import pygame
# Your game setup would go here
gameScreen = pygame.display.set_mode((800,600))
pygame.display.set_caption('Pygame Mouse Click - Test Game')

a = pygame.Rect((100,100),(100,100))
#a.fill("white")
b = pygame.Rect((500,400),(100,100))
#b.fill("pink")



running = True
while running:
    gameScreen.fill((0,0,0)) # Clear the screen
    pygame.draw.rect(gameScreen,"white",a)
    pygame.draw.rect(gameScreen,"pink",b)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if a.collidepoint(x, y): print("a")
            if b.collidepoint(x, y): print("b")
            