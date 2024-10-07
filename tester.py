import pygame
from game_network import Network
from pickleobj import Exchange_object
from player_turn_module import Player_Object
from constants import FACTIONS

width = 500
height = 500
win = pygame.display.set_mode((width, height))


class Main():
    def __init__(self, faction) -> None:
        
        self.faction = faction
        pygame.display.init()
        pygame.font.init()
        pygame.display.set_caption("TO CHANGE")
        
        self.player_a = Player_Object(self.faction)
        self.player_b = Player_Object("")
        
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
        self.net.connect()
        #self.player_a_exchange = self.net.getP()
        #print("player_a: ",self.player_a_exchange) 
        bucle = 0
        
        while self.run:
            
            self.clock.tick(1)
            self.player_a_exchange = self.player_a.exchanger_method_forward()
            #print(self.net.send(self.player_a.player_faction))
            #self.player_b.exchanger_method_backward()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    self.net.send("!DISCONNECT")
                    pygame.quit()
            
            try:
                
                online = self.net.send(self.player_a.player_exchange_obj)
                if online != "NONE":
                    self.player_b.exchanger_method_backward()
                    print(self.player_b)
                #print(self.net.send(self.player_a.player_faction), " tick: ", bucle)
                
                #print(self.player_a_exchange, " vs ", self.player_b_exchange, " tick: ", bucle)
                #print(self.player_b_exchange.player_spell_deck)
                
                bucle += 1
                """if bucle > 5:
                    self.net.send("!DISCONNECT")"""
    
                
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


def main():
    count = 0
    while True:
        for faction in FACTIONS:
            print(count,".",faction)
        option = input("faction: ")
        if option in FACTIONS:
        
            M = Main(option)
            M.main()
            break
    


if __name__ == "__main__":
    
    main()
