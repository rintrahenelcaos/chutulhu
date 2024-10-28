import pygame

from constants import WIDTH, HEIGHT,FACTION_DECK_POSITION, FACTION_HAND, SPELL_DECK_POSITION, SPELLS_HAND, BOARD, BACKGROUND_COLOR, ENEMY_FACTION_HAND, ENEMY_SPELLS_HAND, ROWS, CELL, GENERIC_FONT
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  
pygame.display.init()
pygame.font.init()
pygame.display.set_caption("TO CHANGE")
run = True

while run:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            
            
            run = False
    
    WIN.fill(BACKGROUND_COLOR)
    BOARD.fill("tan4")
    for row in range(ROWS):
        for col in range(row % 2, ROWS, 2):
            pygame.draw.rect(BOARD, "grey3",(CELL*row, CELL*col, CELL,CELL))
    WIN.blit(BOARD,(0,0))
    pygame.draw.rect(WIN, "pink",FACTION_HAND)
    pygame.draw.rect(WIN, "red",SPELLS_HAND)
    pygame.draw.rect(WIN, "pink",ENEMY_FACTION_HAND)
    pygame.draw.rect(WIN, "red",ENEMY_SPELLS_HAND)
    current_phase_informer = GENERIC_FONT.render("phase_informer", 1, "red")
    WIN.blit(current_phase_informer, (CELL*10, 20))
    
    pygame.display.update()
    
    
    
    
pygame.quit()