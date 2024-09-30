import pygame
from game_network import Network
from pickleobj import Exchange_object
from player_turn_module import Player_Object

width = 500
height = 500
win = pygame.display.set_mode((width, height))


class Main():
    def __init__(self) -> None:
        
        pygame.display.init()
        pygame.font.init()
        pygame.display.set_caption("TO CHANGE")
        
        self.player_a = Player_Object("INVESTIGATORS")
        self.player_b = Player_Object("SERPENT_PEOPLE")
        
        self.player_a_exchange = Exchange_object("player_a")
        self.player_b_exchange = Exchange_object("player_b")
        
        
        self.run = True
        self.clock = pygame.time.Clock()
        
        self.mousepos = pygame.mouse.get_pos()
        
    def main(self):
        pygame.display.init()
        pygame.font.init()
        pygame.display.set_caption("TO CHANGE")
        self.net = Network()
        self.player_a_exchange = self.net.getP()
        print("player_a: ",self.player_a_exchange) 
        bucle = 0
        
        while self.run:
            
            self.clock.tick(1)
            #self.player_a_exchange = self.player_a.exchanger_method_forward()
            self.player_b_exchange = self.net.send(self.player_a_exchange)
            #self.player_b.exchanger_method_backward()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    pygame.quit()
            
            try: 
                print(self.player_a_exchange, " vs ", self.player_b_exchange, " tick: ", bucle)
                print(self.player_b_exchange.player_spell_deck)
                bucle += 1
            except: print("waitng")
            
    
    def draw(self):
        win.fill((255,255,255))
        pygame.display.update()
    
    def data_exchange(self):
        
        pass
    
    
def redrawWindow(win,player, player2):
    win.fill((255,255,255))
    player.draw(win)
    player2.draw(win)
    pygame.display.update()


def main2():
    run = True
    n = Network()
    p = n.getP()
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        p2 = n.send(p)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        p.move()
        redrawWindow(win, p, p2)

M = Main()
M.main()