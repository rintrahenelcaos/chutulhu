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
GRID_DIC = {}
for cell in GRID:
    GRID_DIC.update({cell:"None"})

FPS = 60

chosen_cell = None
pos_a = pygame.Vector2(0, 0)
#pos_b = pygame.Vector2(0, 0)
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
    
    def __init__(self, size, xpos, ypos, image, identif):
        self.size = size
        self.xpos = xpos
        self.ypos = ypos
        self.go_pos = pygame.Vector2(self.xpos, self.ypos)
        self.rec = pygame.Rect(self.go_pos[0], self.go_pos[1], self.size, self.size)
        self.image = pygame.image.load(os.path.join("images",str(image))).convert_alpha()
        self.scaled_image = pygame.transform.scale(self.image, (CELL, CELL))
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
        

def draw_window(pos, token):
    
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
        
    """if pos != None:
        selected_pos = grid_position(pos)
        selected_in_grid = GRID.index(selected_pos)
        chosen_cell = (pygame.Rect(CELL*selected_pos[0], CELL*selected_pos[1], CELL, CELL),pygame.time.get_ticks())
        pos_b = pygame.Vector2(chosen_cell[0].x, chosen_cell[0].y)
        print(selected_in_grid)
        
    for obj in game_objects_list: 
        obj.game_object_drawer(pos_b, BOARD)
    """
        
    """ if pos_b != None:
            obj.move(pos_b, BOARD)
        BOARD.blit(obj.scaled_image, (obj.rec))"""
    
    game_mechanics(pos, token)    
    
    WIN.blit(BOARD,(0,0))    # actualizes BOARD -> always after all changes odf it
    
    pygame.display.update()
    

def waving_func(time):
    z = 127*math.cos((2*math.pi/(FPS*40))*time)
    return z

def game_mechanics(pos, token):
    
    global chosen_cell
    global pos_a
    global pos_b
    
    #print("en game_mechanics: ", token)
    
    
    
    
    if pos != None:
        
        selected_pos = grid_position(pos)
        if token != None:
            tokenpos = grid_position((token.rec.x, token.rec.y))
            if tokenpos == selected_pos:
                print("token = pos")
                token.moving = True
            else:pass
            """for obj in game_objects_list: 
                    if obj.moving:
                        obj.game_object_drawer(BOARD, pos_b)
                    else: obj.game_object_drawer(BOARD)"""
            
        selected_in_grid = GRID.index(selected_pos)
        chosen_cell = (pygame.Rect(CELL*selected_pos[0], CELL*selected_pos[1], CELL, CELL),pygame.time.get_ticks())
        pos_b = pygame.Vector2(chosen_cell[0].x, chosen_cell[0].y)
        print(selected_in_grid)
    
    
    for obj in game_objects_list: 
        print(obj.moving)
        if obj.moving:
            obj.game_object_drawer(BOARD, pos_b)
        else: obj.game_object_drawer(BOARD)
        
    #draw_window(pos, None)

    
def main():
    """ Main game function
    """
    
    run = True
    clock = pygame.time.Clock()
    
    
    prueba = GameObject(CELL, pos_a[0], pos_a[1], "token_1.png","prueba1")
    prueba2 = GameObject(CELL,300, 0, "token_2.png","prueba2")
    prueba3 = GameObject(CELL,700,700, "token_3.png","prueba3")
    prueba3.moving = False
    game_objects_list.append(prueba)
    game_objects_list.append(prueba2)
    game_objects_list.append(prueba3)
    print(str(game_objects_list))
    print(prueba)
    while run:
        
        clock.tick(FPS)
        pos = None
        chosen_token = None
        if BOARD.get_rect().collidepoint(pygame.mouse.get_pos()):
            
            pygame.mouse.set_cursor(pygame.cursors.diamond)
            for obj in game_objects_list:
                
                if obj.rec.collidepoint(pygame.mouse.get_pos()):
                    pygame.mouse.set_cursor(pygame.cursors.broken_x)
            
            """for obj in game_objects_list:
                
                if obj.rec.collidepoint(pygame.mouse.get_pos()):
                    pygame.mouse.set_cursor(pygame.cursors.broken_x)
                else: pygame.mouse.set_cursor(pygame.cursors.diamond)"""
        else: pygame.mouse.set_cursor(pygame.cursors.arrow)
        
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_cursor()==pygame.cursors.diamond:
                    pos = pygame.mouse.get_pos()
                    print("board ", pos)
                elif pygame.mouse.get_cursor()==pygame.cursors.broken_x:
                    pos = pygame.mouse.get_pos()
                    print("image pressed")
                    for obj in game_objects_list:
                        if obj.rec.collidepoint(pygame.mouse.get_pos()):
                            print(obj)
                            chosen_token = obj
                            print(type(chosen_token))
                        #else: chosen_token = None
        #game_mechanics(pos)           
        draw_window(pos, chosen_token)
    
    #prueba = GameObject(CELL, 0, 0)       
            
                
            
            
        
        
        
        
    
    pygame.quit()

    

if __name__=="__main__":
    print(GRID_DIC)
    main()
    