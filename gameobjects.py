import pygame

import os


class CardObject:
    
    def __init__(self, size, xpos, ypos,image, identif) -> None:
        self.size = size
        self.xpos = xpos
        self.ypos = ypos
        self.go_pos = pygame.Vector2(self.xpos, self.ypos)
        self.rec = pygame.Rect(self.go_pos[0], self.go_pos[1], self.size, self.size)
        self.image = pygame.image.load(os.path.join("images",str(image))).convert_alpha()
        self.scaled_image = pygame.transform.scale(self.image, (self.rec.width, self.rec.height))
        self.moving = False
        #self.image = image
        self.identif = identif
        
    def card_drawer(self, board, vector = None, looked_on = False):
        if vector != None:
            self.go_pos = self.go_pos.move_towards(vector, 2)
            self.rec.x = self.go_pos[0]
            self.rec.y = self.go_pos[1]
        """if looked_on:
            self.rec.height = self.rec.height*1.5
            self.rec.width = self.rec.width*1.5
        else: 
            self.rec.height = self.size
            self.rec.width = self.size"""
        if looked_on: 
            self.scaled_image = pygame.transform.scale2x(self.image)
        else: 
            print(type(self.image))
            self.scaled_image = pygame.transform.scale(self.image, (self.rec.width, self.rec.height))
        board.blit(self.scaled_image, (self.rec))
             
        pass

class TokenObject:
    
    def __init__(self, size, xpos, ypos, image, identif):
        self.size = size
        self.xpos = xpos
        self.ypos = ypos
        self.go_pos = pygame.Vector2(self.xpos, self.ypos)
        self.rec = pygame.Rect(self.go_pos[0], self.go_pos[1], self.size, self.size)
        self.image = pygame.image.load(os.path.join("images",str(image))).convert_alpha()
        self.scaled_image = pygame.transform.scale(self.image, (self.size, self.size))
        self.moving = False
        self.identif = identif
        
    def __str__(self) -> str:
        return str(self.identif)    
        
        
    
    def token_object_drawer(self, board, vector = None):
        if vector != None:
            self.go_pos = self.go_pos.move_towards(vector, 2)
            self.rec.x = self.go_pos[0]
            self.rec.y = self.go_pos[1]
        board.blit(self.scaled_image, (self.rec))
        