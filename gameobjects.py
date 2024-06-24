import pygame

import os


class CardObject:
    
    def __init__(self) -> None:
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
        
        
    
    def game_object_drawer(self, board, vector = None):
        if vector != None:
            self.go_pos = self.go_pos.move_towards(vector, 2)
            self.rec.x = self.go_pos[0]
            self.rec.y = self.go_pos[1]
        board.blit(self.scaled_image, (self.rec))
        