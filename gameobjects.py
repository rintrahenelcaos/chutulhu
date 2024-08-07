import pygame

import os


class CardObject(pygame.sprite.Sprite):
    
    
    def __init__(self, size, xpos, ypos, image, identif) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.size = size*1
        self.xpos = xpos
        self.ypos = ypos
        self.go_pos = pygame.Vector2(self.xpos, self.ypos)
        self.rec = pygame.Rect(self.go_pos[0], self.go_pos[1], self.size, self.size)
        self.image = pygame.image.load(os.path.join("images",str(image))).convert_alpha()
        self.scaled_image = pygame.transform.scale(self.image, (self.size, self.size))
        self.moving = False
        #self.image = image
        self.identif = identif
        self.looked_on = False
    
    def __str__(self) -> str:
        return str(self.identif)   
    
    def __repr__(self) -> str:
        return self.identif
        
    def card_drawer(self, board, vector = None):
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
        if self.looked_on:
            self.card_info_shower(board) 
            #self.scaled_image = pygame.transform.scale(self.image,(self.size*1.2, self.size*1.2))
        else: 
            #print(type(self.image))
            self.scaled_image = pygame.transform.scale(self.image, (self.size, self.size))
            board.blit(self.scaled_image, (self.rec))
    
    def card_positioner(self,  top = False):
        
        self.rec.width = self.size*0.5
        if top:
            self.rec.width = self.size
    
    def card_info_shower(self, board):
        
        info_rec = pygame.Rect(self.rec.x, self.rec.y-self.size*2, self.size, self.size)
        info_image = pygame.transform.scale(self.image,(self.size*2, self.size*3))
        board.blit(info_image, (info_rec))
        
        
             
        
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
        