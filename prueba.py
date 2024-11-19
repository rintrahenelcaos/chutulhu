import pygame
import os

from constants import WIDTH, HEIGHT,FACTION_DECK_POSITION, FACTION_HAND, SPELL_DECK_POSITION, SPELLS_HAND, BOARD, BACKGROUND_COLOR, ENEMY_FACTION_HAND, ENEMY_SPELLS_HAND, ROWS, COLUMNS ,CELL, GENERIC_FONT, faction_deck_drawer_button, spells_deck_drawer_button, INFORMATION_FRAME
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
        for col in range(row % 2, COLUMNS, 2):
            pygame.draw.rect(BOARD, "grey3",(CELL*col, CELL*row, CELL,CELL))
    WIN.blit(BOARD,(0,0))
    pygame.draw.rect(WIN, "pink",FACTION_HAND)
    pygame.draw.rect(WIN, "red",SPELLS_HAND)
    pygame.draw.rect(WIN, "pink",ENEMY_FACTION_HAND)
    pygame.draw.rect(WIN, "red",ENEMY_SPELLS_HAND)
    pygame.draw.rect(WIN,"white",faction_deck_drawer_button)
    pygame.draw.rect(WIN,"white", INFORMATION_FRAME)
    faction_deck = pygame.image.load(os.path.join("images","faction_deck2.jpg")).convert_alpha() # load faction deck image
    #faction_deck_scaled_image = pygame.transform.rotate(faction_deck, 90.0)
    faction_deck_scaled_image = pygame.transform.scale(faction_deck, (faction_deck_drawer_button.width, faction_deck_drawer_button.height))
    WIN.blit(faction_deck_scaled_image, (faction_deck_drawer_button))

    pygame.draw.rect(WIN,"white",spells_deck_drawer_button)
    spells_deck = pygame.image.load(os.path.join("images","spells_deck_scaled.jpg")).convert_alpha() # load spells deck image
    #spells_deck_scaled_image = pygame.transform.rotate(spells_deck, 90.0)
    spells_deck_scaled_image = pygame.transform.scale(spells_deck,(spells_deck_drawer_button.width, spells_deck_drawer_button.height))
    WIN.blit(spells_deck_scaled_image, (spells_deck_drawer_button))
    current_phase_informer = GENERIC_FONT.render("phase_informer", 1, "red")
    WIN.blit(current_phase_informer, (BOARD.get_width()+20, CELL*0.6))
    
    pygame.display.update()
    
    
    
    
pygame.quit()