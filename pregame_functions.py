import pygame

from constants import CELL, PRE_GAME_TOKEN_MAT
from gameobjects import TokenObject


def player_token_assigner(list_of_tokens, player_object):
    token_mat_positions = [(x,y)for x in range(8) for y in range(2)]
    pos = 0
    for token_inf in list_of_tokens:
        player_object.player_tokens.append(TokenObject(CELL, token_mat_positions[pos][0],token_mat_positions[pos][1],token_inf[0],token_inf[1],int(token_inf[2]), token_inf[3]))
        pos += 1
        #TokenObject(CELL, 0, 0, "token_1.png", "prueba1",1,"")