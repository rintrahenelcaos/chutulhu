import pygame
import math

WIDTH, HEIGHT = 900, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TO CHANGE")
CELL = 100
ROWS = 8
COLUMNS = 8

BACKGROUND_COLOR = (0,0,0)

BOARD = pygame.Surface((800, 800))
GRID = [(x, y) for x in range(8) for y in range(8)]

FPS = 60

chosen_cell = None
pos_a = pygame.Vector2(0, 0)
pos_b = pygame.Vector2(0, 0)



def grid_position(position):
    """translates clicks into discrete cell positions

    Args:
        position (tuple): coordinates

    Returns:
        tuple: cell position
    """
    
    x = (position[0]//CELL)#*CELL
    y = (position[1]//CELL)#*CELL
    return (x,y)

class GameObject():
    def __init__(self, speed, xpos, ypos, image) -> None:
        self.speed = speed
        self.xpos = xpos
        self.ypos = ypos
        self.pos = image.get_rect().move(xpos, ypos)
    
    def move(self, up=False, down=False, left=False, right=False):
        if right:
            self.pos.right += self.speed
        if left:
            self.pos.right -= self.speed
        if down:
            self.pos.top += self.speed
        if up:
            self.pos.top -= self.speed

def draw_window(pos):
    
    global chosen_cell
    global pos_a
    global pos_b
    
    WIN.fill(BACKGROUND_COLOR)
    BOARD.fill("tan4")
    
    
    
    for row in range(ROWS):
        for col in range(row % 2, ROWS, 2):
            pygame.draw.rect(BOARD, "grey3",(CELL*row, CELL*col, CELL,CELL))
   
    
    if chosen_cell != None:
        
        pygame.draw.rect(BOARD, (127+waving_func(pygame.time.get_ticks()-chosen_cell[1]),127+waving_func(pygame.time.get_ticks()-chosen_cell[1]),127+waving_func(pygame.time.get_ticks()-chosen_cell[1])), chosen_cell[0])
        
        #pos_a = pos_a.move_towards(pos_b,2)
    if pos != None:
        selected_pos = grid_position(pos)
        #print(selected_pos)
        #print(grid_position(pos))
        selected_in_grid = GRID.index(selected_pos)
        #print(selected_in_grid)
        #rect = pygame.Rect(CELL*selected_pos[0], CELL*selected_pos[1], CELL, CELL)
        #print((CELL*selected_pos[0], CELL*selected_pos[1], CELL, CELL))
        #pygame.draw.rect(BOARD, (255,0,0), (CELL*selected_pos[0], CELL*selected_pos[1], CELL, CELL))
        chosen_cell = (pygame.Rect(CELL*selected_pos[0], CELL*selected_pos[1], CELL, CELL),pygame.time.get_ticks())
        pos_b = pygame.Vector2(chosen_cell[0].x, chosen_cell[0].y)
        #print(pygame.time.get_ticks())
        
    
    pos_a = pos_a.move_towards(pos_b,10)
    #print(pos_a[0])
    #cuadr = pygame.Rect()
    pygame.draw.rect(BOARD, "white", (pos_a[0],pos_a[1], 100,100))
    
    
    
        
    
    
    WIN.blit(BOARD,(0,0))    # actualizes BOARD -> always after all changes odf it
    
    pygame.display.update()

def waving_func(time):
    z = 127*math.cos((2*math.pi/(FPS*40))*time)
    return z
    
def main():
    """ Main game function
    """
    
    run = True
    clock = pygame.time.Clock()
    
    #WIN.fill(BACKGROUND_COLOR)
    #BOARD.fill("tan4")
    
    
    #pygame.draw.rect(BOARD, "tan4", pygame.Rect(0,0,800,800))
    """for row in range(ROWS):
        for col in range(row % 2, ROWS, 2):
            pygame.draw.rect(BOARD, "grey3",(CELL*row, CELL*col, CELL,CELL))
            """
    """for cell in BOARD:
        print(BOARD.index(cell)%2)
        if BOARD.index(cell)%2 == 0:
            pygame.draw.rect(WIN, "white",pygame.Rect(cell[0],cell[1],100,100))
            
        else: pygame.draw.rect(WIN, "red",pygame.Rect(cell[0],cell[1],100,100))"""
        
        
    #WIN.blit(BOARD,(0,0))
    
    
    
    while run:
        
        clock.tick(FPS)
        pos = None
        if BOARD.get_rect().collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_cursor(pygame.cursors.diamond)
        else: pygame.mouse.set_cursor(pygame.cursors.arrow)
        
        
        """if BOARD.get_rect().collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_cursor() == pygame.cursors.diamond:
                pygame.mouse.set_cursor(pygame.cursors.arrow)
            else: pygame.mouse.set_cursor(pygame.cursors.diamond)"""
        
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_cursor()==pygame.cursors.diamond:
                    pos = pygame.mouse.get_pos()
                    print("board ", pos)
        draw_window(pos)
           
            
                
            
            
        
        
        
        
    
    pygame.quit()
    

if __name__=="__main__":
    main()
    