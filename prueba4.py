import pygame
import sys
import os

from constants import GENERIC_FONT


class Test_Card():
    def __init__(self, xpos, ypos, width, height, colour, image, identif, card_type, range, description) -> None:
        self.xpos = xpos
        self.ypos = ypos
        self.rect = pygame.Rect(xpos, ypos, width, height)
        self.rect = pygame.Surface((width, height))
        self.colour = colour
        self.image = pygame.image.load(os.path.join("images",str(image))).convert_alpha()
        self.identif = identif
        self.card_type = card_type
        self.range = range
        self.description = description
    
    def test_card_draw(self, board):
        
        image_container = pygame.Rect(0,25,self.rect.get_width(), self.rect.get_height()//2)
        scaled_image = pygame.transform.scale(self.image, (image_container.width-10, image_container.height-10))
        card_info_name = GENERIC_FONT.render(self.identif, 1, "black")
        description = GENERIC_FONT.render(self.description, 1, "black")
        
        self.rect.fill("tan")
        pygame.draw.rect(self.rect, "red", image_container)
        self.rect.blit(scaled_image,( 5, image_container.y+5))
        self.rect.blit(card_info_name, (2, 5))
        self.rect.blit(description, (5, image_container.y+image_container.height+5))
        
        board.blit(self.rect, (self.xpos, self.ypos))
        
        #pygame.draw.rect(board, self.colour, ((self.xpos, self.ypos),(self.rect)),width=20)
        
        
        
        

def main():
    pygame.init()
    # print(sorted(pygame.font.get_fonts()))
    screen = pygame.display.set_mode((1150, 480))
    pygame.display.init()
    
    test1 = Test_Card(20, 10, 200, 400, "red", "spells_deck.png", "test_card", "T", "5", "test card descriptio to check line width identation and the rest")
    
    screen.fill("green")
    test1.test_card_draw(screen)        
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            
        
        




if __name__ == "__main__":
    main()