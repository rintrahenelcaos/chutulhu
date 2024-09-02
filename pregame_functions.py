import pygame

from constants import CELL, PRE_GAME_TOKEN_MAT, BOARD
from gameobjects import TokenObject
from dbintermediatefunctions import token_extractor

def player_token_assigner(token_origin, player_object):
    #token_mat_positions = [(x,y)for x in range(8) for y in range(2)]
    list_of_tokens = token_extractor(token_origin)
    pos = 0
    for token_inf in list_of_tokens:
        player_object.player_tokens.append(TokenObject(CELL, PRE_GAME_TOKEN_MAT.x,PRE_GAME_TOKEN_MAT.y,token_inf[0],token_inf[1],int(token_inf[2]), token_inf[3]))
        pos += 1
        #TokenObject(CELL, 0, 0, "token_1.png", "prueba1",1,"")
        
def starting_position_function(token_list):
    
    available_positions = [(x,y) for x in range (8) for y in range(6, 8)]
    available_moves = []
    
    for token in token_list:
        for pos in available_positions:
            if token.rec.x == pos[0]*CELL and token.rec.y == pos[1]*CELL:
                available_positions.remove(pos)
    for pos in available_positions: 
        available_moves.append(pygame.Rect((pos[0]*CELL, pos[1]*CELL), (CELL, CELL)))
        
    return available_moves
    
    
    