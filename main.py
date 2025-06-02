import pygame


import math
from multiprocessing import Process
import os

from constants import FACTIONS, ROWS, COLUMNS, GRID, FPS, BACKGROUND_COLOR, GRID_DIC, WIDTH, HEIGHT, CELL, GAME_SEQUENCE, CARD_WIDTH, BOARD, button2, no_defense_button, temporal_change_turn_button
from constants import PRE_GAME_TOKEN_MAT, pre_game_cancel_button, pre_game_ok_button
from constants import FACTION_HAND, FACTION_DECK_POSITION, faction_deck_drawer_button
from constants import SPELLS_HAND, SPELL_DECK_POSITION, spells_deck_drawer_button
from constants import GENERIC_FONT, CARD_FONT, PHASE_INFORMER_RECT
from constants import ENEMY_FACTION_HAND, ENEMY_SPELLS_HAND

from gameobjects import TokenObject, CardObject
from player_turn_module import Player_Object
from dbcreator import conection_sql
from dbintermediatefunctions import card_data_extractor, discarder
from functionsmodule import movement_blocker, available_movement_detector_pathfinding, available_movement_detector_linear_vector, available_attacks_detector_fixedrange, available_attacks_detector_maxrange_square
from pregame_functions import player_token_assigner, starting_position_function

from game_network import Network

from pickleobj import Exchange_object

from game_server_log import main as server_main

from widgets import DropDown, Button

from server_interpreter import recv_msg_translator, send_msg_translator, send_msg_translator_with_log

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
        self.player_is_hosting = False
        self.enemy_ready = False
        self.player_ready = False
        #new_game_preparations("INVESTIGATORS","SERPENT_PEOPLE")
        self.player_a = Player_Object("NONE")
        #self.player_a = Player_Object("INVESTIGATORS")
        self.player_b = Player_Object("NONE")
        self.player_turn = True
        self.mousepos = pygame.mouse.get_pos()
        
        self.draw_cards_from_cards_indicator = None
        self.draw_spells_from_cards_indicator = None
        
        self.movement_indicator = None  # signals movement amount
        self.moving_tokens = False # tokens are to be moved
        self.available_moves = []

        # Attack phase variables
        
        self.attack_indicator = None
        self.attacking_tokens = False
        self.available_attacks = []
        self.damage_in_course = 0
        self.damaged_token = None
        self.damage_dealt = 0
        
        self.defense_indicator = False
        
        # pre-game / deploy phase variables
        self.chosen_token = None
        self.pos = None
        self.ocupied_cell = None
        
        ############ USER DEFINED EVENTS 
        
        self.mouse_once = True   # Prevents overclicking of mouse
        
        self.freezing_mouse_event = pygame.USEREVENT+1
        
        self.passing_phase = False
        
        
        # test variables
        
        """#prueba = TokenObject(CELL, 0, 0, "token_1.png", "prueba1",1,"")
        prueba2 = TokenObject(CELL,CELL*3, CELL*4, "token_1.png", "prueba2", 1,"")
        prueba3 = TokenObject(CELL,CELL*3,CELL*2, "token_3.png", "prueba3",1,"")

        enemy1 = TokenObject(CELL,CELL*0,CELL*0, "token_2.png", "prueba2", 2,"")
        #enemy2 = TokenObject(CELL,CELL*2, CELL*3, "token_2.png", "prueba2", 2,"")
        #enemy3 = TokenObject(CELL,CELL*4, CELL*3, "token_2.png", "prueba2", 2,"")
        #enemy4 = TokenObject(CELL,CELL*2, CELL*2, "token_2.png", "prueba2", 1,"")
        #enemy5 = TokenObject(CELL,CELL*2, CELL*1, "token_2.png", "prueba2", 1,"")
        #enemy6 = TokenObject(CELL,CELL*4, CELL*2, "token_2.png", "prueba2", 1,"")
        #enemy7 = TokenObject(CELL,CELL*4, CELL*1, "token_2.png", "prueba2", 1,"")
        #enemy8 = TokenObject(CELL,CELL*3, CELL*1, "token_2.png", "prueba2", 1,"")"""
        
         
        
        phase = str
        

        
        
        
        # Network Objects
        
        self.net = Network()  
        
        self.server = Process(target = server_main)
        
        self.order_to_send = "NONE" # msg send to server
        self.recieved_order = "NONE" # msg recieved from the server 
        
        self.repeat_order_control = "NONE"  # used to check on repeated msgs
        
        self.player_log = []
        self.enemy_log = []
        self.order_number = 0
        self.recieved_order_number = -1
        
        
        # Main Menu Widgets
        self.faction_dropdown = DropDown(["white", "grey"], ["green", "blue"], CELL*6, CELL*5, CELL*3, CELL, GENERIC_FONT, "Select Faction", FACTIONS)
        self.faction_chosen_button = Button(CELL*6, CELL*2, CELL*3, CELL,GENERIC_FONT, "continue","gray", lambda: self.dummy_method() )
        self.host_button = Button(CELL*6, CELL*4, CELL*3, CELL,GENERIC_FONT, "HOST", "red",lambda: self.host_game_method() )
        self.join_button = Button(CELL*6, CELL*6, CELL*3, CELL,GENERIC_FONT, "JOIN", "white", lambda: self.to_second_menu() )
        
        # Pregame Scene Widgets
        self.pre_game_cancel_button = Button(CELL, CELL//4*3, CELL*2,CELL//2, GENERIC_FONT, "Cancel Deploy", "red", lambda: self.pregame_mat_assigner())
        self.pre_game_ok_button = Button(CELL*4, CELL//4*3, CELL*2,CELL//2, GENERIC_FONT, "Confirm Deploy", "darkgreen", lambda: self.confirm_deployment())
        
        # Game perse Widgets
        
        
    
        
    def main(self):
        
        #run = True
        #clock = pygame.time.Clock()
        self.mousepos = pygame.mouse.get_pos()
        
        
        #self.scene = "client_test"
        #self.player_a.token_list_loader()
        self.scene = "first_menu"
        
        while self.run:
            
            if self.scene == "first_menu":
                self.main_menu()
            elif self.scene == "second_menu":
                self.main_menu()
            elif self.scene == "pre_game":
                self.pre_game()
            elif self.scene == "in_course_preparations":
                self.in_course_preparations()
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
    
    ### MAIN MENU BLOCK ###
    
    
    
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
        self.player_is_hosting = True
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
            #self.net.send_recv("NONE")
            self.player_turn = False
            self.player_b.player_faction = enemy_faction
            self.player_b.general_list_loader()
            self.player_b.token_list_loader()  
            print("enemy: ",self.player_b)
            #self.net.send_recv("NONE")
            self.pregame_mat_assigner()
            self.scene = "pre_game"
            
        
        
    def dummy_method(self):
        pass
        
    
    def menu_draw(self):
        
        phase_informer = "pre-game"
    
        
        
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
            self.net.send_recv("NONE")
            self.player_b.player_faction = response
            print("enemy faction:",self.player_b.player_faction)
            self.player_b.general_list_loader()
            self.player_b.token_list_loader()
            #self.net.send_recv("NONE")
            self.pregame_mat_assigner() # assigns starting positions to each player token before launching the deploy phase
            self.order_to_send = "NONE"
            self.scene = "pre_game"
            
        else: pass 
            
        
        
        self.WIN.fill(BACKGROUND_COLOR)
        
        phase_informer = "Waiting Enemy to Connect"
        current_phase_informer = GENERIC_FONT.render(phase_informer, 1, "red")
        self.WIN.blit(current_phase_informer, (CELL*10, 20))
#
       
        
        pygame.display.update()
     
    
    def talker_with_logger(self):
        
        
            
        
        self.net.send_only(self.order_to_send)
        if self.order_to_send != "NONE":
            print("##########> ORDER SENDED:   ", self.order_to_send)
        
        self.recieved_order = self.net.recieve_only()
        
        if self.recieved_order != "NONE":
            try:
                splitted_recieved_order = self.recieved_order.split("}", 1)
                msg_number = splitted_recieved_order[0]
                recieved_msg = splitted_recieved_order[1]
                if int(msg_number) > self.recieved_order_number:
                    code, target, order = recv_msg_translator(recieved_msg)
                    self.orders_interpreter_method(code, target, order)
                    print("recieved: ",self.recieved_order, " /// number of recieved: ", self.recieved_order_number)
                    self.recieved_order_number += 1
            except:
                print("Failed interpretation of order")   
                    
        if self.order_to_send != self.repeat_order_control:
            self.repeat_order_control = self.order_to_send
            self.order_number += 1
        
                
        
    
    """def repeated_msg_checker(self):
        
        if self.order_to_send == self.repeat_order_control :
            self.order_to_send = "NONE"
        else:
            self.repeat_order_control = self.order_to_send"""
            
    def standard_talker(self):
        
        self.net.send_only(self.order_to_send)
        if self.order_to_send != "NONE":
            print("##########> ORDER SENDED:   ", self.order_to_send)
            print("IN SCENE: ", self.scene)
        
        self.recieved_order = self.net.recieve_only()
        
        if self.recieved_order != "NONE":
            try:
                code, target, order = recv_msg_translator(self.recieved_order)
                self.orders_interpreter_method(code, target, order)
                print(self.recieved_order)
                #self.order_to_send = "RESPONSE]"+self.recieved_order 
            except: 
                print("Failed interpretation of order")  
                
        self.order_to_send = "NONE" 
        
    """def talker_with_response_checker(self):
        
        self.net.send_only(self.order_to_send)
        
        
        #if self.order_to_send.split("]",1)[0] == "RESPONSE":
        #    print("changing order: "+self.order_to_send)
        #    self.order_to_send = "NONE"
        #    print("to: "+self.order_to_send)
            
        self.recieved_order = self.net.recieve_only()
        
        if self.recieved_order != "NONE":
            if self.recieved_order == self.repeat_order_control:
                self.recieved_order = "NONE"
            else:
                self.repeat_order_control = self.recieved_order
                print("order received: ", self.recieved_order)
                try:
                    code, target, order = recv_msg_translator(self.recieved_order)
                    self.orders_interpreter_method(code, target, order)
                    print(self.recieved_order)
                    #self.order_to_send = "RESPONSE]"+self.recieved_order 
                except: 
                    print("Failed interpretation of order")       
                #self.orders_interpreter_method(code, target, order)
                #self.order_to_send = "RESPONSE]"+self.recieved_order 
            #code, target, order = recv_msg_translator(self.recieved_order)

            #if code == "RESPONSE":
            #    if self.order_to_send == target:
            #        self.order_to_send = "NONE"
            #elif code == "NONE":
            #    pass
            #else:
            
        
        #self.order_to_send = "NONE"    
        #self.net.send_only(self.order_to_send)
        
        """
            
       
    def orders_interpreter_method(self, code, target, order):
        
        
        
        if code == "BATCH":  # initial deploy order. Structure: "BATCH]all:xpos1,ypos1;xpos2,ypos;..."
            #print("initial deploy")
            #self.enemy_ready = True
                        
            for indicator in range(len(self.player_b.player_tokens)):
                xpos, ypos = order[indicator][0], order[indicator][1]
                self.player_b.player_tokens[indicator].vector_to_go[:] = xpos, ypos 
                
        
        elif code == "VECTORTOGO":
            
            for token in self.player_b.player_tokens:
                if str(token) == target:
                    xpos, ypos = order[0][0], order[0][1]
                    token.vector_to_go[:] = xpos, ypos
            
            
            
        elif code == "CARDSDRAWN":
            if target == "faction":
                self.player_b.enemy_fate_phase(order)
            elif target == "spell":
                self.player_b.enemy_spell_draw(order)
            
                
            print("cards drawn")
        
        #elif code == "DAMAGE":
        #    for token in self.player_a.player_tokens:
        #        if str(token) == target:
        #            token.hits = token.hits - order
        
        elif code == "DAMAGE":
            self.defense_indicator = True
            #self.defense_activation(target, int(order))
            self.damaged_token = target
            self.damage_dealt = int(order)
            
        
        elif code == "DEFENSE":
            for token in self.player_b.player_tokens:
                if str(token) == target:
                    token.hits = token.hits - order
            
                    
        elif code == "CARDPLAYED":
            card_info_name, card_type_info, card_info_image = self.player_b.enemy_card_played(target, order)
            print("card played")
        elif code == "ACARDPLAYED":
            print("move token")
        elif code == "XFCARDPLAYED":
            print("XF card played")
        elif code == "XFCARDPLAYED":
            print("XS card played")
        elif code == "SCARDPLAYED":
            print("move token")
        elif code == "NEXT_PHASE":
            self.phase_passer_method()
        elif code == "TURN_CHANGE":
            print("turn change")
            self.player_turn = not self.player_turn
        #print()

        

 
    def pre_game(self):
        
         
        
        self.clock.tick(FPS)
        self.mousepos = pygame.mouse.get_pos()
        #self.scene = "pre_game"
        #self.order_to_send = "NONE"
        #self.recieved_order = "NONE"
        #self.repeated_msg_checker()
        
        self.standard_talker()
        #self.talker_with_logger()
        #if self.order_to_send != "NONE":
        #self.net.send_only(self.order_to_send)
        
        
        #self.recieved_order = self.net.recieve_only()
        
        
        #self.recieved_order = self.net.send_recv(self.order_to_send)
        
        if self.recieved_order != "NONE":
            #### testing filtering msgs #########
            if self.recieved_order.rsplit("]")[0] == "BATCH":
                self.enemy_ready = True
            try:
                #code, target, order = recv_msg_translator(self.recieved_order)
                #self.orders_interpreter_method(code, target, order)
                #self.enemy_ready = True
                pass
                
            except: pass
        
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
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                try:
                    self.net.send("!DISCONNECT")
                    self.server.terminate()
                except: pass
                self.run = False
        
            if event.type == pygame.MOUSEBUTTONUP :
                #if pre_game_cancel_button.collidepoint(self.mousepos): # cancel initial placement
                    #self.pregame_mat_assigner()
                    #self.moving_tokens = False
                    #self.chosen_token = None
                
                #if pre_game_ok_button.collidepoint(self.mousepos) and len(self.available_moves) == 0:
                #    print("next scene")
                #    #var = 0
                #    #available_test = [(x,y) for x in range (8) for y in range(6, 8)]
                #    order = "BATCH]all:"
                #    for token in self.player_a.player_tokens:
                #        order += str(token.vector_to_go[0])+","+str(token.vector_to_go[1])+";"
                #                                
                #    order = order[:-1]
                #    tosend = order    
                #    
                #    print("tosend: ",tosend)
                #    #self.net.send_recv(tosend)
                    
                    
                
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
            
            # Widgets
            if not self.player_ready: # prevent redeploy after finnished 
                self.pre_game_cancel_button.update(events)
            self.pre_game_ok_button.update(events)
        
       ####### Working perfectly ######   
       
        #self.repeated_msg_checker()          
        
        #self.recieved_order = self.net.send_recv(self.order_to_send)
        #
        #if self.recieved_order != "NONE":
        #    try:
        #        code, target, order = recv_msg_translator(self.recieved_order)
        #        self.orders_interpreter_method(code, target, order)
        #        self.enemy_ready = True
        #        
        #    except: pass
        
        if self.player_ready:
            if self.enemy_ready:
                """order = "BATCH]all:"
                order = ""
                for token in self.player_a.player_tokens:
                    order += str(token.vector_to_go[0])+","+str(token.vector_to_go[1])+";"
                    
                    
                order = order[:-1]
                #self.order_to_send = order    
                self.order_to_send = send_msg_translator_with_log(self.order_number,"BATCH","all",order)
                
                print("tosend: ",self.order_to_send)
            """
                #self.confirm_deployment()
                
                self.available_moves = []
                #self.order_to_send = "NONE"
                #self.scene = "in_course"
                self.scene = "in_course_preparations" 
        
        ###################3 END ########################3
        
        #self.recieved_order = self.net.send_recv(self.order_to_send)
        #
        #if self.recieved_order != "NONE":
        #    try:
        #        code, target, order = recv_msg_translator(self.recieved_order)
        #        self.orders_interpreter_method(code, target, order)
        #        self.enemy_ready = True
        #        
        #    except: pass
        #
        #if self.player_ready:
        #    if self.enemy_ready:
        #    
        #        self.confirm_deployment()
        #        
        #        self.available_moves = []
        #        #self.scene = "in_course"
        #        self.scene = "in_course_preparations" 
        
        
                    
                
        if self.scene == "pre_game":
            self.draw_window_pregame()
        else: 
            print("CHANGING SCENE OK")
        
    
    def draw_window_pregame(self):   
        
        phase_informer = "pre-game"
    
        """if self.player:
            phase_informer = "a_"+self.current_phase
        else: phase_informer = "b_"+self.current_phase"""
        
        self.WIN.fill(BACKGROUND_COLOR)
        BOARD.fill("tan4")

        for row in range(ROWS):
            for col in range(row % 2, COLUMNS, 2):
                pygame.draw.rect(BOARD, "grey3",(CELL*col, CELL*row, CELL,CELL))
                
        pygame.draw.rect(BOARD,"green", PRE_GAME_TOKEN_MAT) 
        
        
        
        locate_token_text = GENERIC_FONT.render("Place the tokens in the avilable positions", 1, "red")
        BOARD.blit(locate_token_text,(CELL, CELL//4))
        
        pygame.draw.rect(BOARD, "red", pre_game_cancel_button)
        self.pre_game_cancel_button.draw(BOARD)
        if len(self.available_moves) == (2*COLUMNS)-len(self.player_a.player_tokens):
            self.pre_game_ok_button.draw(BOARD)
            #pygame.draw.rect(BOARD, "darkgreen", pre_game_ok_button)
        """else: 
            pygame.draw.rect(BOARD, "darkgreen", pre_game_ok_button)"""
        self.starting_positions()
        self.selected_token()
        self.token_movement("pre_game")
         
               
        self.WIN.blit(BOARD,(0,0))    # actualizes BOARD -> always after all changes of it

        
        
#
        current_phase_informer = GENERIC_FONT.render(phase_informer, 1, "red")
        self.WIN.blit(current_phase_informer, PHASE_INFORMER_RECT)
#
       
        
        pygame.display.update()
     
    
    """def in_course_preparations_2(self):
        
        #self.repeated_msg_checker()
                
        #if self.order_to_send != "NONE":
        
                
        self.net.send_only(self.order_to_send)
        
        
        self.recieved_order = self.net.recieve_only()
        
        self.player_ready = True
        
        #self.recieved_order = self.net.send_recv(self.order_to_send)
        try:
            code, target, order = recv_msg_translator(self.recieved_order)
            self.orders_interpreter_method(code, target, order)
        except: pass
        #self.recieved_order = self.net.send_recv(self.order_to_send)
        #code, target, order = recv_msg_translator(self.recieved_order)
        #self.orders_interpreter_method(code, target, order)
        
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                try:
                    self.net.send("!DISCONNECT")
                    self.server.terminate()
                    
                except: pass
                
                self.run = False
                
        # test one-shot
        drawn_cards = self.player_a.fate_phase(repetitions = 6)
        self.order_to_send = send_msg_translator("CARDSDRAWN", "faction", drawn_cards)
        print("SELF.ORDER_TO_SEND: CARDS DRAWN ===> ",self.order_to_send)
        #self.net.send_only(self.order_to_send)
        #self.recieved_order = self.net.send_recv(self.order_to_send)
        #try:
        #    code, target, order = recv_msg_translator(self.recieved_order)
        #    self.orders_interpreter_method(code, target, order)
        #    #self.player_ready = True
        #except: pass
        
        
        if self.player_ready:
            print("pass pregame")
            self.scene = "in_course"
        else: 
            print("failed to receive instructions")
                
        #self.recieved_order = "NONE"
        #drawn_cards = self.player_a.fate_phase(repetitions = 3)
        #self.order_to_send = send_msg_translator("CARDSDRAWN", "faction", drawn_cards)
        #print(self.order_to_send)
        #self.clock.tick(FPS)
                
        #response = self.net.send_recv(self.order_to_send)
        #
        #if response != "NONE":
        #    
        #    try:
        #        code, target, order = recv_msg_translator(self.recieved_order)
        #        if code == "CARDSDRAWN":
        #            self.orders_interpreter_method(code, target, order)
        #            self.enemy_ready = True
        #            print("going to in_course")
        #    
        #            self.scene = "in_course"
        #        else: pass
        #    except: pass
        #    #self.net.send_recv("NONE")
        #    #code, target, order = recv_msg_translator(self.recieved_order)
        #    #self.orders_interpreter_method(code, target, order)
        #    #self.player_b.player_faction = response
        #    #print("going to in_course")
        #    #
        #    #self.scene = "in_course"
        #else: pass 
        #self.player_ready = False
        #self.enemy_ready = False
        #self.recieved_order = "NONE"
        #drawn_cards = self.player_a.fate_phase(repetitions = 3)
        #self.order_to_send = send_msg_translator("CARDSDRAWN", "faction", drawn_cards)
        #self.recieved_order = self.net.send_recv(self.order_to_send)
        #
        #while self.enemy_ready == False:
        #    if self.player_ready == False:
        #        self.recieved_order = self.net.send_recv(self.order_to_send)
        #        if self.recieved_order != "NONE":
        #            try:
        #                code, target, order = recv_msg_translator(self.recieved_order)
        #                self.orders_interpreter_method(code, target, order)
        #                self.player_ready = True
        #            except:
        #                pass
        #    elif self.player_ready == True:
        #        self.order_to_send = "PLAYER_READY"
        #        if self.recieved_order == "PLAYER_READY":
        #            self.enemy_ready == True
        #    self.recieved_order = self.net.send_recv(self.order_to_send)
        #        
        #    
        #if self.enemy_ready and self.player_ready:
        #    self.net.send_recv(self.order_to_send)
        #    self.scene = "in_course" """
        
    def in_course_preparations(self):
        
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                try:
                    self.net.send("!DISCONNECT")
                    self.server.terminate()
                    
                except: pass
                
                self.run = False
        
        self.standard_talker()
        #self.talker_with_logger()        
        #self.talker_with_response_checker()
        
        #self.repeated_msg_checker()
                
        #if self.order_to_send != "NONE":
        #self.net.send_only(self.order_to_send)
        #
        #
        #self.recieved_order = self.net.recieve_only()
        #
        #try:
        #    code, target, order = recv_msg_translator(self.recieved_order)
        #    self.orders_interpreter_method(code, target, order)
        #except: pass
        
        drawn_cards = self.player_a.fate_phase(repetitions = 6)
        
        self.order_to_send = send_msg_translator_with_log(self.order_number,"CARDSDRAWN", "faction", drawn_cards)
        self.order_to_send = send_msg_translator("CARDSDRAWN", "faction", drawn_cards)
        print("SELF.ORDER_TO_SEND: CARDS DRAWN ===> ",self.order_to_send)
        #self.net.send_only(send_msg_translator("CARDSDRAWN", "faction", drawn_cards))
        #self.recieved_order = self.net.recieve_only()
        #try:
        #    code, target, order = recv_msg_translator(self.recieved_order)
        #    
        #    self.orders_interpreter_method(code, target, order)
        #except: pass
        
        self.standard_talker()
        #self.talker_with_logger()
        #self.talker_with_response_checker()
        print("pass pregame")
        self.scene = "in_course"
            
    def in_course(self):
        
        
        
        self.clock.tick(FPS)
        self.mousepos = pygame.mouse.get_pos()
        focus_faction_card = None
        focus_spell_card = None
        
        self.standard_talker()
        #self.talker_with_response_checker()
        #self.talker_with_logger()
        
        #self.net.send_only(self.order_to_send)
        #
        #
        #self.recieved_order = self.net.recieve_only()
        #
        ##self.recieved_order = self.net.send_recv(self.order_to_send)
        #
        #if self.recieved_order != "NONE":
        #    try:
        #        code, target, order = recv_msg_translator(self.recieved_order)
        #        self.orders_interpreter_method(code, target, order)
        #        #self.enemy_ready = True
        #    except: 
        #        print("Failed interpretation of order")       
        
        # Network orders cleaner
        
        #self.order_to_send = "NONE"
        
                
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
                
            ### MOUSEBUTTONUP EVENTS ###

            if event.type == pygame.MOUSEBUTTONUP : # and self.mouse_once == True:
                #self.mouse_once = False
                if button2.collidepoint(self.mousepos):   ### passing phases ---> test only
                    
                    self.phase_passer_method()
                    #pygame.time.set_timer(self.freezing_mouse_event, 50, 1)
                    
                    
            
                if self.player_turn and self.passing_phase == False:
                    
                    #if temporal_change_turn_button.collidepoint(self.mousepos):
                    #    
                    #    self.player_turn = not self.player_turn
                    #    print("player turn change",self.player_turn)
                    #    self.order_to_send = "TURN_CHANGE]all:0"

                    ### SPELL CARDS EVENTS ###
    
                    for scrd in self.player_a.player_spell_hand_objs:
                        if scrd.rec.collidepoint(self.mousepos):
                            #print("spell card played")  # CONTROL
                            pass
                        
                    ### FATE PHASE ###
    
                    if self.current_phase == "fate":
                    
                        if faction_deck_drawer_button.collidepoint(self.mousepos):
                            
                            drawn_cards = self.player_a.fate_phase(repetitions = 3)
                            
                            self.order_to_send = send_msg_translator_with_log(self.order_number,"CARDSDRAWN", "faction", drawn_cards)
                            self.order_to_send = send_msg_translator("CARDSDRAWN", "faction", drawn_cards)
                            print(self.order_to_send)
                            #pygame.time.set_timer(self.freezing_mouse_event, 50, 1) # prevents hitting the cards when draself.WINg
                            
                            self.phase_passer_method()
                            
                    ### SUMMON PHASE EVENT ###
                    
                    if self.current_phase == "summon":
                        if self.draw_cards_from_cards_indicator != None:
                            drawn_cards = self.player_a.fate_phase(repetitions=self.draw_cards_from_cards_indicator)
                            self.order_to_send = send_msg_translator_with_log(self.order_number,"CARDSDRAWN", "faction", drawn_cards)
                            self.order_to_send = send_msg_translator("CARDSDRAWN", "faction", drawn_cards)
                            self.draw_cards_from_cards_indicator = None
                            self.phase_passer_method()
                            #pygame.time.set_timer(self.freezing_mouse_event, 50, 1)
                        elif self.draw_spells_from_cards_indicator != None:
                            drawn_cards = self.player_a.xs_card_activation(repetitions=self.draw_spells_from_cards_indicator)
                            self.order_to_send = send_msg_translator_with_log(self.order_number,"CARDSDRAWN", "spell", drawn_cards)
                            self.order_to_send = send_msg_translator("CARDSDRAWN", "spell", drawn_cards)
                            self.draw_spells_from_cards_indicator = None
                            self.phase_passer_method()
                            #pygame.time.set_timer(self.freezing_mouse_event, 50, 1)
                        
                        else:    
                            card_selected, code = self.card_picker()
                            #drawn_cards = self.player_a.fate_phase(repetitions=int(code))
                            self.order_to_send = send_msg_translator_with_log(self.order_number,"CARDPLAYED", "faction", card_selected)
                            self.order_to_send = send_msg_translator("CARDPLAYED", "faction", card_selected)
                        #pygame.time.set_timer(self.freezing_mouse_event, 50, 1)
    
                    ### MOVE PHASE EVENT ###
    
                    if self.current_phase == "move":
                    
                    
                        if pygame.mouse.get_cursor() == pygame.cursors.broken_x: 
                            for move in self.available_moves:
                                if move.collidepoint(self.mousepos):
                                    self.movement_activation(move)
                                   
    
                        elif pygame.mouse.get_cursor() == pygame.cursors.diamond:
                        
                            for token in self.player_a.player_tokens:
                                if self.moving_tokens and token.rec.collidepoint(self.mousepos):
                                    self.chosen_token = token
    
                                    self.available_moves = available_movement_detector_linear_vector(token, self.movement_indicator ,self.player_a.player_tokens, self.player_b.player_tokens)
                                    #print("self.available_moves",self.available_moves)
                        else:
                            card_selected, code = self.card_picker()

                            self.order_to_send = send_msg_translator_with_log(self.order_number,"CARDPLAYED", "faction", card_selected)
                            self.order_to_send = send_msg_translator("CARDPLAYED", "faction", card_selected)
                            
                            
                    ### ATTACK PHASE EVENT ###
    
                    if self.current_phase == "att": 
                    
                        if pygame.mouse.get_cursor() == pygame.cursors.broken_x:
                            for attack in self.available_attacks:
                                if attack.collidepoint(self.mousepos):
                                   for enemy in self.player_b.player_tokens:
                                       if enemy.rec.collidepoint(self.mousepos):
                                            ### hit the enemy
                                            self.damage_activation(enemy)
                                            
                                                                                       
    
    
                        elif pygame.mouse.get_cursor() == pygame.cursors.diamond:
                        
                            for token in self.player_a.player_tokens:
                                if self.attacking_tokens and token.rec.collidepoint(self.mousepos):
                                    self.chosen_token = token
                                    self.available_attacks = available_attacks_detector_maxrange_square(token, self.attack_indicator, self.player_a.player_tokens, self.player_b.player_tokens)
                                    #print(self.available_attacks)
    
    
                        else:
                            card_selected, code = self.card_picker()
                            self.order_to_send = send_msg_translator_with_log(self.order_number,"CARDPLAYED", "faction", card_selected)
                            self.order_to_send = send_msg_translator("CARDPLAYED", "faction", card_selected)                                        
    
    
    
    
                ### DEFENSE PHASE EVENT ###
                if self.defense_indicator and self.player_turn == False:
                    print("in the defense phase")
                    #self.defense_activation(self.damaged_token, self.damage_dealt)
                    
                    
                #if self.current_phase == "def" and self.damaged_token != None: # test function
                    
                    #self.player_turn = False
                    for token in self.player_a.player_tokens:
                        if str(token) == self.damaged_token:
                    
                            if no_defense_button.collidepoint(self.mousepos):

                                token.hits = token.hits - self.damage_dealt
                                #self.damage_in_course = 0

                                #self.player_turn = True

                                self.order_to_send = send_msg_translator_with_log(self.order_number,"DEFENSE", self.damaged_token, str(self.damage_dealt))
                                self.order_to_send = send_msg_translator("DEFENSE", self.damaged_token, str(self.damage_dealt))
                                print("order to send in defense: "+self.order_to_send)
                                self.damaged_token = None
                                self.defense_indicator = False
                                                        
                        
                        
        
        
        
        self.passing_phase = False
                
        # surviving tokens control
        
        for token_a in self.player_a.player_tokens:
            if token_a.hits < 1:
                self.player_a.player_tokens.remove(token_a)
        for token_b in self.player_b.player_tokens:
            if token_b.hits < 1:
                self.player_b.player_tokens.remove(token_b)



        pygame.event.clear()
        self.draw_window(focus_faction_card, focus_spell_card, "in_course")
    
         
        
    def draw_window(self, focus_faction_card, focus_spell_card, game_status_indicator):
        
        phase_informer = str
    
        if self.player_turn:
            phase_informer = "Your trun: "+self.current_phase
        else: phase_informer = "Enemy's turn"+self.current_phase

        self.WIN.fill(BACKGROUND_COLOR)
        BOARD.fill("tan4")

        for row in range(ROWS):
            for col in range(row % 2, COLUMNS, 2):
                pygame.draw.rect(BOARD, "grey3",(CELL*col, CELL*row, CELL,CELL))
    
        
        self.available_moves_method()   
        self.token_movement("in_course")
        self.available_attacks_method()
        
        


        self.WIN.blit(BOARD,(0,0))    # actualizes BOARD -> always after all changes of it

        pygame.draw.rect(self.WIN, "pink",FACTION_HAND)
        pygame.draw.rect(self.WIN, "red",SPELLS_HAND)
        pygame.draw.rect(self.WIN, "pink",ENEMY_FACTION_HAND)
        pygame.draw.rect(self.WIN, "red",ENEMY_SPELLS_HAND)


        faction_deck = pygame.image.load(os.path.join("images","faction_deck2.jpg")).convert_alpha() # load faction deck image
        faction_deck_scaled_image = pygame.transform.scale(faction_deck, (faction_deck_drawer_button.width, faction_deck_drawer_button.height))
        self.WIN.blit(faction_deck_scaled_image, (faction_deck_drawer_button))

        pygame.draw.rect(self.WIN, "white", button2)
        
        #pygame.draw.rect(self.WIN, "yellow", temporal_change_turn_button)
        
        if self.defense_indicator and self.player_turn == False:
            pygame.draw.rect(self.WIN, "aqua", no_defense_button)

        spells_deck = pygame.image.load(os.path.join("images","spells_deck_scaled.jpg")).convert_alpha() # load spells deck image
        spells_deck_scaled_image = pygame.transform.rotate(spells_deck, 90.0)
        spells_deck_scaled_image = pygame.transform.scale(spells_deck_scaled_image,(spells_deck_drawer_button.width, spells_deck_drawer_button.height))
        self.WIN.blit(spells_deck_scaled_image, (spells_deck_drawer_button))

        current_phase_informer = GENERIC_FONT.render(phase_informer, 1, "red")
        self.WIN.blit(current_phase_informer, PHASE_INFORMER_RECT)

        faction_hand_sign = GENERIC_FONT.render("Faction Hand", 1, "black")
        self.WIN.blit(faction_hand_sign,(FACTION_HAND.x+5,FACTION_HAND.y))

        spells_hand_sign = GENERIC_FONT.render("Spells hand",1,"black")
        self.WIN.blit(spells_hand_sign, (SPELLS_HAND.x+5,SPELLS_HAND.y))
        
        
            
        self.faction_hand_controller(focus_faction_card, self.current_phase)
        self.spells_hand_controller(focus_spell_card, self.current_phase)
        self.enemy_faction_hand_controller()
        




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
        self.moving_tokens = False
        self.chosen_token = None
        
    def confirm_deployment(self):
        
        if self.player_ready == False:
        
            print("next scene")

            order = "BATCH]all:"
            order = ""
            for token in self.player_a.player_tokens:
                order += str(token.vector_to_go[0])+","+str(token.vector_to_go[1])+";"

            order = order[:-1]
            self.order_to_send = send_msg_translator_with_log(self.order_number, "BATCH", "all", order)  
            self.order_to_send = send_msg_translator("BATCH", "all", order)    

            print("tosend: ",self.order_to_send)

            self.player_ready = True
        else: 
            print("next scene")

            order = "BATCH]all:"
            order = ""
            for token in self.player_a.player_tokens:
                order += str(token.vector_to_go[0])+","+str(token.vector_to_go[1])+";"

            order = order[:-1]
            self.order_to_send = send_msg_translator_with_log(self.order_number, "BATCH", "all", order)  
            self.order_to_send = send_msg_translator("BATCH", "all", order)  
  

            print("tosend: ",self.order_to_send)
            
            
            
            
       
    def starting_positions(self):
        
        
        #positions_slots = starting_position_function(self.player_a.player_tokens)
        for pos_slot in self.available_moves:
            
            color = (0,127+waving_func(pygame.time.get_ticks()),0)
            pygame.draw.rect(BOARD, color, pos_slot, width=6,border_radius=10)

    
            
    def faction_hand_controller(self, card,  current_phase):
        
        available_space = (FACTION_HAND.width-8-CARD_WIDTH*1.1*2)//(len(self.player_a.player_hand_objs)+2)
            
        for crd in self.player_a.player_hand_objs:  # positions cardobject
            
            xpos = float
            ypos = float
            position = pygame.Vector2(0,0)
            
            #crd.rec.x = FACTION_HAND.x+5+CELL*player_hand.index(crd)*0.7 # assigns position to the object in the hand
            #crd.rec.y = FACTION_HAND.y+CELL*0.7

            if current_phase == "move" and (crd.card_type == "M" or crd.card_type == "XF" or crd.card_type == "XS"):
                #xpos = FACTION_HAND.x+CELL*0.2
                #position = pygame.Vector2(xpos, FACTION_HAND.y+5+available_space*self.player_a.player_hand_objs.index(crd))
                
                ypos = FACTION_HAND.y+CELL*0.2
                position = pygame.Vector2(FACTION_HAND.x+5+available_space*self.player_a.player_hand_objs.index(crd), ypos)
                #crd.card_drawer(self.WIN,pygame.Vector2(FACTION_HAND.x+5+CELL*player_hand.index(crd)*0.7, ypos))

            elif current_phase == "att" and (crd.card_type == "A"):
                #xpos = FACTION_HAND.x+CELL*0.2
                #position = pygame.Vector2(xpos, FACTION_HAND.y+5+available_space*self.player_a.player_hand_objs.index(crd))
                ypos = FACTION_HAND.y+CELL*0.2
                position = pygame.Vector2(FACTION_HAND.x+5+available_space*self.player_a.player_hand_objs.index(crd), ypos)

                #crd.card_drawer(self.WIN, position)  
            elif current_phase == "def" and (crd.card_type == "D"):
                #xpos = FACTION_HAND.x+CELL*0.3
                #position = pygame.Vector2(xpos, FACTION_HAND.y+5+available_space*self.player_a.player_hand_objs.index(crd))
                ypos = FACTION_HAND.y+CELL*0.2
                position = pygame.Vector2(FACTION_HAND.x+5+available_space*self.player_a.player_hand_objs.index(crd), ypos)

                #crd.card_drawer(self.WIN, position)  
            elif current_phase == "fate":
                #xpos = FACTION_HAND.x+CELL*0.7
                #position = pygame.Vector2(xpos, FACTION_HAND.y+5+available_space*self.player_a.player_hand_objs.index(crd))
                ypos = FACTION_HAND.y+CELL*0.7
                position = pygame.Vector2(FACTION_HAND.x+5+available_space*self.player_a.player_hand_objs.index(crd), ypos)
            elif current_phase == "summon" and (crd.card_type == "XS"):# or crd.card_type == "XF"):
                
                ypos = FACTION_HAND.y+CELL*0.2
                position = pygame.Vector2(FACTION_HAND.x+5+available_space*self.player_a.player_hand_objs.index(crd), ypos)
                
            else:
                #xpos = FACTION_HAND.x+CELL*0.7
                #position = pygame.Vector2(xpos, FACTION_HAND.y+5+available_space*self.player_a.player_hand_objs.index(crd))
                ypos = FACTION_HAND.y+CELL*0.7
                position = pygame.Vector2(FACTION_HAND.x+5+available_space*self.player_a.player_hand_objs.index(crd), ypos)
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
    
    def enemy_faction_hand_controller(self):
        available_space = (ENEMY_FACTION_HAND.width-8)//(len(self.player_b.player_hand_objs)+1)
        for crd in self.player_b.player_hand_objs:
            ypos = int
            
            position = pygame.Vector2(ENEMY_FACTION_HAND.x+available_space*self.player_b.player_hand_objs.index(crd), ENEMY_FACTION_HAND.y+4)
            
            crd.card_drawer(self.WIN, position, enemy = True)
            
    def enemy_spell_hand_controller(self):
        
        available_space = (ENEMY_SPELLS_HAND.width-8)//(len(self.player_b.player_spell_hand_objs)+1)
        for crd in self.player_b.player_spell_hand_objs:
            ypos = int
            
            position = pygame.Vector2(ENEMY_SPELLS_HAND.x+available_space*self.player_b.player_hand_objs.index(crd), ENEMY_SPELLS_HAND.y+4)
            
            crd.card_drawer(self.WIN, position, enemy = True)
            
    def enemy_card_played_shower(self):
        
        
        
        pass
    
    def phase_passer_method(self):
        
        
        if len(GAME_SEQUENCE) == GAME_SEQUENCE.index(self.current_phase)+1:
            
            
            self.player_turn = not self.player_turn
            self.current_phase = GAME_SEQUENCE[0]
            
        else:
            
            self.current_phase = GAME_SEQUENCE[GAME_SEQUENCE.index(self.current_phase)+1]
            
        self.passing_phase =True
        self.order_to_send = send_msg_translator_with_log(self.order_number,"NEXT_PHASE", "pass", "phase")
        self.order_to_send = send_msg_translator("NEXT_PHASE", "pass", "phase")

    def movement_activation(self, move):
        
        self.pos = (move.x, move.y)
        #print("move to: ", self.pos)
        self.position = pygame.Vector2(self.pos[0], self.pos[1])
        self.chosen_token.vector_to_go = self.position
        # sending order to server
        self.order_to_send = send_msg_translator_with_log(self.order_number,"VECTORTOGO",self.chosen_token,self.pos)
        self.order_to_send = send_msg_translator("VECTORTOGO",self.chosen_token,self.pos)
        
        
        ### resetting values to prevent various movements over the same card ###
        self.available_moves = [] 
        self.pos = None
        self.movement_indicator = None
        self.moving_tokens = False
        
        self.phase_passer_method()
        #pygame.time.set_timer(self.freezing_mouse_event, 50, 1)
        
        #self.phase_passer_method()
        
    def damage_activation(self, enemy):
        
        self.damaged_token = self.player_b.player_tokens.index(enemy) # to use
                                            
        #self.damage_dealt = self.damage_in_course
        #enemy.hits = enemy.hits - self.damage_in_course
    
        ### resetting values to prevent various attacks over the same card ###
        self.available_attacks = []
        self.attack_indicator = None
        self.attacking_tokens = False
        self.defense_indicator = True
        #self.player_b.player_tokens[self.damaged_token].hits = self.player_b.player_tokens[self.damaged_token].hits - self.damage_in_course
        
        
        
        self.order_to_send = send_msg_translator_with_log(self.order_number,"DAMAGE", self.player_b.player_tokens[self.damaged_token], self.damage_in_course)
        self.order_to_send = send_msg_translator("DAMAGE", self.player_b.player_tokens[self.damaged_token], self.damage_in_course)
        
        print("Damage msg : ", self.order_to_send)
        
        self.damage_in_course = 0
        #self.current_phase = "def"
        #pygame.time.wait(10000)
        #pygame.time.set_timer(self.freezing_mouse_event, 50, 1)
        #self.phase_passer_method()
    
    def defense_activation(self, damaged_token, damage_to_deal):
        
        for crd in self.player_a.player_hand_objs:
                if crd.rec.collidepoint(self.mousepos):        
                
                    if crd.card_type == "D":
                        
                        crd.activate_card()
                        self.damage_in_course = 0
                        #self.damaged_token = None
                        damage_to_deal = 0
                        self.player_a.faction_card_discard(crd)
                        #self.player_turn = True
                        self.defense_indicator = False
                        #discarder("cards_a", str(crd.identif))
                        #self.player_a.player_hand_objs.remove(crd)
                        self.order_to_send = send_msg_translator_with_log(self.order_number,"DEFENSE", damaged_token, damage_to_deal)
                        self.order_to_send = send_msg_translator("DEFENSE", damaged_token, damage_to_deal)
                        
                        
        if no_defense_button.collidepoint(self.mousepos):
            
            #self.player_b.player_tokens[self.damaged_token].hits = self.player_b.player_tokens[self.damaged_token].hits - self.damage_in_course
            self.damage_in_course = 0
            #self.damaged_token = None
            #self.player_turn = True
            self.defense_indicator = False
            for token in self.player_a.player_tokens:
                if str(token) == damaged_token:
                    token.hits = token.hits - damage_to_deal
                    self.order_to_send = send_msg_translator_with_log(self.order_number,"DEFENSE", damaged_token, damage_to_deal)
                    self.order_to_send = send_msg_translator("DEFENSE", damaged_token, damage_to_deal)
        
                
        
        
        
    
    
    def card_picker(self):
        card_picked = str
        code = str
        if self.current_phase == "move":
            for crd in self.player_a.player_hand_objs:
                if crd.rec.collidepoint(self.mousepos):
                    if (crd.card_type == "M"): # or crd.card_type == "XF"): # or crd.card_type == "XS"):
                        code = crd.activate_card()
                        #discarder("cards_a", str(crd.identif))
                        #if crd.card_type == "M":
                        #    self.order_to_send = "MCARDPLAYED]:"+str(crd)+":all"
                        #elif crd.card_type == "XS" or crd.card_type == "XF":
                        #    self.order_to_send = "XCARDPLAYED]:"+str(crd)+":"+crd.card_type
                        card_picked = str(crd)
                        self.player_a.faction_card_discard(crd)
                        #self.player_a.player_hand_objs.remove(crd)
    
                        self.movement_indicator = self.player_a.move_phase(code)
    
                        if self.movement_indicator != None: self.moving_tokens = True
                        #print("self.moving_tokens: ",self.moving_tokens)  # CONTROL
    
            for crd in self.player_a.player_spell_hand_objs:
                if crd.rec.collidepoint(self.mousepos):
                    self.player_a.spell_card_discard(crd)
                    
        elif self.current_phase == "att":
            for crd in self.player_a.player_hand_objs:
                if crd.rec.collidepoint(self.mousepos):
                    if (crd.card_type == "A"):
                        self.attack_indicator = crd.activate_card()[1]
                        code = crd.activate_card()[1]
                        #discarder("cards_a", str(crd.identif))
                        self.damage_in_course = crd.damage
                        card_picked = str(crd)
                        self.player_a.faction_card_discard(crd)
                        #self.player_a.player_hand_objs.remove(crd)
    
    
                        #self.player_a.attack_phase()
    
                        if self.attack_indicator != None: 
                            self.attacking_tokens = True
        
        elif self.current_phase == "summon":
            for crd in self.player_a.player_hand_objs:
                if crd.rec.collidepoint(self.mousepos):
                    if (crd.card_type == "XS"or crd.card_type == "XF"):
                        code = crd.activate_card()[1]
                        if crd.card_type == "XS":
                            card_picked = str(crd)
                            self.draw_spells_from_cards_indicator = int(code)
                        elif crd.card_type == "XF":
                            card_picked = str(crd)
                            self.draw_cards_from_cards_indicator = int(code)
                            
                            
                            
                        #discarder("cards_a", str(crd.identif))
                        #if crd.card_type == "M":
                        #    self.order_to_send = "MCARDPLAYED]:"+str(crd)+":all"
                        #elif crd.card_type == "XS" or crd.card_type == "XF":
                        #    self.order_to_send = "XCARDPLAYED]:"+str(crd)+":"+crd.card_type
                        #card_picked = str(crd)
                        self.player_a.faction_card_discard(crd)
                        #self.player_a.player_hand_objs.remove(crd)
    
                        #self.movement_indicator = self.player_a.move_phase(code)
    
                        #if self.movement_indicator != None: self.moving_tokens = True
                        #print("self.moving_tokens: ",self.moving_tokens)  # CONTROL
            
        
        print("returning card in card_picker :" ,card_picked)
        return card_picked, code    
        



def main():
    """server = Process(target = server_main)
    server.start()"""
    M = Main("NONE")
    M.main()
    
    


if __name__=="__main__":
    
    main()
    
    #M = Main()
    #M.main()