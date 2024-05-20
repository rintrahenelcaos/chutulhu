import pygame
import math
import os

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
pos_b = None
game_objects_list = []



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

class GameObject:
    def __init__(self, size, xpos, ypos, image):
        self.size = size
        self.xpos = xpos
        self.ypos = ypos
        self.go_pos = pygame.Vector2(self.xpos, self.ypos)
        self.rec = pygame.Rect(self.go_pos[0], self.go_pos[1], self.size, self.size)
        self.image = pygame.image.load(os.path.join("images",str(image))).convert_alpha()
        self.scaled_image = pygame.transform.scale(self.image, (CELL, CELL))
        
        
        
    
    def move(self, vector):
        self.go_pos = self.go_pos.move_towards(vector, 2)
        self.rec.x = self.go_pos[0]
        self.rec.y = self.go_pos[1]
        

def draw_window(pos, prueba):
    
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
        
    if pos != None:
        selected_pos = grid_position(pos)
        selected_in_grid = GRID.index(selected_pos)
        chosen_cell = (pygame.Rect(CELL*selected_pos[0], CELL*selected_pos[1], CELL, CELL),pygame.time.get_ticks())
        pos_b = pygame.Vector2(chosen_cell[0].x, chosen_cell[0].y)
        
    for obj in game_objects_list:
        
        if pos_b != None:
            obj.move(pos_b)
        BOARD.blit(obj.scaled_image, (obj.rec))
        
    
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
    
    
    prueba = GameObject(CELL, pos_a[0], pos_a[1], "token_1.png")
    prueba2 = GameObject(CELL,300, 0, "token_2.png")
    prueba3 = GameObject(CELL,700,700, "token_3.png")
    game_objects_list.append(prueba)
    game_objects_list.append(prueba2)
    game_objects_list.append(prueba3)
    
    while run:
        
        clock.tick(FPS)
        pos = None
        if BOARD.get_rect().collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_cursor(pygame.cursors.diamond)
        else: pygame.mouse.set_cursor(pygame.cursors.arrow)
        
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_cursor()==pygame.cursors.diamond:
                    pos = pygame.mouse.get_pos()
                    print("board ", pos)
                    
        draw_window(pos, prueba)
    
    #prueba = GameObject(CELL, 0, 0)       
            
                
            
            
        
        
        
        
    
    pygame.quit()
    

if __name__=="__main__":
    main()
    