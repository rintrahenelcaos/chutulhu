import pygame

pygame.font.init()
pygame.display.init()

DECKS = ["spells", "cards_a", "cards_b"]


FACTIONS = ["INVESTIGATORS","DEEP_ONES", "CULTIST","SERPENT_PEOPLE"]

ROWS = 8
COLUMNS = 8
#CELL = 100

BACKGROUND_COLOR = (0,0,0)

GRID = [(x, y) for x in range(8) for y in range(8)]
GRID_DIC = {}
for cell in GRID:
    GRID_DIC.update({cell:"None"})

FPS = 60





resolution_info = pygame.display.Info()
WIDTH, HEIGHT = resolution_info.current_w-100, resolution_info.current_h-90
HEIGHT = resolution_info.current_h -90
CELL = round(HEIGHT/8,0)
WIDTH = CELL*15
CARD_WIDTH = CELL*4/5

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
BOARD = pygame.Surface((CELL*8, CELL*8))


#positions

FACTION_HAND = pygame.Rect((WIDTH-CELL*7,CELL*4),(CELL*8, CELL*2))
SPELLS_HAND = pygame.Rect((WIDTH-CELL*7,CELL*6),(CELL*8,CELL*2))


FACTION_DECK_POSITION = (WIDTH-CELL,FACTION_HAND.y+CELL/2)
SPELL_DECK_POSITION = (WIDTH-CELL,SPELLS_HAND.y+CELL/2)

PRE_GAME_TOKEN_MAT = pygame.Rect((0,0),(CELL*8, CELL*5))

# Buttons

pre_game_cancel_button = pygame.Rect((CELL, CELL//4*3),(CELL*2,CELL//2))
pre_game_ok_button = pygame.Rect((CELL*4, CELL//4*3),(CELL*2,CELL//2))

faction_deck_drawer_button = pygame.Rect(FACTION_DECK_POSITION,(CARD_WIDTH,CARD_WIDTH*5/3))
spells_deck_drawer_button = pygame.Rect(SPELL_DECK_POSITION,(CARD_WIDTH,CARD_WIDTH*5/3))
button2 = pygame.Rect((WIDTH-CELL, 20),(CELL,20))

no_defense_button = pygame.Rect((WIDTH-CELL, CELL*2),(CELL,CELL))




#print(CELL)
#print(resolution_info.current_h, "    ", resolution_info.current_w)
#WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# 
GENERIC_FONT = pygame.font.SysFont("times", int(CELL*0.2))
CARD_FONT = pygame.font.SysFont("times",int(CELL*0.18))

GAME_SEQUENCE = ["a_fate", "a_move", "a_att", "b_def","b_fate", "b_move", "b_att", "a_def"]
GAME_SEQUENCE = ["def", "clean", "fate", "move", "att"]

