import pygame
import pygame_menu

from multiprocessing import Process

import os

from game_server import main as server_main

from main import Main

from constants import WIDTH, HEIGHT

"""pygame.init()"""
"""pygame.display.set_caption("TO CHANGE")"""
"""surface = pygame.display.set_mode((WIDTH, HEIGHT))"""

def set_difficulty():
    # Do the job here !
    os.system("cls")
    
    server = Process(target = server_main)
    server.start()
    

def start_game():
    #server = Process(target = server_main)
    #server.start()
    pass

def main_menu():
    pygame.init()
    pygame.display.set_caption("TO CHANGE")
    surface = pygame.display.set_mode((WIDTH, HEIGHT))

    menu = pygame_menu.Menu('Welcome', 400, 300, theme=pygame_menu.themes.THEME_BLUE)

    menu.add.text_input('Name :', default='John Doe')
    menu.add.button('Host ', set_difficulty)
    menu.add.button('Play', start_game)
    menu.add.button('Quit', pygame_menu.events.EXIT)


    menu.mainloop(surface)
    
if __name__=="__main__":
    
    main_menu()
#server = Process(target = server_main)
#server.start()