import pygame

import os

from constants import CARD_FONT, CELL, BOARD
from functionsmodule import movement_activation, x_activation, attack_activation, defense_activation


class CardObject(pygame.sprite.Sprite):
    
    
    def __init__(self, size, xpos, ypos, image, identif, card_type, range, damage = 1, card_back = "faction_deck.png") -> None:
        pygame.sprite.Sprite.__init__(self)
        self.size = size*1
        self.sizeheight = size*5/3
        self.xpos = xpos
        self.ypos = ypos
        self.go_pos = pygame.Vector2(self.xpos, self.ypos)
        self.rec = pygame.Rect(self.go_pos[0], self.go_pos[1], self.size, self.size)
        self.image_dir = image
        self.image = pygame.image.load(os.path.join("images",str(image))).convert_alpha()
        self.scaled_image = pygame.transform.scale(self.image, (self.size, self.size))
        self.back_image = pygame.image.load(os.path.join("images",str(card_back))).convert_alpha()
        self.scaled_back_image = pygame.transform.scale(self.back_image, (self.size, self.sizeheight))
        self.moving = False
        self.identif = identif
        self.looked_on = False
        self.card_type = card_type
        self.range = range
        self.damage = damage
        self.name_show = identif.replace("_"," ")[:-1]
        
    
    def __str__(self) -> str:
        return str(self.identif)   
    
    def __repr__(self) -> str:
        return self.identif
        
    def card_drawer(self, board, vector = None, enemy = False):
        if vector != None:
            self.go_pos = self.go_pos.move_towards(vector, 10)
            self.rec.x = self.go_pos[0]
            self.rec.y = self.go_pos[1]
        
        if enemy:
            board.blit(self.scaled_back_image, (self.rec))
        else:
        
            if self.looked_on:
                self.card_info_shower(board) 
                #self.scaled_image = pygame.transform.scale(self.image,(self.size*1.2, self.size*1.2))
            else: 
                #print(type(self.image))
                self.scaled_image = pygame.transform.scale(self.image, (self.size, self.sizeheight))
                board.blit(self.scaled_image, (self.rec))
        
    
    def card_positioner(self,  top = False):
        
        self.rec.width = self.size*0.5
        if top:
            self.rec.width = self.size
    
    def card_info_shower(self, board):
        
        
        info_rec = pygame.Rect(self.rec.x, self.rec.y-self.size*2, self.size, self.sizeheight)
        info_image = pygame.transform.scale(self.image,(self.size*2, self.sizeheight*2))
        card_info_name = CARD_FONT.render(self.name_show, 1, "black")
        card_type_info = CARD_FONT.render(self.card_type,1,"red")
        board.blit(info_image, (info_rec))
        board.blit(card_info_name,(info_rec.x, info_rec.y))
        board.blit(card_type_info,(info_rec.x, self.rec.y + self.size*0.8))
    
    def activate_card(self):
        print(self.name_show, "    ", self.card_type)
        code = (self.card_type, self.range) 
        """if self.card_type == "M":
            code = movement_activation((self.range))
        elif self.card_type == "XS" or self.card_type == "XF":
            code = x_activation(self.card_type,int(self.range))
        elif self.card_type == "A":
            code = attack_activation((self.range))
        elif self.card_type == "D":
            code = defense_activation()"""
        return code
    
    def card_information_returner(self):
        
        return self.image_dir, self.card_type, self.name_show, self.range, self.damage         
        
             
        
class TokenObject(pygame.sprite.Sprite):
    
    def __init__(self, size, xpos, ypos, image, identif, hits, notes):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.xpos = xpos
        self.ypos = ypos
        self.go_pos = pygame.Vector2(self.xpos, self.ypos)
        self.rec = pygame.Rect(self.go_pos[0], self.go_pos[1], self.size, self.size)
        self.image = pygame.image.load(os.path.join("images",str(image))).convert_alpha()
        self.scaled_image = pygame.transform.scale(self.image, (self.size, self.size))
        self.moving = False
        self.identif = identif
        self.vector_to_go = pygame.Vector2(self.xpos, self.ypos)
        self.hits = hits
        self.notes = notes
        
    def __str__(self) -> str:
        return str(self.identif)    
        
        
    
    def token_object_drawer(self, board, vector = None, turner = False):
        if vector != None:
            self.vector_to_go = vector
        if turner:
             
            self.go_pos = self.go_pos.move_towards(self.vector_to_go, 10)
            self.rec.x = abs(self.go_pos[0] - BOARD.get_width()) - CELL
            self.rec.y = abs(self.go_pos[1] - BOARD.get_height()) -  CELL
            
        else:    
            self.go_pos = self.go_pos.move_towards(self.vector_to_go, 10)
            self.rec.x = self.go_pos[0]
            self.rec.y = self.go_pos[1]
        if self.rec.x == self.vector_to_go.x and self.rec.y == self.vector_to_go.y:
            self.moving = False
        board.blit(self.scaled_image, (self.rec))
        
        
def main():
    pygame.display.set_mode((10, 10))
    pygame.display.init()
    token = TokenObject(10,1,2,"token_2.png","one",2,"dfgdf")
    print(token)
    print(token.vector_to_go)
    print(type(token.vector_to_go))
    print(type(token.vector_to_go[0]))
    if str(token) == "one":
        print("recognizes by string")
        
    else: print("failed identification")

#main()