import pygame


import math
from multiprocessing import Process
import os

from constants import FACTIONS, ROWS, COLUMNS, GRID, FPS, BACKGROUND_COLOR, GRID_DIC, WIDTH, HEIGHT, CELL, GAME_SEQUENCE, CARD_WIDTH, BOARD, button2, no_defense_button
from constants import PRE_GAME_TOKEN_MAT, pre_game_cancel_button, pre_game_ok_button
from constants import FACTION_HAND, FACTION_DECK_POSITION, faction_deck_drawer_button
from constants import SPELLS_HAND, SPELL_DECK_POSITION, spells_deck_drawer_button
from constants import GENERIC_FONT, CARD_FONT

from gameobjects import TokenObject, CardObject
from player_turn_module import Player_Object
from dbcreator import conection_sql
from dbintermediatefunctions import card_data_extractor, discarder
from functionsmodule import movement_blocker, available_movement_detector_pathfinding, available_movement_detector_linear_vector, available_attacks_detector_fixedrange, available_attacks_detector_maxrange_square
from pregame_functions import player_token_assigner, starting_position_function

from game_network import Network

from pickleobj import Exchange_object

from game_server import main as server_main

from widgets import DropDown, Button

from server_interpreter import recv_msg_translator, send_msg_translator

#self.WIN = pygame.display.set_mode((WIDTH, HEIGHT))  

def waving_func(time):
    z = 127*math.cos((2*math.pi/(FPS*40))*time)
    return z


class Main():
    def __init__(self, faction) -> None:
        
        self.WIN = pygame.display.set_mode((WIDTH, HEIGHT))  
        self.faction = faction
        pygame.display.init()
        pygame.font.init()
        pygame.display.set_caption("TO CHANGE")
        
        
        # CONSTANTS previously placed in a different module. Hvae to 
        self.run = True
        self.clock = pygame.time.Clock()
        self.scene = "pre_game"
        self.current_phase = GAME_SEQUENCE[0]
        self.phase_passer = 2
        #new_game_preparations("INVESTIGATORS","SERPENT_PEOPLE")
        self.player_a = Player_Object("NONE")
        #self.player_a = Player_Object("INVESTIGATORS")
        self.player_b = Player_Object("NONE")
        self.player_turn = True
        self.mousepos = pygame.mouse.get_pos()
        
        
        self.movement_indicator = None  # signals movement amount
        self.moving_tokens = False # tokens are to be moved
        self.available_moves = []

        self.attack_indicator = None
        self.attacking_tokens = False
        self.available_attacks = []
        self.damage_in_course = 0
        self.damaged_token = None
        self.damage_dealt = 0
        
        self.defense_indicator = False
        
        self.chosen_token = None
        self.pos = None
        self.ocupied_cell = None
        
        self.freezing_mouse_event = pygame.USEREVENT+1
        
        
        #prueba = TokenObject(CELL, 0, 0, "token_1.png", "prueba1",1,"")
        prueba2 = TokenObject(CELL,CELL*3, CELL*4, "token_1.png", "prueba2", 1,"")
        prueba3 = TokenObject(CELL,CELL*3,CELL*2, "token_3.png", "prueba3",1,"")

        enemy1 = TokenObject(CELL,CELL*0,CELL*0, "token_2.png", "prueba2", 2,"")
        #enemy2 = TokenObject(CELL,CELL*2, CELL*3, "token_2.png", "prueba2", 2,"")
        #enemy3 = TokenObject(CELL,CELL*4, CELL*3, "token_2.png", "prueba2", 2,"")
        #enemy4 = TokenObject(CELL,CELL*2, CELL*2, "token_2.png", "prueba2", 1,"")
        #enemy5 = TokenObject(CELL,CELL*2, CELL*1, "token_2.png", "prueba2", 1,"")
        #enemy6 = TokenObject(CELL,CELL*4, CELL*2, "token_2.png", "prueba2", 1,"")
        #enemy7 = TokenObject(CELL,CELL*4, CELL*1, "token_2.png", "prueba2", 1,"")
        #enemy8 = TokenObject(CELL,CELL*3, CELL*1, "token_2.png", "prueba2", 1,"")
        
         
        
        phase = str
        

        #self.player_a.player_tokens.append(prueba)
        #self.player_a.player_tokens.append(prueba2)
        #self.player_a.player_tokens.append(prueba3) 

        #self.player_b.player_tokens.append(enemy1) 
        #self.player_b.player_tokens.append(enemy2) 
        #self.player_b.player_tokens.append(enemy3)   
        #self.player_b.player_tokens.append(enemy4)
        #self.player_b.player_tokens.append(enemy5)
        #self.player_b.player_tokens.append(enemy6)
        #self.player_b.player_tokens.append(enemy7)
        #self.player_b.player_tokens.append(enemy8)
        self.scene = "client_test"
        
        if self.scene == "pre_game":
            self.player_a.player_tokens = []   # testing pre-game
            self.player_b.player_tokens = []
        if self.scene == "pre_game" or self.scene == "client_test":
            #self.player_a.player_tokens = []   # testing pre-game
            #self.player_b.player_tokens = []
            #self.player_a.token_list_loader()
            #print(self.player_a.player_tokens)
            if self.scene == "pre_game":
                self.pregame_mat_assigner()
        
        if self.scene == "client_test":pass
        # Network Objects
        
        self.net = Network()  
        
        self.server = Process(target = server_main)
            #self.net = Network()
            #self.net.connect(self.faction)
            
        # Exchange objects
        
        self.player_a_exchange = Exchange_object("player_a")
        self.player_b_exchange = Exchange_object("player_b")
        
        # Main Menu Objects
        self.faction_dropdown = DropDown(["white", "grey"], ["green", "blue"], CELL*6, CELL*5, CELL*3, CELL, GENERIC_FONT, "Select Faction", FACTIONS)
        self.faction_chosen_button = Button(CELL*6, CELL*2, CELL*3, CELL,GENERIC_FONT, "continue","gray", lambda: self.dummy_method() )
        self.host_button = Button(CELL*6, CELL*4, CELL*3, CELL,GENERIC_FONT, "HOST", "red",lambda: self.host_game_method() )
        self.join_button = Button(CELL*6, CELL*6, CELL*3, CELL,GENERIC_FONT, "JOIN", "white", lambda: self.to_second_menu() )
    
    
        
    def main(self):
        
        #run = True
        #clock = pygame.time.Clock()
        self.mousepos = pygame.mouse.get_pos()
        
        
        self.scene = "client_test"
        #self.player_a.token_list_loader()
        self.scene = "first_menu"
        
        while self.run:
            
            if self.scene == "first_menu":
                self.main_menu()
            elif self.scene == "second_menu":
                self.main_menu()
            elif self.scene == "pre_game":
                self.pre_game()
            elif self.scene == "in_course":
                self.in_course()
            elif self.scene == "client_test":
                self.client_testing()
            elif self.scene == "wait_enemy":
                self.waiting_enemy()
                
            #self.pre_game()
            #self.client_testing()
            """if self.scene == "pre_game":
                self.pre_game()
            elif self.scene == "in_course":
                self.in_course()    
            elif self.scene == "client_test"  :
                self.client_testing()      """
            
        pygame.quit()
    
    ### MAIN MANEU BLOCK ###
    
    
    
    def main_menu(self):
        
        self.clock.tick(FPS)
        
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                try:
                    self.net.send("!DISCONNECT")
                    self.server.terminate()
                except: pass
                
                self.run = False
            if self.scene == "first_menu":
                self.host_button.update(events)
                self.join_button.update(events)
            elif self.scene == "second_menu":
                selected_faction = self.faction_dropdown.update(events)
                
                if selected_faction >= 0:
                    self.faction_dropdown.main = self.faction_dropdown.options[selected_faction]
                    self.faction_chosen_button.action = lambda: self.faction_selector(self.faction_dropdown.main)
                self.faction_chosen_button.update(events)
        
        self.menu_draw()
        
        
    
    def host_game_method(self):
        os.system("cls")
        self.server.start()
        self.to_second_menu()
        
    def to_second_menu(self):
        self.scene = "second_menu"
    
    def faction_selector(self, selection):
        self.faction = selection
        print(self.faction)
        self.player_a.player_faction = self.faction
        self.player_a.general_list_loader()
        self.player_a.token_list_loader()
        enemy_faction = self.net.connect(self.faction)
        if enemy_faction == "NONE":
            print("waiting enemy")
            self.scene = "wait_enemy"
        else: 
            
            self.player_b.player_faction = enemy_faction
            self.player_b.general_list_loader()
            self.player_b.token_list_loader()  
            print("enemy: ",self.player_b)
            self.scene = "client_test"
            
        
        
    def dummy_method(self):
        pass
        
    
    def menu_draw(self):
        
        phase_informer = "pre-game"
    
        """if self.player:
            phase_informer = "a_"+self.current_phase
        else: phase_informer = "b_"+self.current_phase"""
        
        self.WIN.fill(BACKGROUND_COLOR)
        if self.scene == "first_menu":
            self.host_button.draw(self.WIN)
            self.join_button.draw(self.WIN)
        elif self.scene == "second_menu":
            self.faction_dropdown.draw(self.WIN)
            self.faction_chosen_button.draw(self.WIN)
        
        pygame.display.update()
    
    def waiting_enemy(self):
        
        self.clock.tick(FPS)
        
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                try:
                    self.net.send("!DISCONNECT")
                    self.server.terminate()
                except: pass
                
                self.run = False
        
        response = self.net.send_recv(self.player_a.player_faction)
        
        if response != "NONE":
            self.player_b.player_faction = response
            print("enemy faction:",self.player_b.player_faction)
            self.player_b.general_list_loader()
            self.player_b.token_list_loader()
            self.scene = "client_test"
        else: pass 
            
        
        
        self.WIN.fill(BACKGROUND_COLOR)
        
        phase_informer = "Waiting Enemy to Connect"
        current_phase_informer = GENERIC_FONT.render(phase_informer, 1, "red")
        self.WIN.blit(current_phase_informer, (CELL*10, 20))
#
       
        
        pygame.display.update()
        
        
            
        
        
        
          
            
        
        
    def client_testing(self):
        bucle = 0
        
        self.clock.tick(FPS)
        self.mousepos = pygame.mouse.get_pos()
        
        tosend = "NONE"
        enemy_pos = "NONE"
                
        phase_informer = "testing server"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                try:
                    self.net.send_recv("!DISCONNECT")
                    self.server.terminate()
                except: pass
                
                self.run = False
                
        
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                if no_defense_button.collidepoint(self.mousepos):
                    var = 0
                    available_test = [(x,y) for x in range (8) for y in range(6, 8)]
                    for token in self.player_a.player_tokens:
                        token.vector_to_go = pygame.Vector2(available_test[var][0]*CELL, available_test[var][1]*CELL)
                        var += 1
                    print("vector_to_go[0]: ",self.player_a.player_tokens[0].vector_to_go[0])
                    print(str(self.player_a.player_tokens[0].vector_to_go[0]))
                    vector_to_go0 = str(self.player_a.player_tokens[0].vector_to_go[0])
                    vector_to_go1 = str(self.player_a.player_tokens[0].vector_to_go[1])
                    tosend = "VECTORTOGO]"+str(self.player_a.player_tokens[0])+":"+vector_to_go0+","+vector_to_go1
                    #tosend = vector_to_go0+":"+vector_to_go1
                    print(tosend)
                    
        try:
            
            enemy_pos = self.net.send_recv(tosend)
            if enemy_pos != "NONE":
                
                separator = enemy_pos.index(":")
                xpos = float(enemy_pos[:separator])
                ypos = float(enemy_pos[separator+1:])
                self.player_b.player_tokens[0].vector_to_go[:] = xpos, ypos
        
        except:
            print("problems in enemy_pos")
        
            
            
        
        self.WIN.fill(BACKGROUND_COLOR)
        BOARD.fill("tan4")

        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(BOARD, "grey3",(CELL*row, CELL*col, CELL,CELL))
        
        self.player_a.player_tokens[0].token_object_drawer(BOARD)
        self.player_b.player_tokens[0].token_object_drawer(BOARD, turner = True)
               
        self.WIN.blit(BOARD,(0,0))    # actualizes BOARD -> always after all changes of it

        pygame.draw.rect(self.WIN, "red", no_defense_button)
        
        

        current_phase_informer = GENERIC_FONT.render(phase_informer, 1, "red")
        self.WIN.blit(current_phase_informer, (CELL*10, 20))

       
        
        pygame.display.update()   
        
 
    def pre_game(self):
        
        self.clock.tick(FPS)
        self.mousepos = pygame.mouse.get_pos()
        self.scene = "pre_game"
        
        self.movement_indicator = 1
                
        self.available_moves = starting_position_function(self.player_a.player_tokens)
        if self.ocupied_cell != None:   # overlapping tokens prevention
            try:
                self.available_moves.remove(self.ocupied_cell)
            except:
                self.ocupied_cell = None
        
        
            
        if BOARD.get_rect().collidepoint(self.mousepos):
            pygame.mouse.set_cursor(pygame.cursors.arrow) 
        
        if BOARD.get_rect().collidepoint(self.mousepos):
            
            for mov in self.available_moves:
                if mov.collidepoint(self.mousepos) and self.moving_tokens: # during move phase
                    pygame.mouse.set_cursor(pygame.cursors.broken_x)
               
        
            for obj in self.player_a.player_tokens:
            
                if obj.rec.collidepoint(self.mousepos): # during move phase token selection
                    pygame.mouse.set_cursor(pygame.cursors.diamond) 
            
            if pre_game_cancel_button.collidepoint(self.mousepos) or pre_game_ok_button.collidepoint(self.mousepos):
                
                pygame.mouse.set_cursor(pygame.cursors.tri_left)
                
        
        else:
            pygame.mouse.set_cursor(pygame.cursors.arrow) # standard        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                try:
                    self.net.send("!DISCONNECT")
                    self.server.terminate()
                except: pass
                self.run = False
        
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                if pre_game_cancel_button.collidepoint(self.mousepos): # cancel initial placement
                    self.pregame_mat_assigner()
                    self.moving_tokens = False
                    self.chosen_token = None
                
                if pre_game_ok_button.collidepoint(self.mousepos) and len(self.available_moves) == 0:
                    print("next scene")
                    self.scene = "in_course"
                
                if pygame.mouse.get_cursor() == pygame.cursors.diamond:
                    for token in self.player_a.player_tokens:
                        if token.rec.collidepoint(self.mousepos):
                            self.chosen_token = token

                            self.moving_tokens = True
                
                if pygame.mouse.get_cursor() == pygame.cursors.broken_x:
                    
                    for move in self.available_moves:
                        if move.collidepoint(self.mousepos):
                        
                            self.pos = (move.x, move.y)
                            #print("move to: ", self.pos)
                            self.position = pygame.Vector2(self.pos[0], self.pos[1])
                            self.chosen_token.vector_to_go = self.position
                            ### resetting values to prevent various movements over the same card ###
                            self.pos = None
                            self.moving_tokens = False
                            self.chosen_token = None
                            self.ocupied_cell = move
                
        if self.scene == "pre_game":
            self.draw_window_pregame()
        else: 
            pass
        
    
    def draw_window_pregame(self):   
        
        phase_informer = "pre-game"
    
        """if self.player:
            phase_informer = "a_"+self.current_phase
        else: phase_informer = "b_"+self.current_phase"""
        
        self.WIN.fill(BACKGROUND_COLOR)
        BOARD.fill("tan4")

        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(BOARD, "grey3",(CELL*row, CELL*col, CELL,CELL))
                
        pygame.draw.rect(BOARD,"green", PRE_GAME_TOKEN_MAT) 
        
        
        
        locate_token_text = GENERIC_FONT.render("Place the tokens in the avilable positions", 1, "red")
        BOARD.blit(locate_token_text,(CELL, CELL//4))
        
        pygame.draw.rect(BOARD, "red", pre_game_cancel_button)
        if len(self.available_moves) == 0:
            pygame.draw.rect(BOARD, "darkgreen", pre_game_ok_button)
        """else: 
            pygame.draw.rect(BOARD, "darkgreen", pre_game_ok_button)"""
        self.starting_positions()
        self.selected_token()
        self.token_movement("pre_game")
         
               
        self.WIN.blit(BOARD,(0,0))    # actualizes BOARD -> always after all changes of it

        
        
#
        current_phase_informer = GENERIC_FONT.render(phase_informer, 1, "red")
        self.WIN.blit(current_phase_informer, (CELL*10, 20))
#
       
        
        pygame.display.update()
             
            
    def in_course(self):
        
        self.clock.tick(FPS)
        self.mousepos = pygame.mouse.get_pos()
        focus_faction_card = None
        focus_spell_card = None
        
        # Network 
        
        #self.p2 = self.net.send(self.p)
        
        ### cursor's management ###
        
        if BOARD.get_rect().collidepoint(self.mousepos):
            pygame.mouse.set_cursor(pygame.cursors.arrow) 

        if BOARD.get_rect().collidepoint(self.mousepos) and (self.movement_indicator != None or self.attack_indicator != None):

            for mov in self.available_moves:
                if mov.collidepoint(self.mousepos) and self.moving_tokens: # during move phase
                    pygame.mouse.set_cursor(pygame.cursors.broken_x)
            for att in self.available_attacks:
                if att.collidepoint(self.mousepos) and self.attacking_tokens: # during attack phase
                    pygame.mouse.set_cursor(pygame.cursors.broken_x)
            for obj in self.player_a.player_tokens:
            
                if obj.rec.collidepoint(self.mousepos): # during move phase token selection
                    pygame.mouse.set_cursor(pygame.cursors.diamond)
        else:
            pygame.mouse.set_cursor(pygame.cursors.arrow) # standard


        ### Cursor over CARDS ###

        for card in self.player_a.player_hand_objs:
            if card.rec.collidepoint(self.mousepos): 

                card.looked_on = True

                focus_faction_card = self.player_a.player_hand_objs.index(card)

            else:
                card.looked_on = False


        for scrd in self.player_a.player_spell_hand_objs:
            if scrd.rec.collidepoint(self.mousepos):

                scrd.looked_on = True
                focus_spell_card = self.player_a.player_spell_hand_objs.index(scrd)
            else: 
                scrd.looked_on = False

        ### EVENTS ####

        for event in pygame.event.get():  
            if event.type == pygame.QUIT:
                self.run = False

            if event.type== self.freezing_mouse_event:
                
                self.phase_passer_method()
                
            ### MOUSEBUTTONDOWN EVENTS ###

            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                if button2.collidepoint(self.mousepos):   ### passing phases ---> test only
                    
                    self.phase_passer_method()
                    
                
                if self.player_turn:

                    ### SPELL CARDS EVENTS ###
    
                    for scrd in self.player_a.player_spell_hand_objs:
                        if scrd.rec.collidepoint(self.mousepos):
                            #print("spell card played")  # CONTROL
                            pass
                        
                    ### FATE PHASE ###
    
                    if self.current_phase == "fate":
                    
                        if faction_deck_drawer_button.collidepoint(self.mousepos):
                            
                            self.player_a.fate_phase(repetitions = 3)
                            pygame.time.set_timer(self.freezing_mouse_event, 1000, 1) # prevents hitting the cards when draself.WINg
                            
                            #self.phase_passer_method()
    
                    ### MOVE PHASE EVENT ###
    
                    if self.current_phase == "move":
                    
                    
                        if pygame.mouse.get_cursor() == pygame.cursors.broken_x: 
                            for move in self.available_moves:
                                if move.collidepoint(self.mousepos):
                                
                                    self.pos = (move.x, move.y)
                                    #print("move to: ", self.pos)
                                    self.position = pygame.Vector2(self.pos[0], self.pos[1])
                                    self.chosen_token.vector_to_go = self.position
                                    ### resetting values to prevent various movements over the same card ###
                                    self.available_moves = [] 
                                    self.pos = None
                                    self.movement_indicator = None
                                    self.moving_tokens = False
                                    pygame.time.set_timer(self.freezing_mouse_event, 1000, 1)
                                    #self.phase_passer_method()
                                    
    
                        elif pygame.mouse.get_cursor() == pygame.cursors.diamond:
                        
                            for token in self.player_a.player_tokens:
                                if self.moving_tokens and token.rec.collidepoint(self.mousepos):
                                    self.chosen_token = token
    
                                    self.available_moves = available_movement_detector_linear_vector(token, self.movement_indicator ,self.player_a.player_tokens, self.player_b.player_tokens)
                                    #print("self.available_moves",self.available_moves)
                        else:
                            for crd in self.player_a.player_hand_objs:
                                if crd.rec.collidepoint(self.mousepos):
                                    if (crd.card_type == "M" or crd.card_type == "XS" or crd.card_type == "XF"):
                                        code = crd.activate_card()
                                        #discarder("cards_a", str(crd.identif))
                                        
                                        self.player_a.faction_card_discard(crd)
                                        #self.player_a.player_hand_objs.remove(crd)
    
                                        self.movement_indicator = self.player_a.move_phase(code)
    
                                        if self.movement_indicator != None: self.moving_tokens = True
                                        #print("self.moving_tokens: ",self.moving_tokens)  # CONTROL
    
                            for crd in self.player_a.player_spell_hand_objs:
                                if crd.rec.collidepoint(self.mousepos):
                                    self.player_a.spell_card_discard(crd)
    
                    ### ATTACK PHASE EVENT ###
    
                    if self.current_phase == "att": 
                    
                        if pygame.mouse.get_cursor() == pygame.cursors.broken_x:
                            for attack in self.available_attacks:
                                if attack.collidepoint(self.mousepos):
                                   for enemy in self.player_b.player_tokens:
                                       if enemy.rec.collidepoint(self.mousepos):
                                            ### hit the enemy
                                            self.damaged_token = self.player_b.player_tokens.index(enemy) # to use
                                            
                                            #self.damage_dealt = self.damage_in_course
                                            #enemy.hits = enemy.hits - self.damage_in_course
    
                                            ### resetting values to prevent various attacks over the same card ###
                                            self.available_attacks = []
                                            self.attack_indicator = None
                                            self.attacking_tokens = False
                                            self.defense_indicator = True
                                            self.player_b.player_tokens[self.damaged_token].hits = self.player_b.player_tokens[self.damaged_token].hits - self.damage_in_course
                                            self.damage_in_course = 0
                                            #self.current_phase = "def"
                                            #pygame.time.wait(10000)
                                            pygame.time.set_timer(self.freezing_mouse_event, 1000, 1)
                                            #self.phase_passer_method()
                        
                                            
    
    
                        elif pygame.mouse.get_cursor() == pygame.cursors.diamond:
                        
                            for token in self.player_a.player_tokens:
                                if self.attacking_tokens and token.rec.collidepoint(self.mousepos):
                                    self.chosen_token = token
                                    self.available_attacks = available_attacks_detector_maxrange_square(token, self.attack_indicator, self.player_a.player_tokens, self.player_b.player_tokens)
                                    #print(self.available_attacks)
    
    
                        else:
                            for crd in self.player_a.player_hand_objs:
                                if crd.rec.collidepoint(self.mousepos):
                                    if (crd.card_type == "A"):
                                        self.attack_indicator = crd.activate_card()[1]
                                        self.player_a.faction_card_discard(crd)
                                        #discarder("cards_a", str(crd.identif))
                                        self.damage_in_course = card.damage
                                        #self.player_a.player_hand_objs.remove(crd)
    
    
                                        #self.player_a.attack_phase()
    
                                        if self.attack_indicator != None: 
                                            self.attacking_tokens = True
                                            
    
    
    
    
                    ### DEFENSE PHASE EVENT ###
                    #if self.defense_indicator:
                    if self.current_phase == "def" and self.damaged_token != None: # test function
                        pass
                        #self.player_turn = False
                        """for crd in self.player_a.player_hand_objs:
                            if crd.rec.collidepoint(self.mousepos):        
                            
                                if crd.card_type == "D":
                                    
                                    crd.activate_card()
                                    self.damage_in_course = 0
                                    self.damaged_token = None
                                    self.player_a.faction_card_discard(crd)
                                    self.player_turn = True
                                    self.defense_indicator = False
                                    #discarder("cards_a", str(crd.identif))
                                    #self.player_a.player_hand_objs.remove(crd)
                                    
                        if no_defense_button.collidepoint(self.mousepos):
                            
                            self.player_b.player_tokens[self.damaged_token].hits = self.player_b.player_tokens[self.damaged_token].hits - self.damage_in_course
                            self.damage_in_course = 0
                            self.damaged_token = None
                            self.player_turn = True
                            self.defense_indicator = False"""
                        
                                
                
        # surviving tokens control
        
        for token_a in self.player_a.player_tokens:
            if token_a.hits < 1:
                self.player_a.player_tokens.remove(token_a)
        for token_b in self.player_b.player_tokens:
            if token_b.hits < 1:
                self.player_b.player_tokens.remove(token_b)




        self.draw_window(focus_faction_card, focus_spell_card, "in_course")
    
         
        
    def draw_window(self, focus_faction_card, focus_spell_card, game_status_indicator):
        
        phase_informer = str
    
        if self.player_turn:
            phase_informer = "Your trun: "+self.current_phase
        else: phase_informer = "Enemy's turn"+self.current_phase

        self.WIN.fill(BACKGROUND_COLOR)
        BOARD.fill("tan4")

        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(BOARD, "grey3",(CELL*row, CELL*col, CELL,CELL))
    
        
        self.available_moves_method()   
        self.token_movement("in_course")
        self.available_attacks_method()
        


        self.WIN.blit(BOARD,(0,0))    # actualizes BOARD -> always after all changes of it

        pygame.draw.rect(self.WIN, "pink",FACTION_HAND)
        pygame.draw.rect(self.WIN, "red",SPELLS_HAND)


        faction_deck = pygame.image.load(os.path.join("images","faction_deck2.jpg")).convert_alpha() # load faction deck image
        faction_deck_scaled_image = pygame.transform.scale(faction_deck, (faction_deck_drawer_button.width, faction_deck_drawer_button.height))
        self.WIN.blit(faction_deck_scaled_image, (faction_deck_drawer_button))

        pygame.draw.rect(self.WIN, "white", button2)
        pygame.draw.rect(self.WIN, "red", no_defense_button)

        spells_deck = pygame.image.load(os.path.join("images","spells_deck_scaled.jpg")).convert_alpha() # load spells deck image
        spells_deck_scaled_image = pygame.transform.scale(spells_deck,(spells_deck_drawer_button.width, spells_deck_drawer_button.height))
        self.WIN.blit(spells_deck_scaled_image, (spells_deck_drawer_button))

        current_phase_informer = GENERIC_FONT.render(phase_informer, 1, "red")
        self.WIN.blit(current_phase_informer, (CELL*10, 20))

        faction_hand_sign = GENERIC_FONT.render("Faction Hand", 1, "black")
        self.WIN.blit(faction_hand_sign,(FACTION_HAND.x+5,FACTION_HAND.y))

        spells_hand_sign = GENERIC_FONT.render("Spells hand",1,"black")
        self.WIN.blit(spells_hand_sign, (SPELLS_HAND.x+5,SPELLS_HAND.y))
        
        
            
        self.faction_hand_controller(focus_faction_card, self.current_phase)
        self.spells_hand_controller(focus_spell_card, self.current_phase)





        pygame.display.update()
    
    def selected_token(self):
        if self.chosen_token != None:
            color = (127+waving_func(pygame.time.get_ticks()),127+waving_func(pygame.time.get_ticks()),127+waving_func(pygame.time.get_ticks()))
            pygame.draw.rect(BOARD, color, self.chosen_token.rec, width=6,border_radius=10)
            #print(self.chosen_token)
    
    
    def token_movement(self, game_secene):
    

        for obj in self.player_a.player_tokens:
            obj.token_object_drawer(BOARD)
        if game_secene == "in_course" or game_secene == "client_test":
            
            for obj2 in self.player_b.player_tokens:
                
                obj2.token_object_drawer(BOARD, turner = True) 
                
                  
    
    def available_moves_method(self):
        #print(available_moves)
        for move in self.available_moves:
            color = (0,127+waving_func(pygame.time.get_ticks()),0)
            #grid_move = pygame.Rect(move[0],move[1],CELL,CELL)
            pygame.draw.rect(BOARD, color, move, width=6,border_radius=10)

    def available_attacks_method(self):
    
        for attack in self.available_attacks:
            color = (127+waving_func(pygame.time.get_ticks()), 0, 0)
            pygame.draw.rect(BOARD, color, attack, width=6,border_radius=10)
            
    def pregame_mat_assigner(self):
        
        pregame_positions = [(x,y) for x in range(8) for y in range(2)]
        count = 0
        for token in self.player_a.player_tokens:
            vector2 = pygame.Vector2(pregame_positions[count][0]*CELL, pregame_positions[count][1]*CELL+2*CELL)
            token.vector_to_go = vector2
            count += 1
       
    def starting_positions(self):
        
        
        #positions_slots = starting_position_function(self.player_a.player_tokens)
        for pos_slot in self.available_moves:
            
            color = (0,127+waving_func(pygame.time.get_ticks()),0)
            pygame.draw.rect(BOARD, color, pos_slot, width=6,border_radius=10)

    
            
    def faction_hand_controller(self, card,  current_phase):
    
            
        for crd in self.player_a.player_hand_objs:  # positions cardobject

            ypos = float
            position = pygame.Vector2(0,0)
            #crd.rec.x = FACTION_HAND.x+5+CELL*player_hand.index(crd)*0.7 # assigns position to the object in the hand
            #crd.rec.y = FACTION_HAND.y+CELL*0.7

            if current_phase == "move" and (crd.card_type == "M" or crd.card_type == "XS" or crd.card_type == "XF"):
                ypos = FACTION_HAND.y+CELL*0.3
                position = pygame.Vector2(FACTION_HAND.x+5+CELL*self.player_a.player_hand_objs.index(crd)*0.7, ypos)
                #crd.card_drawer(self.WIN,pygame.Vector2(FACTION_HAND.x+5+CELL*player_hand.index(crd)*0.7, ypos))

            elif current_phase == "att" and (crd.card_type == "A"):
                ypos = FACTION_HAND.y+CELL*0.3
                position = pygame.Vector2(FACTION_HAND.x+5+CELL*self.player_a.player_hand_objs.index(crd)*0.7, ypos)

                #crd.card_drawer(self.WIN, position)  
            elif current_phase == "def" and (crd.card_type == "D"):
                ypos = FACTION_HAND.y+CELL*0.3
                position = pygame.Vector2(FACTION_HAND.x+5+CELL*self.player_a.player_hand_objs.index(crd)*0.7, ypos)

                #crd.card_drawer(self.WIN, position)  
            elif current_phase == "fate":
                ypos = FACTION_HAND.y+CELL*0.7
                position = pygame.Vector2(FACTION_HAND.x+5+CELL*self.player_a.player_hand_objs.index(crd)*0.7, ypos)
            else:
                ypos = FACTION_HAND.y+CELL*0.7
                position = pygame.Vector2(FACTION_HAND.x+5+CELL*self.player_a.player_hand_objs.index(crd)*0.7, ypos)
            crd.card_drawer(self.WIN, position)   
            crd.card_positioner() # 
        if card != None: #focus card changes size/picture - prevents false overlaping
            try: 
                self.player_a.player_hand_objs[card].card_drawer(self.WIN)
                #print(player_hand[card].card_type)
            except: pass
            
    def spells_hand_controller(self, scrd,  current_phase): 
    
        for card in self.player_a.player_spell_hand_objs: 
            #ypos = float
            #position = pygame.Vector2(0,0)

            ypos = SPELLS_HAND.y+CELL*0.7
            position = pygame.Vector2(SPELLS_HAND.x+5+CELL*self.player_a.player_spell_hand_objs.index(card)*0.7,ypos)

            card.card_drawer(self.WIN, position)
            card.card_positioner()

        if scrd != None:
            try:
                self.player_a.player_spell_hand_objs[scrd].card_drawer(self.WIN)
            except: pass
    
    def phase_passer_method(self):
        
        
        if len(GAME_SEQUENCE) == GAME_SEQUENCE.index(self.current_phase)+1:
            
            
            self.player_turn = not self.player_turn
            self.current_phase = GAME_SEQUENCE[0]
        else:
            
            self.current_phase = GAME_SEQUENCE[GAME_SEQUENCE.index(self.current_phase)+1]

def main_menu(window):
    
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.init()
    pygame.font.init()
    pygame.display.set_caption("TO CHANGE")
    
    mousepos = pygame.mouse.get_pos()
    clock = pygame.time.Clock()
    run = True
    
    
    
    
    
    
    pass 

def main_menu(window):
    pass
    


def main():
    """server = Process(target = server_main)
    server.start()"""
    M = Main("NONE")
    M.main()
    
    


if __name__=="__main__":
    
    main()
    
    #M = Main()
    #M.main()