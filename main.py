import pygame

import math

import os

from constants import FACTIONS, ROWS, COLUMNS, GRID, FPS, BACKGROUND_COLOR, GRID_DIC, WIDTH, HEIGHT, CELL, GAME_SEQUENCE, CARD_WIDTH, FACTION_HAND, SPELLS_HAND, FACTION_DECK_POSITION, SPELL_DECK_POSITION
from gameobjects import TokenObject, CardObject
from player_turn_module import new_game_preparations, fate_phase, move_phase, Player_Object
from dbcreator import conection_sql
from dbintermediatefunctions import card_data_extractor, discarder



class Main():
    def __init__(self) -> None:
        
        pygame.display.init()
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("TO CHANGE")
        
    def main(self):
        
        run = True
        clock = pygame.time.Clock()
        #pygame.draw.rect(WIN, "pink",FACTION_HAND)
        #pygame.draw.rect(WIN, "pink",SPELLS_HAND)
        prueba = TokenObject(CELL, pos_a[0], pos_a[1], "token_1.png", "prueba1")
        prueba2 = TokenObject(CELL,CELL*3, 0, "token_2.png", "prueba2")
        prueba3 = TokenObject(CELL,CELL*3,CELL*4, "token_3.png", "prueba3")
        #pruebacard1 = CardObject(CELL, FACTION_HAND.x+5, FACTION_HAND.y+CELL*0.3, "LiK7BK9ia.jpeg", "pruebacard1" )
        #pruebacard2 = CardObject(CELL, FACTION_HAND.x+5+CELL, FACTION_HAND.y+CELL*0.3, "McLLez6ki.jpeg", "pruebacard2" )
        
        game_objects_list.append(prueba)
        game_objects_list.append(prueba2)
        game_objects_list.append(prueba3)
        
        resolution_info = pygame.display.Info()
        print(resolution_info.current_h)
        print(str(game_objects_list))
        print(prueba)
        
        
        
        current_phase = GAME_SEQUENCE[1]
        
        
        new_game_preparations("INVESTIGATORS","SERPENT_PEOPLE")
        player_a = Player_Object("currentgame.db", "cards_a", "player_a")
        player_b = Player_Object("currentgame.db", "cards_b", "player_b")
        hosting_player = True
        phase = str
        movement_indicator = None
        
        player_a.player_tokens.append(prueba)
        player_a.player_tokens.append(prueba2)
        player_a.player_tokens.append(prueba3)    
        
        while run:
            
            clock.tick(FPS)
            pos = None
            surface = None
            chosen_token = None
            focus_faction_card = None
            focus_spell_card = None
            
            #drawn_cards = []
            mousepos = pygame.mouse.get_pos()
            
                        
            if BOARD.get_rect().collidepoint(mousepos):
                surface = "board"
                #surface = "board"
                pygame.mouse.set_cursor(pygame.cursors.diamond)
                for obj in player_a.player_tokens:
                    
                    if obj.rec.collidepoint(pygame.mouse.get_pos()):
                        pygame.mouse.set_cursor(pygame.cursors.broken_x)
                        
            else:
                pygame.mouse.set_cursor(pygame.cursors.arrow) 
                
                    #pygame.mouse.set_cursor(pygame.cursors.arrow)
            
            for card in player_a.player_hand:
                if card.rec.collidepoint(mousepos): 
                    
                    card.looked_on = True
                    #card.card_drawer(WIN)
                    focus_faction_card = player_a.player_hand.index(card)
                    
                    #print(focus_faction_card)
                    #if card.looked_on: print("card collide",card.looked_on)
                else:
                    card.looked_on = False
                    #card.card_drawer(WIN)
                    
                    #print("card collide, height: ",card.rec.height)
                #else: card.card_drawer(WIN)
            
            for scrd in player_a.player_spell_hand:
                if scrd.rec.collidepoint(mousepos):
                    
                    scrd.looked_on = True
                    focus_spell_card = player_a.player_spell_hand.index(scrd)
                else: 
                    scrd.looked_on = False
                    
            
            for event in pygame.event.get():  
                if event.type == pygame.QUIT:
                    run = False
                    
                
                    
                if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                    
                    
                    if pygame.mouse.get_cursor()==pygame.cursors.diamond:
                        pos = pygame.mouse.get_pos()
                        print("board ", pos)
                    elif pygame.mouse.get_cursor()==pygame.cursors.broken_x:
                        pos = pygame.mouse.get_pos()
                        print("image pressed")
                        for obj in player_a.player_tokens:
                            if obj.rec.collidepoint(mousepos):
                                print(obj)
                                chosen_token = obj
                                print(type(chosen_token))
                            #else: chosen_token = None
                    else: 
                        if button2.collidepoint(mousepos):
                            print(current_phase)
                            if len(GAME_SEQUENCE) == GAME_SEQUENCE.index(current_phase)+1:
                                hosting_player = not hosting_player
                                print(hosting_player)
                                
                                current_phase = GAME_SEQUENCE[0]
                            else:
                                current_phase = GAME_SEQUENCE[GAME_SEQUENCE.index(current_phase)+1]
                            
                            """if hosting_player:
                                phase = "a_"+current_phase
                            else: phase = "b_"+current_phase"""
                        elif faction_deck_drawer_button.collidepoint(mousepos):
                            if current_phase == "fate":
                                print("draw")
                                player_a.fate_phase(repetitions = 3)
                            
                            #drawn_cards = card_data_extractor("cards_a", "hand")
                        
                        else:
                            for crd in player_a.player_hand:
                                if crd.rec.collidepoint(mousepos):
                                    if current_phase == "move" and (crd.card_type == "M" or crd.card_type == "XS" or crd.card_type == "XF"):
                                        code = crd.activate_card()
                                        discarder("cards_a", str(crd.identif))
                                        player_a.player_hand.remove(crd)
                                        #drawn_cards = card_data_extractor("cards_a", "hand")
                                        movement_indicator = player_a.move_phase(code, SPELL_DECK_POSITION[0], SPELL_DECK_POSITION[1])
                                    elif current_phase == "att" and (crd.card_type == "A"):
                                        crd.activate_card()
                                        discarder("cards_a", str(crd.identif))
                                        player_a.player_hand.remove(crd)
                                        #drawn_cards = card_data_extractor("cards_a", "hand")
                                        player_a.attack_phase()
                                    elif current_phase == "def" and (crd.card_type == "D"):
                                        crd.activate_card()
                                        discarder("cards_a", str(crd.identif))
                                        player_a.player_hand.remove(crd)
                                        #drawn_cards = card_data_extractor("cards_a", "hand")
                                        player_a.defense_phase()
                            for scrd in player_a.player_spell_hand:
                                if scrd.rec.collidepoint(mousepos):
                                    print("spell card played")
            chosen_token = player_a.player_tokens[2]
                
                #if event.type == pygame.Mo
            #game_mechanics(pos)           

        pygame.quit()

if __name__=="__main__":
    
    
    M = Main()
    M.main()