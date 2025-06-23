import pygame
import pyautogui

import os


class Enemy_Does_Capsulle:
    
    def __init__(self, capsulle_width, capsulle_height, initial_pos, activated_pos, colour, image, text) -> None:
        self.width = capsulle_width
        self.height = capsulle_height
        self.initial_pos = initial_pos
        self.activated_pos = activated_pos
        
        self.color = colour
        self.image = image
        self.text = text
        self.active = True
        self.v2_position = pygame.Vector2(self.initial_pos)
        self.rect = pygame.Rect(self.initial_pos[0], self.initial_pos[1], self.width, self.height)
        self.image = pygame.image.load(os.path.join("images",str(image))).convert_alpha()
        self.scaled_image = pygame.transform.scale(self.image, (self.width, self.height))
        
    def capsulle_drawer(self, board, vector = None, enemy = False):
        
        if vector != None :
            self.v2_position = self.v2_position.move_towards(vector, 10)
            self.rect.x = self.v2_position[0]
            self.rect.y = self.v2_position[1]
        
        self.scaled_image = pygame.transform.scale(self.image, (self.width, self.height))
        board.blit(self.scaled_image, (self.rect))
    



