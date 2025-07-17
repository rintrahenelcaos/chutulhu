import pygame
import sys


class Test_Card():
    def __init__(self, xpos, ypos, width, height, colour) -> None:
        self.rect = pygame.Rect(xpos, ypos, width, height)
        self.colour = colour
    
    def test_card_draw(self, board):
        
        board.draw.rect(board, self.colour, self.rect)
        

def main():
    pygame.init()
    # print(sorted(pygame.font.get_fonts()))
    screen = pygame.display.set_mode((1150, 480))
    pygame.display.init()
    
    test1 = Test_Card(20, 10, 60, 40, "red")
    
    screen.fill("green")
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
        test1.test_card_draw(screen)        
        pygame.display.update()
        




if __name__ == "__main__":
    main()