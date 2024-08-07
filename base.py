import pygame

import math

import os

from constants import FACTIONS, ROWS, COLUMNS, GRID, FPS, BACKGROUND_COLOR, GRID_DIC
from gameobjects import TokenObject, CardObject
from turnmodule import new_game_preparations, fate_phase
from dbcreator import conection_sql
from dbintermediatefunctions import card_data_extractor, discarder



WIDTH, HEIGHT = 900, 800
pygame.display.init()
pygame.font.init()
resolution_info = pygame.display.Info()
WIDTH, HEIGHT = resolution_info.current_w-100, resolution_info.current_h-90
HEIGHT = resolution_info.current_h -90
CELL = round(HEIGHT/8,0)
WIDTH = CELL*15
print(CELL)
print(resolution_info.current_h, "    ", resolution_info.current_w)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TO CHANGE")

#ROWS = 8
#COLUMNS = 8
#CELL = 100
#
#BACKGROUND_COLOR = (0,0,0)
#
BOARD = pygame.Surface((CELL*8, CELL*8))
FACTION_HAND = pygame.Rect((WIDTH-CELL*7,CELL*4),(CELL*8, CELL*2))
SPELLS_HAND = pygame.Rect((WIDTH-CELL*7,CELL*6),(CELL*8,CELL*2))
button = pygame.Rect((FACTION_HAND.x+CELL*5,FACTION_HAND.y),(CELL,20))


GENERIC_FONT = pygame.font.SysFont("times", int(CELL*0.2))
#GRID = [(x, y) for x in range(8) for y in range(8)]
#GRID_DIC = {}
#for cell in GRID:
#    GRID_DIC.update({cell:"None"})
#
#FPS = 60

chosen_cell = None
pos_a = pygame.Vector2(0, 0)
#pos_b = pygame.Vector2(0, 0)
pos_b = None
game_objects_list = []
hand_card_list = []




def grid_position(position):
    """translates clicks into discrete cell positions

    Args:
        position (tuple): coordinates

    Returns:
        tuple: cell position
    """
    
    x = (position[0]//CELL)#*CELL
    y = (position[1]//CELL)#*CELL
    return (x,y)




        

def draw_window(pos, token, card, drawn_cards):
    
    global chosen_cell
    global pos_a
    global pos_b
    
    WIN.fill(BACKGROUND_COLOR)
    BOARD.fill("tan4")
    #FACTION_HAND.fill("pink")
    #SPELLS_HAND.fill("red")
    #faction_hand_rect = pygame.Rect(0,0,FACTION_HAND.get_width(),FACTION_HAND.get_height())
    
    #FACTION_HAND.
    
    
    
    for row in range(ROWS):
        for col in range(row % 2, ROWS, 2):
            pygame.draw.rect(BOARD, "grey3",(CELL*row, CELL*col, CELL,CELL))
   
    
    if chosen_cell != None:
        
        pygame.draw.rect(BOARD, (127+waving_func(pygame.time.get_ticks()-chosen_cell[1]),127+waving_func(pygame.time.get_ticks()-chosen_cell[1]),127+waving_func(pygame.time.get_ticks()-chosen_cell[1])), chosen_cell[0])
        
    
    
    game_mechanics(pos, token)    
    
    
    WIN.blit(BOARD,(0,0))    # actualizes BOARD -> always after all changes of it
    #WIN.blit(FACTION_HAND,(CELL*8,0))
    #WIN.blit(SPELLS_HAND,(CELL*8,CELL*4))
    
    pygame.draw.rect(WIN, "pink",FACTION_HAND)
    pygame.draw.rect(WIN, "red",SPELLS_HAND)
    pygame.draw.rect(WIN,"grey", button)
    faction_hand_sign = GENERIC_FONT.render("Faction Hand", 1, "black")
    WIN.blit(faction_hand_sign,(FACTION_HAND.x+5,FACTION_HAND.y))
    spells_hand_sign = GENERIC_FONT.render("Spells hand",1,"black")
    WIN.blit(spells_hand_sign, (SPELLS_HAND.x+5,SPELLS_HAND.y))
    """for crd in hand_card_list:
        crd.rec.x = FACTION_HAND.x+5+CELL*hand_card_list.index(crd)*0.7
        crd.card_positioner()
        crd.card_drawer(WIN)
    if card != None:
        hand_card_list[card].card_drawer(WIN)"""
    faction_hand_controller(card, drawn_cards)
    
    
        
    
    
    pygame.display.update()
    

def waving_func(time):
    z = 127*math.cos((2*math.pi/(FPS*40))*time)
    return z

def game_mechanics(pos, token):
    
    global chosen_cell
    global pos_a
    global pos_b
    
    
    #print("en game_mechanics: ", token)
    
    
    
    
    if pos != None:
        
        selected_pos = grid_position(pos)
        if token != None:
            tokenpos = grid_position((token.rec.x, token.rec.y))
            if tokenpos == selected_pos:
                print("token = pos")
                token.moving = True
        
        selected_in_grid = GRID.index(selected_pos)
        chosen_cell = (pygame.Rect(CELL*selected_pos[0], CELL*selected_pos[1], CELL, CELL),pygame.time.get_ticks())
        pos_b = pygame.Vector2(chosen_cell[0].x, chosen_cell[0].y)
        print(selected_in_grid)
    
    
    for obj in game_objects_list: 
        #print(obj.moving)
        if obj.moving:
            obj.token_object_drawer(BOARD, pos_b)
        else: obj.token_object_drawer(BOARD)
        
    #draw_window(pos, None)
    
def faction_hand_controller(card, drawn_cards):
    
    global hand_card_list
    
    for drawn in drawn_cards:
        identif_list = []   # list of identifiers of cardobjects
        for crd in hand_card_list:
            identif_list.append(crd.identif)
        try: 
            identif_list.index(drawn[0]) # checks if cardobject already added
        except:
            hand_card_list.append(CardObject(CELL,0,0,drawn[3],drawn[0])) #adds cardobject
        #hand_card_list = list(set(hand_card_list))
        
    for crd in hand_card_list:  # positions cardobject
        crd.rec.x = FACTION_HAND.x+5+CELL*hand_card_list.index(crd)*0.7 # assigns position to the object in the hand
        crd.rec.y = FACTION_HAND.y+CELL*0.3
        crd.card_positioner() #
        crd.card_drawer(WIN)
    if card != None: #focus card changes size/picture 
        try: 
            hand_card_list[card].card_drawer(WIN)
        except: pass
    collide = FACTION_HAND.collideobjectsall(hand_card_list, key=lambda crdobj: crdobj.rec)
    #print("hand_card_list: ",hand_card_list)
    #print("collide: ",collide)
    
    

    
def main():
    """ Main game function
    """
    
    run = True
    clock = pygame.time.Clock()
    #pygame.draw.rect(WIN, "pink",FACTION_HAND)
    #pygame.draw.rect(WIN, "pink",SPELLS_HAND)
    prueba = TokenObject(CELL, pos_a[0], pos_a[1], "token_1.png", "prueba1")
    prueba2 = TokenObject(CELL,CELL*3, 0, "token_2.png", "prueba2")
    prueba3 = TokenObject(CELL,CELL*7,CELL*7, "token_3.png", "prueba3")
    pruebacard1 = CardObject(CELL, FACTION_HAND.x+5, FACTION_HAND.y+CELL*0.3, "LiK7BK9ia.jpeg", "pruebacard1" )
    pruebacard2 = CardObject(CELL, FACTION_HAND.x+5+CELL, FACTION_HAND.y+CELL*0.3, "McLLez6ki.jpeg", "pruebacard2" )
    
    game_objects_list.append(prueba)
    game_objects_list.append(prueba2)
    game_objects_list.append(prueba3)
    
    resolution_info = pygame.display.Info()
    print(resolution_info.current_h)
    print(str(game_objects_list))
    print(prueba)
    
    
    
    new_game_preparations("INVESTIGATORS","SERPENT_PEOPLE")
        
    
    while run:
        
        clock.tick(FPS)
        pos = None
        surface = None
        chosen_token = None
        focus_faction_card = None
        drawn_cards = []
        mousepos = pygame.mouse.get_pos()
        #event = pygame.event.poll()
        """if FACTION_HAND.collidepoint(mousepos): 
            surface = "faction_hand"
            #print(surface)
        elif SPELLS_HAND.collidepoint(mousepos):
            surface = "spells_hand"  
            #print(surface)
        elif BOARD.get_rect().collidepoint(mousepos):
            surface = "board"
            #print(surface)"""
            
        if BOARD.get_rect().collidepoint(mousepos):
            surface = "board"
            #surface = "board"
            pygame.mouse.set_cursor(pygame.cursors.diamond)
            for obj in game_objects_list:
                
                if obj.rec.collidepoint(pygame.mouse.get_pos()):
                    pygame.mouse.set_cursor(pygame.cursors.broken_x)
                    
        else:
            pygame.mouse.set_cursor(pygame.cursors.arrow) 
            if FACTION_HAND.collidepoint(mousepos): 
                surface = "faction_hand"
                
            elif SPELLS_HAND.collidepoint(mousepos):
                surface = "spells_hand" 
                #pygame.mouse.set_cursor(pygame.cursors.arrow)
        
        for card in hand_card_list:
            if card.rec.collidepoint(mousepos): 
                card.looked_on = True
                #card.card_drawer(WIN)
                focus_faction_card = hand_card_list.index(card)
                
                #print(focus_faction_card)
                #if card.looked_on: print("card collide",card.looked_on)
            else:
                card.looked_on = False
                #card.card_drawer(WIN)
                
                #print("card collide, height: ",card.rec.height)
            #else: card.card_drawer(WIN)
                
        
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                print("surface: ",surface)
                
                if pygame.mouse.get_cursor()==pygame.cursors.diamond:
                    pos = pygame.mouse.get_pos()
                    print("board ", pos)
                elif pygame.mouse.get_cursor()==pygame.cursors.broken_x:
                    pos = pygame.mouse.get_pos()
                    print("image pressed")
                    for obj in game_objects_list:
                        if obj.rec.collidepoint(mousepos):
                            print(obj)
                            chosen_token = obj
                            print(type(chosen_token))
                        #else: chosen_token = None
                else: 
                    print("no board")
                    if button.collidepoint(mousepos):
                        print("draw")
                        fate_phase("cards_a", "deck", "hand")
                        drawn_cards = card_data_extractor("cards_a", "hand")
                    else:
                        
                        for crd in hand_card_list:
                            if crd.rec.collidepoint(mousepos):
                                print(crd.identif)
                                discarder("cards_a", str(crd.identif))
                                hand_card_list.remove(crd)
                                drawn_cards = card_data_extractor("cards_a", "hand")
            
            #if event.type == pygame.Mo
        #game_mechanics(pos)           
        draw_window(pos, chosen_token, focus_faction_card, drawn_cards)
    
    #prueba = GameObject(CELL, 0, 0)       
            
                
            
            
        
        
        
        
    
    pygame.quit()

    

if __name__=="__main__":
    
    print(GRID_DIC)
    main()
    