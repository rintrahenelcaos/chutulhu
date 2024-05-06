import pygame

WIDTH, HEIGHT = 900, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TO CHANGE")
CELL = 100
ROWS = 8
COLUMNS = 8

BACKGROUND_COLOR = (0,0,0)

BOARD = [((x*CELL, y*CELL), []) for x in range(8) for y in range(8)]

def draw_window():
    
    
    #WIN.fill(BACKGROUND_COLOR)
    
    
    pygame.display.update()


def main():
    """ MMain game function
    """
    
    run = True
    WIN.fill(BACKGROUND_COLOR)
    pygame.draw.rect(WIN, "tan4", pygame.Rect(0,0,800,800))
    for row in range(ROWS):
        for col in range(row % 2, ROWS, 2):
            pygame.draw.rect(WIN, "grey3",(CELL*row, CELL*col, CELL,CELL))
    """for cell in BOARD:
        print(BOARD.index(cell)%2)
        if BOARD.index(cell)%2 == 0:
            pygame.draw.rect(WIN, "white",pygame.Rect(cell[0],cell[1],100,100))
            
        else: pygame.draw.rect(WIN, "red",pygame.Rect(cell[0],cell[1],100,100))"""
    
    while run:
        
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:
                run = False
            
                
            
            
        
        
        draw_window()
        
    
    pygame.quit()
    

if __name__=="__main__":
    main()
    print(BOARD)
    print(len(BOARD))