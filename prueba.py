import pygame
import os

from constants import WIDTH, HEIGHT,FACTION_DECK_POSITION, FACTION_HAND, SPELL_DECK_POSITION, SPELLS_HAND, BOARD, BACKGROUND_COLOR, ENEMY_FACTION_HAND, ENEMY_SPELLS_HAND, ROWS, COLUMNS ,CELL, GENERIC_FONT, faction_deck_drawer_button, spells_deck_drawer_button, INFORMATION_FRAME, PHASE_INFORMER_RECT, LOG_FRAME, INFORMATION_SLIDE
from widgets import TextScroll, TextScrollLog

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
    pygame.draw.rect(WIN,"yellow", INFORMATION_FRAME)
    pygame.draw.rect(WIN, "aqua", INFORMATION_SLIDE)
    
    STORY1 = """FIRST LINE OF TEXT
    second line of text
    third line of text
    ** last line of text that fits
    this line should force scroll up
    and here again for
    each line the follows"""
    STORY1 = ["FIRST LINE OF TEXT",
              "second line of text"]
    #pygame.draw.rect(WIN, "pink", LOG_FRAME)
    #scrolltest = TextScrollLog(LOG_FRAME, pygame.font.SysFont("Liberation Sans", 65), "yellow", "red", "pink", STORY1)
    #scrolltest.update()
    #scrolltest.draw(WIN)
    
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
    WIN.blit(current_phase_informer, PHASE_INFORMER_RECT)
    
    pygame.display.update()
    
    
    
    
pygame.quit()