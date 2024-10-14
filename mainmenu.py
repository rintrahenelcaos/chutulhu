import pygame
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.dropdown import Dropdown


from multiprocessing import Process

import os

from game_server import main as server_main

from main import Main

from game_network import Network

from constants import WIDTH, HEIGHT, CELL, FACTIONS
#pygame.init()
#pygame.display.set_caption("TO CHANGE")
#pygame.font.init()
#WIN = pygame.display.set_mode((WIDTH, HEIGHT))

"""faction_dropdown = Dropdown(WIN, CELL*8, CELL*3, CELL*3, CELL*4/5, "choose faction", choices=FACTIONS, direction='down', textHAlign='left')

def faction_selector():
    faction = faction_dropdown.getSelected()
    print(faction)
    return faction

faction_chosen_button = Button(WIN, CELL*8, CELL*2, CELL*3, CELL*4/5, text = "continue", onClick = lambda: faction_selector())"""


#host_button = Button(WIN, CELL*3, CELL*3, CELL*3, CELL*4/5, text = "host game", onClick = lambda: self.host_game_method())
#join_button = Button(WIN, CELL*3, CELL*4, CELL*3, CELL*4/5, text = "Join game", onClick = lambda: self.net.connect(self.faction))

def host_game():
    
    os.system("cls")
    server = Process(target = server_main)
    server.start()
    #net.connect(faction)

def join_game(window):
    faction_menu(window)


def main_menu():
    pygame.init()
    pygame.display.set_caption("TO CHANGE")
    pygame.font.init()
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    host_button = Button(WIN, CELL*3, CELL*3, CELL*3, CELL*4/5, text = "host game", onClick = lambda: host_game())
    join_button = Button(WIN, CELL*3, CELL*4, CELL*3, CELL*4/5, text = "Join game", onClick = lambda: join_game(WIN))
    run = True
    
    while run:
        #WIN.fill("black")
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                """try:
                    net.send("!DISCONNECT")
                except: pass"""
                pygame.quit()
                run = False
                quit()
        WIN.fill("black")
        pygame_widgets.update(events)
        pygame.display.update()
        
    pygame.quit()
    
    
    pass

def faction_selector(faction_dropdown):
    faction = faction_dropdown.getSelected()
    print(faction)
    faction = faction

def faction_menu(window):
    faction_dropdown = Dropdown(window, CELL*8, CELL*3, CELL*3, CELL*4/5, "choose faction", choices=FACTIONS, direction='down', textHAlign='left')
    faction_chosen_button = Button(window, CELL*8, CELL*2, CELL*3, CELL*4/5, text = "continue", onClick = lambda: faction_selector(faction_dropdown))
    run = True
    
    while run:
        #WIN.fill("black")
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                """try:
                    net.send("!DISCONNECT")
                except: pass"""
                pygame.quit()
                run = False
                quit()
        window.fill("black")
        pygame_widgets.update(events)
        pygame.display.update()
        
    pygame.quit()
    
    
    pass  

class Main_menu():
    def __init__(self) -> None:
        #self.WIN = window
        pygame.init()
        pygame.display.set_caption("TO CHANGE")
        pygame.font.init()

        self.WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        self.net = Network()
        self.faction = str
        self.run = True   
        self.menu = "first" 
        #self.faction_dropdown, self.faction_chosen_button, self.host_button, self.join_button = None, None, None, None
        # Main Menu Objects
        
        self.faction_dropdown = Dropdown(self.WIN, CELL*8, CELL*3, CELL*3, CELL*4/5, "choose faction", choices=FACTIONS, direction='down', textHAlign='left')
        self.faction_chosen_button = Button(self.WIN, CELL*8, CELL*2, CELL*3, CELL*4/5, text = "continue", onClick = lambda: self.faction_selector())
        self.host_button = Button(self.WIN, CELL*3, CELL*3, CELL*3, CELL*4/5, text = "host game", onClick = lambda: self.host_game_method())
        self.join_button = Button(self.WIN, CELL*3, CELL*4, CELL*3, CELL*4/5, text = "Join game", onClick = lambda: self.net.connect(self.faction))
        
    
    def main_menu(self):
       
        while self.run:
        
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    try:
                        self.net.send("!DISCONNECT")
                    except: pass
                    pygame.quit()
                    self.run = False
                    quit()
        
            self.WIN.fill("black")
            pygame_widgets.update(events)
            pygame.display.update()
        
        pygame.quit()

    def host_game_method(self):
        os.system("cls")
        server = Process(target = server_main)
        server.start()
        #self.net.connect(self.faction)

    def faction_selector(self):
        faction = self.faction_dropdown.getSelected()
        print(faction)
        self.faction = faction
            
    def second_menu(self):
        pass


"""run = True
while run:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
            quit()

    

    pygame_widgets.update(events)
    pygame.display.update()"""            
if __name__=="__main__":
    
    men = Main_menu()
    men.main_menu()