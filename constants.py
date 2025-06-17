import pygame
import pyautogui
from widgets import Button, DropDown

pygame.font.init()
#pygame.display.init()

DECKS = ["spells", "cards_a", "cards_b"]


FACTIONS = ["INVESTIGATORS", "DEEP_ONES", "CULTIST", "SERPENT_PEOPLE"]

ROWS = 8
COLUMNS = 12
#CELL = 100

BACKGROUND_COLOR = (0,0,0)

GRID = [(x, y) for x in range(COLUMNS) for y in range(ROWS)]
GRID_DIC = {}
for cell in GRID:
    GRID_DIC.update({cell:"None"})

FPS = 60





resolution_info = pyautogui.size()
WIDTH, HEIGHT = resolution_info.width-100, resolution_info.height-150

HEIGHT = resolution_info.height -100
BASIC_UNIT = round(HEIGHT/12,0)

CELL = round(HEIGHT/8,0)
CELL = BASIC_UNIT
WIDTH = resolution_info.width - BASIC_UNIT
CARD_WIDTH = BASIC_UNIT*4/5

#WIN = pygame.display.set_mode((WIDTH, HEIGHT))
BOARD = pygame.Surface((CELL*COLUMNS, CELL*ROWS))



#positions


#FACTION_HAND = pygame.Rect((BOARD.get_width(),))
SPELLS_HAND = pygame.Rect((BOARD.get_width(),  HEIGHT-CELL*1.8),((WIDTH-BOARD.get_width()),CELL*1.8))
FACTION_HAND = pygame.Rect((BOARD.get_width(),HEIGHT-SPELLS_HAND.height*2),((WIDTH-BOARD.get_width()), CELL*1.8))

FACTION_HAND = pygame.Rect((0, BOARD.get_height()),((BOARD.get_width()/2), CELL*1.8))
SPELLS_HAND = pygame.Rect((FACTION_HAND.width, BOARD.get_height()),((BOARD.get_width()/2),CELL*1.8))

FACTION_DECK_POSITION = (FACTION_HAND.x+FACTION_HAND.width-CARD_WIDTH*1.1, FACTION_HAND.y+CELL/4)
SPELL_DECK_POSITION = (SPELLS_HAND.x+SPELLS_HAND.width-CARD_WIDTH*1.1, SPELLS_HAND.y+CELL/4)


PHASE_INFORMER_RECT = (BOARD.get_width()+20, CELL*0.6)


#FACTION_DECK_POSITION = (FACTION_HAND.x+FACTION_HAND.width/2-(CARD_WIDTH*5/3)/2, FACTION_HAND.y+FACTION_HAND.height-CELL)
#SPELL_DECK_POSITION = (SPELLS_HAND.x+SPELLS_HAND.width/2-(CARD_WIDTH*5/3)/2, SPELLS_HAND.y+SPELLS_HAND.height-CELL)

PRE_GAME_TOKEN_MAT = pygame.Rect((0,0),(BOARD.get_width(), CELL*5))

# enemy positions

ENEMY_FACTION_HAND = pygame.Rect((BOARD.get_width(),0),((WIDTH-BOARD.get_width())//2, CELL//2))
ENEMY_SPELLS_HAND = pygame.Rect((BOARD.get_width()+ENEMY_FACTION_HAND.width,0),((WIDTH-BOARD.get_width())//2, CELL//2))
INFORMATION_FRAME = pygame.Rect((BOARD.get_width(),CELL*1),((WIDTH-BOARD.get_width()),CELL*5))
LOG_FRAME = pygame.Rect((BOARD.get_width(),CELL*7), ((WIDTH-BOARD.get_width()-CELL),CELL*3))

# Buttons

pre_game_cancel_button = pygame.Rect((CELL, CELL//4*3),(CELL*2,CELL//2))
pre_game_ok_button = pygame.Rect((CELL*4, CELL//4*3),(CELL*2,CELL//2))

faction_deck_drawer_button = pygame.Rect(FACTION_DECK_POSITION,(CARD_WIDTH,CARD_WIDTH*5/3))
spells_deck_drawer_button = pygame.Rect(SPELL_DECK_POSITION,(CARD_WIDTH,CARD_WIDTH*5/3))

#faction_deck_drawer_button = pygame.Rect(FACTION_DECK_POSITION,(CARD_WIDTH*5/3,CARD_WIDTH))
#spells_deck_drawer_button = pygame.Rect(SPELL_DECK_POSITION,(CARD_WIDTH*5/3,CARD_WIDTH))

button2 = pygame.Rect((WIDTH-CELL, 20),(CELL,20))

no_defense_button = pygame.Rect((WIDTH-CELL, CELL*2),(CELL,CELL))

temporal_change_turn_button = pygame.Rect((WIDTH-CELL*2, CELL*2),(CELL,CELL))



# MAIN MENU






#print(CELL)
#print(resolution_info.current_h, "    ", resolution_info.current_w)
#WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# 
GENERIC_FONT = pygame.font.SysFont("times", int(CELL*0.2))
CARD_FONT = pygame.font.SysFont("times",int(CELL*0.18))



GAME_SEQUENCE = ["a_fate", "a_move", "a_att", "b_def","b_fate", "b_move", "b_att", "a_def"]
GAME_SEQUENCE = ["fate", "move", "att"]
GAME_SEQUENCE = ["fate", "summon", "move", "att"]

### Constants for object loaders



REQ_FIELDS = ['Images','Unit_Name', 'Hits', 'Notes'] # for token objects in Player_Object

