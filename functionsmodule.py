import pygame

from dbintermediatefunctions import drawer, card_counter, card_data_extractor
from constants import CELL




def movement_activation(range):
    print("movement: ", range)
    return ("M", range)
    
def x_activation(code ,number): #draws card from spell deck
    """sensible = card_counter(self.player_deck, "deck")
       #deckcounter = "SELECT COUNT(*) FROM "+db+" WHERE location='"+deck+"'"
       #print(deckcounter)
       #pointer.execute(deckcounter)
       #deckcount = pointer.fetchone()[0]
       #print("deckcount = ", deckcount, " ", type(deckcount))
    if sensible == 0:
        reshuffle_deck(self.player_deck)
        deckmixer(self.player_deck)
        print("reshufle")
    drawer(self.player_deck, "hand", "deck")
    
    self.hand_refresher(card_data_extractor(self.player_deck, "hands"), xpos, ypos)  """
    
    print(code,": ", number)
    return (code, number)
    

def attack_activation(range):
    print("attack: ", range)
    
def defense_activation():
    print("defense")


def movement_blocker(available_moves, token_lists_a, token_list_b):  # movement with pathfinder
    
    templist = available_moves.copy()
    
    for move in templist:
        for token_a in token_lists_a:
            if move == token_a.rec:
                available_moves.remove(move)
                
        for token_b in token_list_b:
            if move == token_b.rec:
                available_moves.remove(move) 
            
        
    #print("out of movement_bloker: ",available_moves)
    return available_moves


    
def available_movement_detector_pathfinding(token_indicator, movement, token_lists_a, token_list_b):   # with pathfinding
    
    token_rec = token_indicator.rec    
    available_moves = [token_rec] 
    
    
    if movement == "K":
        temp_list = []
        k1 = pygame.Rect((token_rec.x - CELL*2, token_rec.y - CELL),(CELL,CELL)) 
        temp_list.append(k1)
        k2 = pygame.Rect((token_rec.x - CELL*2, token_rec.y + CELL),(CELL,CELL))
        temp_list.append(k2)
        k3 = pygame.Rect((token_rec.x + CELL*2, token_rec.y + CELL),(CELL,CELL))
        temp_list.append(k3)
        k4 = pygame.Rect((token_rec.x + CELL*2, token_rec.y + CELL),(CELL,CELL))
        temp_list.append(k4)
        k5 = pygame.Rect((token_rec.x - CELL, token_rec.y - CELL*2),(CELL,CELL))
        temp_list.append(k5)
        k6 = pygame.Rect((token_rec.x + CELL, token_rec.y - CELL*2),(CELL,CELL))
        temp_list.append(k6)
        k7 = pygame.Rect((token_rec.x - CELL, token_rec.y + CELL*2),(CELL,CELL))
        temp_list.append(k7)
        k8 = pygame.Rect((token_rec.x + CELL, token_rec.y + CELL*2),(CELL,CELL))
        temp_list.append(k8)
        available_moves = movement_blocker(temp_list, token_lists_a, token_list_b)
        available_moves = [i for n, i in enumerate(available_moves) if i not in available_moves[:n]]
    
    else:    
           
        for mov in range(int(movement)):
            temp_list = []            
            for mov in available_moves:
            
                n_mov = pygame.Rect((mov.x, mov.y - CELL),(CELL,CELL))
                temp_list.append(n_mov)
                ne_mov = pygame.Rect((mov.x + CELL, mov.y - CELL),(CELL,CELL))
                temp_list.append(ne_mov)
                e_mov =  pygame.Rect((mov.x + CELL, mov.y),(CELL,CELL))
                temp_list.append(e_mov)
                se_mov =  pygame.Rect( (mov.x + CELL, mov.y + CELL),(CELL,CELL))
                temp_list.append(se_mov)
                s_mov = pygame.Rect((mov.x, mov.y + CELL) ,(CELL,CELL))
                temp_list.append(s_mov)
                sw_mov = pygame.Rect((mov.x - CELL, mov.y + CELL) ,(CELL,CELL))
                temp_list.append(sw_mov)
                w_mov =  pygame.Rect((mov.x - CELL, mov.y),(CELL,CELL))
                temp_list.append(w_mov)
                nw_mov =  pygame.Rect((mov.x - CELL, mov.y - CELL),(CELL,CELL))
                temp_list.append(nw_mov)
            #print(temp_list)
            #temp_list = list(set(temp_list))
            available_moves = movement_blocker(temp_list, token_lists_a, token_list_b)
            available_moves = [i for n, i in enumerate(available_moves) if i not in available_moves[:n]]
        #print(available_moves) 
    #print(available_moves)
    
    return available_moves

def available_movement_detector_linear_vector(token_indicator, movement, friendly_tokens, enemy_tokens):   # with vector movement in square
    
    token_rec = token_indicator.rec    
    available_moves = [token_rec] 
    
    
    if movement == "K":
        temp_list = []
        k1 = pygame.Rect((token_rec.x - CELL*2, token_rec.y - CELL),(CELL,CELL)) 
        temp_list.append(k1)
        k2 = pygame.Rect((token_rec.x - CELL*2, token_rec.y + CELL),(CELL,CELL))
        temp_list.append(k2)
        k3 = pygame.Rect((token_rec.x + CELL*2, token_rec.y + CELL),(CELL,CELL))
        temp_list.append(k3)
        k4 = pygame.Rect((token_rec.x + CELL*2, token_rec.y + CELL),(CELL,CELL))
        temp_list.append(k4)
        k5 = pygame.Rect((token_rec.x - CELL, token_rec.y - CELL*2),(CELL,CELL))
        temp_list.append(k5)
        k6 = pygame.Rect((token_rec.x + CELL, token_rec.y - CELL*2),(CELL,CELL))
        temp_list.append(k6)
        k7 = pygame.Rect((token_rec.x - CELL, token_rec.y + CELL*2),(CELL,CELL))
        temp_list.append(k7)
        k8 = pygame.Rect((token_rec.x + CELL, token_rec.y + CELL*2),(CELL,CELL))
        temp_list.append(k8)
        available_moves = movement_blocker(temp_list, friendly_tokens, enemy_tokens)
        available_moves = [i for n, i in enumerate(available_moves) if i not in available_moves[:n]]
    
    else:    
           
        for mov in range(int(movement)):
            temp_list = []            
            for mov in available_moves:
            
                n_mov = pygame.Rect((mov.x, mov.y - CELL),(CELL,CELL))
                temp_list.append(n_mov)
                ne_mov = pygame.Rect((mov.x + CELL, mov.y - CELL),(CELL,CELL))
                temp_list.append(ne_mov)
                e_mov =  pygame.Rect((mov.x + CELL, mov.y),(CELL,CELL))
                temp_list.append(e_mov)
                se_mov =  pygame.Rect( (mov.x + CELL, mov.y + CELL),(CELL,CELL))
                temp_list.append(se_mov)
                s_mov = pygame.Rect((mov.x, mov.y + CELL) ,(CELL,CELL))
                temp_list.append(s_mov)
                sw_mov = pygame.Rect((mov.x - CELL, mov.y + CELL) ,(CELL,CELL))
                temp_list.append(sw_mov)
                w_mov =  pygame.Rect((mov.x - CELL, mov.y),(CELL,CELL))
                temp_list.append(w_mov)
                nw_mov =  pygame.Rect((mov.x - CELL, mov.y - CELL),(CELL,CELL))
                temp_list.append(nw_mov)
            #print(temp_list)
            available_moves = temp_list
            available_moves = [i for n, i in enumerate(available_moves) if i not in available_moves[:n]]
        friends_in_sight, enemies_in_sight = token_detector(token_rec, available_moves, friendly_tokens, enemy_tokens)
        available_moves = movement_acquisition(token_rec, available_moves, friends_in_sight, enemies_in_sight)
            
        #print(available_moves) 
    #print(available_moves)
    
    return available_moves

"""
def target_acquisition(attacking_token, available_attacks, friendly_fire_list, targets_list):   # calculates options bia line of sight
    
    attacking_token_center = attacking_token.center
    templist = (available_attacks.copy())
    
    
    friends_list = []
    enemies_list = []
    
    for target in templist:
        for friendly in friendly_fire_list:
            print("friend: ", friendly.rec)
            if target == friendly.rec:
                friends_list.append(target)
                if attacking_token == target:
                    friends_list.remove(target)
        for enemy in targets_list:
            if target == enemy.rec:
                enemies_list.append(target)
    #print("friends: ", friends_list)
    enemies_on_sight = enemies_list.copy()
               
    for target in enemies_list:
        #print(target)
        blocked = False
        exclutionary_list = enemies_list.copy()
        exclutionary_list.remove(target)
        line = (attacking_token_center, target.center)
        
        for blocking_enemy in exclutionary_list:
            limited_inflate = blocking_enemy.inflate(-5, -5)
            obstacle_test = limited_inflate.clipline(line)
            if obstacle_test: 
                blocked = True
                #print("blocking: ",blocking_enemy, " the target: ", target)
            
        
        for friend in friends_list:
            friend_in_the_middle = friend.clipline(line)
            if friend_in_the_middle: blocked = True
        
        if blocked: enemies_on_sight.remove(target)
        
    return enemies_on_sight  
    """            

def token_detector(acting_token, available_positions, friendly_tokens, enemy_tokens): 
    
    
    templist = (available_positions.copy())
    
    
    friends_list = []
    enemies_list = []
    
    
    
    for target in templist:
        for friendly in friendly_tokens:
            #print("friend: ", friendly.rec)
            if target == friendly.rec:
                friends_list.append(target)
                if acting_token == target:
                    friends_list.remove(target)
        for enemy in enemy_tokens:
            if target == enemy.rec:
                enemies_list.append(target)
    
    return friends_list, enemies_list        
        
def target_acquisition_new(attacking_token, friends_list, enemies_list):
    
    
    attacking_token_center = attacking_token.center
    enemies_on_sight = enemies_list.copy()
    
    for target in enemies_list:
        
        blocked = False
        exclutionary_list = enemies_list.copy()
        exclutionary_list.remove(target)
        line = (attacking_token_center, target.center)
        
        for blocking_enemy in exclutionary_list:
            limited_inflate = blocking_enemy.inflate(-5, -5)
            obstacle_test = limited_inflate.clipline(line)
            if obstacle_test: 
                blocked = True
                
        
        for friend in friends_list:
            limited_inflate = friend.inflate(-5, -5)
            friend_in_the_middle = limited_inflate.clipline(line)
            if friend_in_the_middle: 
                blocked = True
        
        if blocked: enemies_on_sight.remove(target)
        
    return enemies_on_sight 

def k_target_adquisition(attacks, enemies_list):
    
    enemies_in_sight = enemies_list
    
    return enemies_in_sight
    
def movement_acquisition(moving_token, possible_moves, friends_in_the_way, enemies_in_the_way):
    
    moving_token_center = moving_token.center
    
    available_movements = possible_moves.copy()
    
    for move in possible_moves:
        
        blocked = False
        line = (moving_token_center, move.center)
        
        for blocking_enemy in enemies_in_the_way:
            limited_inflate = blocking_enemy.inflate(-5, -5)
            obstacle_test = limited_inflate.clipline(line)
            if obstacle_test: 
                blocked = True
        
        for blocking_friend in friends_in_the_way:
            limited_inflate = blocking_friend.inflate(-5, -5)
            friend_in_the_middle = limited_inflate.clipline(line)
            if friend_in_the_middle:
                blocked = True
        
        if blocked: available_movements.remove(move)
        if moving_token in available_movements: available_movements.remove(moving_token)
    
    return available_movements
    
    
    
                
                
"""            
def available_atacks_detector(token_indicator, attack_range, friendly_tokens_list, enemy_token_list):
    token_rec = token_indicator.rec
    token_center = (token_indicator.rec.x + CELL//2, token_indicator.rec.y + CELL//2)
    
    for step in range(int(attack_range)+1):
        n_mov = pygame.Rect((mov.x, mov.y - CELL),(CELL,CELL))
        temp_list.append(n_mov)
        ne_mov = pygame.Rect((mov.x + CELL, mov.y - CELL),(CELL,CELL))
        temp_list.append(ne_mov)
        e_mov =  pygame.Rect((mov.x + CELL, mov.y),(CELL,CELL))
        temp_list.append(e_mov)
        se_mov =  pygame.Rect( (mov.x + CELL, mov.y + CELL),(CELL,CELL))
        temp_list.append(se_mov)
        s_mov = pygame.Rect((mov.x, mov.y + CELL) ,(CELL,CELL))
        temp_list.append(s_mov)
        sw_mov = pygame.Rect((mov.x - CELL, mov.y + CELL) ,(CELL,CELL))
        temp_list.append(sw_mov)
        w_mov =  pygame.Rect((mov.x - CELL, mov.y),(CELL,CELL))
        temp_list.append(w_mov)
        nw_mov =  pygame.Rect((mov.x - CELL, mov.y - CELL),(CELL,CELL))
        temp_list.append(nw_mov)
    # detect cells in range
    friends_in_range = []
    for friendly in friendly_tokens_list:
        friendly_vector = pygame.Vector2(friendly.rec.x,friendly.rec.y)
        if friendly_vector.distance_to((token_rec.x,token_rec.y)) <= int(attack_range)*CELL+1:
            friends_in_range.append(friendly.rec)
    
    enemies_in_range = []
    for enemy in enemy_token_list:
        enemy_vector = pygame.Vector2(enemy.rec.x, enemy.rec.y)
        if enemy_vector.distance_to((token_rec.x, token_rec.y)) <= int(attack_range)*CELL+1:
            enemies_in_range.append(enemy.rec)
    
    available_attacks = friends_in_range + enemies_in_range 
    return available_attacks
        """


def available_attacks_detector_fixedrange(token_indicator, attack_range, token_lists_a, token_list_b):  # fixed range version with simplified directions
    token_rec = token_indicator.rec    
    available_attacks = [token_rec] 
    
    if attack_range == "K":
        temp_list = []
        k1 = pygame.Rect((token_rec.x - CELL*2, token_rec.y - CELL),(CELL,CELL)) 
        temp_list.append(k1)
        k2 = pygame.Rect((token_rec.x - CELL*2, token_rec.y + CELL),(CELL,CELL))
        temp_list.append(k2)
        k3 = pygame.Rect((token_rec.x + CELL*2, token_rec.y + CELL),(CELL,CELL))
        temp_list.append(k3)
        k4 = pygame.Rect((token_rec.x + CELL*2, token_rec.y + CELL),(CELL,CELL))
        temp_list.append(k4)
        k5 = pygame.Rect((token_rec.x - CELL, token_rec.y - CELL*2),(CELL,CELL))
        temp_list.append(k5)
        k6 = pygame.Rect((token_rec.x + CELL, token_rec.y - CELL*2),(CELL,CELL))
        temp_list.append(k6)
        k7 = pygame.Rect((token_rec.x - CELL, token_rec.y + CELL*2),(CELL,CELL))
        temp_list.append(k7)
        k8 = pygame.Rect((token_rec.x + CELL, token_rec.y + CELL*2),(CELL,CELL))
        temp_list.append(k8)
        available_attacks = temp_list - movement_blocker(temp_list, token_lists_a, token_list_b)
        available_attacks = [i for n, i in enumerate(available_attacks) if i not in available_attacks[:n]]
        
    
    else:    
           
        for ranged in range(1,int(attack_range)+1):
            temp_list = []            
            #for attack in available_attacks:
            
            n_mov = pygame.Rect((token_rec.x, token_rec.y - CELL*ranged),(CELL,CELL))
            temp_list.append(n_mov)
            ne_mov = pygame.Rect((token_rec.x + CELL*ranged, token_rec.y - CELL*ranged),(CELL,CELL))
            temp_list.append(ne_mov)
            e_mov =  pygame.Rect((token_rec.x + CELL*ranged, token_rec.y),(CELL,CELL))
            temp_list.append(e_mov)
            se_mov =  pygame.Rect( (token_rec.x + CELL*ranged, token_rec.y + CELL*ranged),(CELL,CELL))
            temp_list.append(se_mov)
            s_mov = pygame.Rect((token_rec.x, token_rec.y + CELL*ranged) ,(CELL,CELL))
            temp_list.append(s_mov)
            sw_mov = pygame.Rect((token_rec.x - CELL*ranged, token_rec.y + CELL*ranged) ,(CELL,CELL))
            temp_list.append(sw_mov)
            w_mov =  pygame.Rect((token_rec.x - CELL*ranged, token_rec.y),(CELL,CELL))
            temp_list.append(w_mov)
            nw_mov =  pygame.Rect((token_rec.x - CELL*ranged, token_rec.y - CELL*ranged),(CELL,CELL))
            temp_list.append(nw_mov)
            #print(temp_list)
            #temp_list = list(set(temp_list))
            #available_attacks = temp_list - movement_blocker(temp_list, token_lists_a, token_list_b)
            available_attacks = temp_list
            available_attacks = [i for n, i in enumerate(available_attacks) if i not in available_attacks[:n]]
    
    return available_attacks
    
    
def available_attacks_detector_maxrange_square(token_indicator, attack_range, friendly_token_list, enemy_token_list):    # max range version with square area effect
    
    token_rec = token_indicator.rec    
    available_attacks = [token_rec] 
    
    
    if attack_range == "K":
        temp_list = []
        k1 = pygame.Rect((token_rec.x - CELL*2, token_rec.y - CELL),(CELL,CELL)) 
        temp_list.append(k1)
        k2 = pygame.Rect((token_rec.x - CELL*2, token_rec.y + CELL),(CELL,CELL))
        temp_list.append(k2)
        k3 = pygame.Rect((token_rec.x + CELL*2, token_rec.y + CELL),(CELL,CELL))
        temp_list.append(k3)
        k4 = pygame.Rect((token_rec.x + CELL*2, token_rec.y + CELL),(CELL,CELL))
        temp_list.append(k4)
        k5 = pygame.Rect((token_rec.x - CELL, token_rec.y - CELL*2),(CELL,CELL))
        temp_list.append(k5)
        k6 = pygame.Rect((token_rec.x + CELL, token_rec.y - CELL*2),(CELL,CELL))
        temp_list.append(k6)
        k7 = pygame.Rect((token_rec.x - CELL, token_rec.y + CELL*2),(CELL,CELL))
        temp_list.append(k7)
        k8 = pygame.Rect((token_rec.x + CELL, token_rec.y + CELL*2),(CELL,CELL))
        temp_list.append(k8)
        
        #available_attacks = movement_blocker(temp_list, friendly_token_list, enemy_token_list)
        available_attacks = temp_list
        available_attacks = [i for n, i in enumerate(available_attacks) if i not in available_attacks[:n]]
        friends_not_use, enemies_in_sight = token_detector(token_rec, available_attacks, friendly_token_list, enemy_token_list)
        available_attacks = enemies_in_sight
    
    else:    
           
        for mov in range(int(attack_range)):
            temp_list = []            
            for mov in available_attacks:
            
                n_mov = pygame.Rect((mov.x, mov.y - CELL),(CELL,CELL))
                temp_list.append(n_mov)
                ne_mov = pygame.Rect((mov.x + CELL, mov.y - CELL),(CELL,CELL))
                temp_list.append(ne_mov)
                e_mov =  pygame.Rect((mov.x + CELL, mov.y),(CELL,CELL))
                temp_list.append(e_mov)
                se_mov =  pygame.Rect( (mov.x + CELL, mov.y + CELL),(CELL,CELL))
                temp_list.append(se_mov)
                s_mov = pygame.Rect((mov.x, mov.y + CELL) ,(CELL,CELL))
                temp_list.append(s_mov)
                sw_mov = pygame.Rect((mov.x - CELL, mov.y + CELL) ,(CELL,CELL))
                temp_list.append(sw_mov)
                w_mov =  pygame.Rect((mov.x - CELL, mov.y),(CELL,CELL))
                temp_list.append(w_mov)
                nw_mov =  pygame.Rect((mov.x - CELL, mov.y - CELL),(CELL,CELL))
                temp_list.append(nw_mov)
            #print(temp_list)
            #temp_list = list(set(temp_list))
            #available_attacks = movement_blocker(temp_list, friendly_token_list, enemy_token_list)
            available_attacks = temp_list
            available_attacks = [i for n, i in enumerate(available_attacks) if i not in available_attacks[:n]]
        #available_attacks.remove(token_rec)
        #print("avatts: ",available_attacks)
        firends_in_sight, enemies_in_sight = token_detector(token_rec, available_attacks, friendly_token_list, enemy_token_list)
        available_attacks = target_acquisition_new(token_rec, firends_in_sight, enemies_in_sight)
        
    #print(available_moves)
    
    return available_attacks