import pygame
# Your game setup would go here
gameScreen = pygame.display.set_mode((800,600))
pygame.display.set_caption('Pygame Mouse Click - Test Game')
# Define rectangles and their colors
rectangles = [
    {"rect": pygame.Rect((100, 100), (100, 100)), "color": (255,0,0), "clicked_color": (255,255,0)}, # Red rectangle
    {"rect": pygame.Rect((350, 275), (100, 100)), "color": (0,255,0), "clicked_color": (255,0,255)}, # Green rectangle
    {"rect": pygame.Rect((600, 450), (100, 100)), "color": (0,0,255), "clicked_color": (0,255,255)}  # Blue rectangle
]
running = True
while running:
    gameScreen.fill((0,0,0)) # Clear the screen
    for r in rectangles:  # Draw rectangles
        pygame.draw.rect(gameScreen, r["color"], r["rect"])
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos() # Get click position
            for r in rectangles: # Check each rectangle
                if r["rect"].collidepoint(x, y): # Check if click is within rectangle
                    r["color"] = r["clicked_color"] # Change the clicked color
pygame.quit()