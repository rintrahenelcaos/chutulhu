import pygame

import math

import os

from constants import FACTIONS, ROWS, COLUMNS, GRID, FPS, BACKGROUND_COLOR, GRID_DIC, WIDTH, HEIGHT, CELL, GAME_SEQUENCE, CARD_WIDTH, FACTION_HAND, SPELLS_HAND, FACTION_DECK_POSITION, SPELL_DECK_POSITION, WIN, BOARD, faction_deck_drawer_button,spells_deck_drawer_button,button2, GENERIC_FONT,CARD_FONT
from gameobjects import TokenObject, CardObject
from player_turn_module import new_game_preparations, fate_phase, move_phase, grid_position,to_grid,Player_Object
from dbcreator import conection_sql
from dbintermediatefunctions import card_data_extractor, discarder
from functionsmodule import movement_blocker, available_movement_detector_pathfinding, available_movement_detector_linear_vector, available_attacks_detector_fixedrange, available_attacks_detector_maxrange_square


#WIDTH, HEIGHT = 900, 800
pygame.display.init()
pygame.font.init()
#resolution_info = pygame.display.Info()
#WIDTH, HEIGHT = resolution_info.current_w-100, resolution_info.current_h-90
#HEIGHT = resolution_info.current_h -90
#CELL = round(HEIGHT/8,0)
#WIDTH = CELL*15
#print(CELL)
#print(resolution_info.current_h, "    ", resolution_info.current_w)
#WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TO CHANGE")

#ROWS = 8
#COLUMNS = 8
#CELL = 100
#
#BACKGROUND_COLOR = (0,0,0)
#
#BOARD = pygame.Surface((CELL*8, CELL*8))
#FACTION_HAND = pygame.Rect((WIDTH-CELL*7,CELL*4),(CELL*8, CELL*2))
#SPELLS_HAND = pygame.Rect((WIDTH-CELL*7,CELL*6),(CELL*8,CELL*2))

#faction_deck_drawer_button = pygame.Rect(FACTION_DECK_POSITION,(CARD_WIDTH,CARD_WIDTH*5/3))
#spells_deck_drawer_button = pygame.Rect(SPELL_DECK_POSITION,(CARD_WIDTH,CARD_WIDTH*5/3))
#button2 = pygame.Rect((WIDTH-CELL, 20),(CELL,20))


#GENERIC_FONT = pygame.font.SysFont("times", int(CELL*0.2))
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

   

def draw_window(card, player_a_hand, scrd, spell_player_a_hand ,current_phase, player, movement_indicator, available_moves, available_attacks,player_tokens, player2_tokens):
    
    global chosen_cell
    global pos_a
    global pos_b
    phase_informer = str
    
    if player:
        phase_informer = "a_"+current_phase
    else: phase_informer = "b_"+current_phase
    
    WIN.fill(BACKGROUND_COLOR)
    BOARD.fill("tan4")
        
    for row in range(ROWS):
        for col in range(row % 2, ROWS, 2):
            pygame.draw.rect(BOARD, "grey3",(CELL*row, CELL*col, CELL,CELL))
   
    
    available_moves_function(available_moves)   
    token_movement(player_tokens, player2_tokens)
    available_attacks_function(available_attacks)
    
    
    WIN.blit(BOARD,(0,0))    # actualizes BOARD -> always after all changes of it
    
    pygame.draw.rect(WIN, "pink",FACTION_HAND)
    pygame.draw.rect(WIN, "red",SPELLS_HAND)
    
    
    faction_deck = pygame.image.load(os.path.join("images","faction_deck2.jpg")).convert_alpha() # load faction deck image
    faction_deck_scaled_image = pygame.transform.scale(faction_deck, (faction_deck_drawer_button.width, faction_deck_drawer_button.height))
    WIN.blit(faction_deck_scaled_image, (faction_deck_drawer_button))
    
    pygame.draw.rect(WIN, "white", button2)
    
    spells_deck = pygame.image.load(os.path.join("images","spells_deck_scaled.jpg")).convert_alpha() # load spells deck image
    spells_deck_scaled_image = pygame.transform.scale(spells_deck,(spells_deck_drawer_button.width, spells_deck_drawer_button.height))
    WIN.blit(spells_deck_scaled_image, (spells_deck_drawer_button))
    
    current_phase_informer = GENERIC_FONT.render(phase_informer, 1, "red")
    WIN.blit(current_phase_informer, (CELL*10, 20))
    
    faction_hand_sign = GENERIC_FONT.render("Faction Hand", 1, "black")
    WIN.blit(faction_hand_sign,(FACTION_HAND.x+5,FACTION_HAND.y))
    
    spells_hand_sign = GENERIC_FONT.render("Spells hand",1,"black")
    WIN.blit(spells_hand_sign, (SPELLS_HAND.x+5,SPELLS_HAND.y))
    
    faction_hand_controller(card, player_a_hand, current_phase)
    spells_hand_controller(scrd, spell_player_a_hand, current_phase)
    
    
        
    
    
    pygame.display.update()
    

def waving_func(time):
    z = 127*math.cos((2*math.pi/(FPS*40))*time)
    return z


        
def token_movement(player_tokens, player2_tokens):
    
    #print("new token mov")
    
    for obj in player_tokens:
        obj.token_object_drawer(BOARD)
    for obj2 in player2_tokens:
        obj2.token_object_drawer(BOARD)
            
    
    
def faction_hand_controller(card, player_hand, current_phase):
    
            
    for crd in player_hand:  # positions cardobject
        
        ypos = float
        position = pygame.Vector2(0,0)
        #crd.rec.x = FACTION_HAND.x+5+CELL*player_hand.index(crd)*0.7 # assigns position to the object in the hand
        #crd.rec.y = FACTION_HAND.y+CELL*0.7
        
        if current_phase == "move" and (crd.card_type == "M" or crd.card_type == "XS" or crd.card_type == "XF"):
            ypos = FACTION_HAND.y+CELL*0.3
            position = pygame.Vector2(FACTION_HAND.x+5+CELL*player_hand.index(crd)*0.7, ypos)
            #crd.card_drawer(WIN,pygame.Vector2(FACTION_HAND.x+5+CELL*player_hand.index(crd)*0.7, ypos))
            
        elif current_phase == "att" and (crd.card_type == "A"):
            ypos = FACTION_HAND.y+CELL*0.3
            position = pygame.Vector2(FACTION_HAND.x+5+CELL*player_hand.index(crd)*0.7, ypos)
        
            #crd.card_drawer(WIN, position)  
        elif current_phase == "def" and (crd.card_type == "D"):
            ypos = FACTION_HAND.y+CELL*0.3
            position = pygame.Vector2(FACTION_HAND.x+5+CELL*player_hand.index(crd)*0.7, ypos)
        
            #crd.card_drawer(WIN, position)  
        elif current_phase == "fate":
            ypos = FACTION_HAND.y+CELL*0.7
            position = pygame.Vector2(FACTION_HAND.x+5+CELL*player_hand.index(crd)*0.7, ypos)
        else:
            ypos = FACTION_HAND.y+CELL*0.7
            position = pygame.Vector2(FACTION_HAND.x+5+CELL*player_hand.index(crd)*0.7, ypos)
        crd.card_drawer(WIN, position)   
        crd.card_positioner() # 
    if card != None: #focus card changes size/picture - prevents false overlaping
        try: 
            player_hand[card].card_drawer(WIN)
            #print(player_hand[card].card_type)
        except: pass
        
def spells_hand_controller(scrd, spell_player_hand, current_phase): 
    
    for card in spell_player_hand: 
        #ypos = float
        #position = pygame.Vector2(0,0)
        
        ypos = SPELLS_HAND.y+CELL*0.7
        position = pygame.Vector2(SPELLS_HAND.x+5+CELL*spell_player_hand.index(card)*0.7,ypos)
        
        card.card_drawer(WIN, position)
        card.card_positioner()
    
    if scrd != None:
        try:
            spell_player_hand[scrd].card_drawer(WIN)
        except: pass
    
    pass        

def available_moves_function(available_moves):
    #print(available_moves)
    for move in available_moves:
        color = (0,127+waving_func(pygame.time.get_ticks()),0)
        #grid_move = pygame.Rect(move[0],move[1],CELL,CELL)
        pygame.draw.rect(BOARD, color, move, width=6,border_radius=10)

def available_attacks_function(available_attacks):
    
    for attack in available_attacks:
        color = (127+waving_func(pygame.time.get_ticks()), 0, 0)
        pygame.draw.rect(BOARD, color, attack, width=6,border_radius=10)
    
def pre_game(player_tokens):
    
    for token in player_tokens:
        
        
    
    
    
        pass
    


def main():   #New function
    """ Main game function
    """
    
    run = True
    clock = pygame.time.Clock()
    
    prueba = TokenObject(CELL, pos_a[0], pos_a[1], "token_1.png", "prueba1",1)
    prueba2 = TokenObject(CELL,CELL*3, CELL*4, "token_1.png", "prueba2", 1)
    prueba3 = TokenObject(CELL,CELL*3,CELL*2, "token_3.png", "prueba3",1)
    
    enemy1 = TokenObject(CELL,CELL*3, CELL*3, "token_2.png", "prueba2", 2)
    enemy2 = TokenObject(CELL,CELL*2, CELL*3, "token_2.png", "prueba2", 2)
    enemy3 = TokenObject(CELL,CELL*4, CELL*3, "token_2.png", "prueba2", 2)
    enemy4 = TokenObject(CELL,CELL*2, CELL*2, "token_2.png", "prueba2", 1)
    enemy5 = TokenObject(CELL,CELL*2, CELL*1, "token_2.png", "prueba2", 1)
    enemy6 = TokenObject(CELL,CELL*4, CELL*2, "token_2.png", "prueba2", 1)
    enemy7 = TokenObject(CELL,CELL*4, CELL*1, "token_2.png", "prueba2", 1)
    enemy8 = TokenObject(CELL,CELL*3, CELL*1, "token_2.png", "prueba2", 1)
    
    
    current_phase = GAME_SEQUENCE[1]
    
    
    new_game_preparations("INVESTIGATORS","SERPENT_PEOPLE")
    player_a = Player_Object("currentgame.db", "cards_a", "player_a")
    player_b = Player_Object("currentgame.db", "cards_b", "player_b")
    hosting_player = True
    phase = str
    movement_indicator = None  # signals movement amount
    moving_tokens = False # tokens are to be moved
    available_moves = []
    
    attack_indicator = None
    attacking_tokens = False
    available_attacks = []
    damage_in_course = 0
    
    chosen_token = None
    pos = None
    
    player_a.player_tokens.append(prueba)
    player_a.player_tokens.append(prueba2)
    player_a.player_tokens.append(prueba3) 
    
    player_b.player_tokens.append(enemy1) 
    player_b.player_tokens.append(enemy2) 
    player_b.player_tokens.append(enemy3)   
    player_b.player_tokens.append(enemy4)
    player_b.player_tokens.append(enemy5)
    player_b.player_tokens.append(enemy6)
    player_b.player_tokens.append(enemy7)
    player_b.player_tokens.append(enemy8)
    
    
    
    
    
    while run:
        
        clock.tick(FPS)
        
        surface = None
        focus_faction_card = None
        focus_spell_card = None
        initial_pos = None
        
        
        #drawn_cards = []
        mousepos = pygame.mouse.get_pos()
        
        
        ### cursor's management ###
        
        if BOARD.get_rect().collidepoint(mousepos):
            pygame.mouse.set_cursor(pygame.cursors.arrow) 
            
        if BOARD.get_rect().collidepoint(mousepos) and (movement_indicator != None or attack_indicator != None):
            
            for mov in available_moves:
                if mov.collidepoint(mousepos) and moving_tokens: # during move phase
                    pygame.mouse.set_cursor(pygame.cursors.broken_x)
            for att in available_attacks:
                if att.collidepoint(mousepos) and attacking_tokens: # during attack phase
                    pygame.mouse.set_cursor(pygame.cursors.broken_x)
            for obj in player_a.player_tokens:
            
                if obj.rec.collidepoint(mousepos): # during move phase token selection
                    pygame.mouse.set_cursor(pygame.cursors.diamond)
        else:
            pygame.mouse.set_cursor(pygame.cursors.arrow) # standard
            
        
        ### Cursor over CARDS ###
          
        for card in player_a.player_hand:
            if card.rec.collidepoint(mousepos): 
                
                card.looked_on = True
                
                focus_faction_card = player_a.player_hand.index(card)
            
            else:
                card.looked_on = False
                
        
        for scrd in player_a.player_spell_hand:
            if scrd.rec.collidepoint(mousepos):
                
                scrd.looked_on = True
                focus_spell_card = player_a.player_spell_hand.index(scrd)
            else: 
                scrd.looked_on = False
        
        ### EVENTS ####
        
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:
                run = False
            
            ### MOUSEBUTTONDOWN EVENTS ###
            
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                if button2.collidepoint(mousepos):   ### passing phases ---> test only
                        
                        if len(GAME_SEQUENCE) == GAME_SEQUENCE.index(current_phase)+1:
                            hosting_player = not hosting_player
                            
                            
                            current_phase = GAME_SEQUENCE[0]
                        else:
                            current_phase = GAME_SEQUENCE[GAME_SEQUENCE.index(current_phase)+1]
                            
                ### SPELL CARDS EVENTS ###
                            
                for scrd in player_a.player_spell_hand:
                    if scrd.rec.collidepoint(mousepos):
                        #print("spell card played")  # CONTROL
                        pass
                
                ### FATE PHASE ###
                        
                if current_phase == "fate":
                    
                    if faction_deck_drawer_button.collidepoint(mousepos):
                        player_a.fate_phase(repetitions = 3)

                ### MOVE PHASE EVENT ###
                
                if current_phase == "move":
                
                        
                    if pygame.mouse.get_cursor() == pygame.cursors.broken_x: 
                        for move in available_moves:
                            if move.collidepoint(mousepos):
                            
                                pos = (move.x, move.y)
                                #print("move to: ", pos)
                                position = pygame.Vector2(pos[0], pos[1])
                                chosen_token.vector_to_go = position
                                ### resetting values to prevent various movements over the same card ###
                                available_moves = [] 
                                pos = None
                                movement_indicator = None
                                moving_tokens = False
                                
                    elif pygame.mouse.get_cursor() == pygame.cursors.diamond:
                    
                        for token in player_a.player_tokens:
                            if moving_tokens and token.rec.collidepoint(mousepos):
                                chosen_token = token
                                
                                available_moves = available_movement_detector_linear_vector(token, movement_indicator ,player_a.player_tokens, player_b.player_tokens)
                                #print("available_moves",available_moves)
                    else:
                        for crd in player_a.player_hand:
                            if crd.rec.collidepoint(mousepos):
                                if (crd.card_type == "M" or crd.card_type == "XS" or crd.card_type == "XF"):
                                    code = crd.activate_card()
                                    discarder("cards_a", str(crd.identif))
                                    player_a.player_hand.remove(crd)
                                    
                                    movement_indicator = player_a.move_phase(code)
                                    
                                    if movement_indicator != None: moving_tokens = True
                                    #print("moving_tokens: ",moving_tokens)  # CONTROL

                
                ### ATTACK PHASE EVENT ###
                
                if current_phase == "att": 
                    
                    if pygame.mouse.get_cursor() == pygame.cursors.broken_x:
                        for attack in available_attacks:
                            if attack.collidepoint(mousepos):
                               for enemy in player_b.player_tokens:
                                   if enemy.rec.collidepoint(mousepos):
                                        ### hit the enemy
                                        enemy.hits = enemy.hits - damage_in_course
                                        
                                        ### resetting values to prevent various attacks over the same card ###
                                        available_attacks = []
                                        attack_indicator = None
                                        attacking_tokens = False
                                        damage_in_course = 0
                        
                    
                    elif pygame.mouse.get_cursor() == pygame.cursors.diamond:
                    
                        for token in player_a.player_tokens:
                            if attacking_tokens and token.rec.collidepoint(mousepos):
                                chosen_token = token
                                available_attacks = available_attacks_detector_maxrange_square(token, attack_indicator, player_a.player_tokens, player_b.player_tokens)
                                #print(available_attacks)
                                
                    
                    else:
                        for crd in player_a.player_hand:
                            if crd.rec.collidepoint(mousepos):
                                if (crd.card_type == "A"):
                                    attack_indicator = crd.activate_card()[1]
                                    discarder("cards_a", str(crd.identif))
                                    damage_in_course = card.damage
                                    player_a.player_hand.remove(crd)


                                    #player_a.attack_phase()

                                    if attack_indicator != None: attacking_tokens = True
                    
                                

                
                ### DEFENSE PHASE EVENT ###
                
                if current_phase == "def": 
                           
                    for crd in player_a.player_hand:
                        if crd.rec.collidepoint(mousepos):        

                            if current_phase == "def" and (crd.card_type == "D"):

                                crd.activate_card()
                                discarder("cards_a", str(crd.identif))
                                player_a.player_hand.remove(crd)
                                
                                player_a.defense_phase()

        # surviving tokens control
        for token_a in player_a.player_tokens:
            if token_a.hits < 1:
                player_a.player_tokens.remove(token_a)
        for token_b in player_b.player_tokens:
            if token_b.hits < 1:
                player_b.player_tokens.remove(token_b)
        
            
        
            
        draw_window(focus_faction_card, 
                    player_a.player_hand, 
                    focus_spell_card, 
                    player_a.player_spell_hand ,
                    current_phase, 
                    hosting_player, 
                    movement_indicator, 
                    available_moves,
                    available_attacks,
                    player_a.player_tokens,
                    player_b.player_tokens)
    
    pygame.quit()



if __name__=="__main__":
    
    print(GRID_DIC)
    main()
    